from __future__ import annotations

import argparse
import json
import os
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = REPO_DIR / "evaluation" / "reason_category_refinement"
DEFAULT_BATCH_SIZE = 100
DEFAULT_TIMEOUT = 20
PAGE_SIZE = 1000

DEFAULT_TARGET_CATEGORIES: tuple[str, ...] = ("worker_status", "no_dismissal", "incompetence")

REASON_TEXT_GUARDS: dict[str, list[str]] = {
    "worker_status": [
        "근로자성",
        "근로자에 해당",
        "근로기준법상 근로자",
        "당사자적격",
        "종속적 관계",
        "종속관계",
        "사용종속관계",
        "계약의 형식",
        "도급계약인지",
        "고용계약인지",
        "실질에 있어",
        "임금을 목적으로",
        "지휘감독",
        "출퇴근",
        "사업소득세",
        "4대보험",
        "독자적 사업",
        "업무수행 과정",
    ],
    "no_dismissal": [
        "해고가 존재하지",
        "해고부존재",
        "권고사직",
        "사직서",
        "자발적 사직",
        "합의 퇴직",
        "합의해지",
        "해고로 볼 수 없",
        "당연퇴직",
        "사직의 의사",
        "근로관계 종료",
    ],
    "incompetence": [
        "업무능력 부족",
        "저성과",
        "근무성적 불량",
        "부적격",
        "실적 최하위",
        "개선 기회",
        "개선기회",
        "경고",
        "시정",
        "교육",
        "본채용 거부",
        "능력 부족",
        "업무수행 능력",
    ],
}


@dataclass(frozen=True)
class DecisionRow:
    id: str
    title: str
    case_number: str
    department: str
    decision_date: str
    decision_result: str
    key_issue: str
    holding_summary: str
    holding_points: str
    reason_category: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate DB-ready refinement payloads for selected reason categories without mutating DB by default"
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=list(DEFAULT_TARGET_CATEGORIES),
        help="대상 reason_category 목록",
    )
    parser.add_argument("--apply-db", action="store_true", help="생성된 payload를 실제 DB에 반영")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--output-dir")
    parser.add_argument("--limit-per-reason", type=int, default=0)
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() not in os.environ:
                os.environ[name.strip()] = value.strip()


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} must be set")
    return value


def build_headers() -> dict[str, str]:
    service_key = require_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }


def ensure_output_dir(path_arg: str | None) -> Path:
    if path_arg:
        output_dir = Path(path_arg)
    else:
        output_dir = DEFAULT_OUTPUT_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def fetch_reason_rows(reason: str, timeout: int, limit_per_reason: int) -> list[DecisionRow]:
    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    rows: list[DecisionRow] = []
    offset = 0

    while True:
        current_limit = PAGE_SIZE
        if limit_per_reason > 0:
            current_limit = min(PAGE_SIZE, max(limit_per_reason - len(rows), 0))
        if current_limit <= 0:
            break

        params = {
            "select": "id,title,case_number,department,decision_date,decision_result,key_issue,holding_summary,holding_points,reason_category",
            "reason_category": f"cs.{{{reason}}}",
            "order": "decision_date.desc.nullslast,id.asc",
            "limit": str(current_limit),
            "offset": str(offset),
        }
        response = requests.get(
            f"{supabase_url}/rest/v1/nlrc_decisions",
            headers=headers,
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        chunk = response.json()
        if not chunk:
            break

        for row in chunk:
            rows.append(
                DecisionRow(
                    id=str(row.get("id") or ""),
                    title=str(row.get("title") or ""),
                    case_number=str(row.get("case_number") or ""),
                    department=str(row.get("department") or ""),
                    decision_date=str(row.get("decision_date") or ""),
                    decision_result=str(row.get("decision_result") or ""),
                    key_issue=str(row.get("key_issue") or ""),
                    holding_summary=str(row.get("holding_summary") or ""),
                    holding_points=str(row.get("holding_points") or ""),
                    reason_category=list(row.get("reason_category") or []),
                )
            )

        if len(chunk) < current_limit or (limit_per_reason > 0 and len(rows) >= limit_per_reason):
            break
        offset += len(chunk)

    return rows


def build_text(row: DecisionRow) -> str:
    return " ".join(
        value for value in (row.title, row.key_issue, row.holding_summary, row.holding_points) if value
    ).lower()


def passes_guard(row: DecisionRow, markers: list[str]) -> bool:
    haystack = build_text(row)
    return any(marker.lower() in haystack for marker in markers)


def summarize_row(row: DecisionRow) -> dict[str, Any]:
    return {
        "id": row.id,
        "title": row.title,
        "case_number": row.case_number,
        "department": row.department,
        "decision_date": row.decision_date,
        "decision_result": row.decision_result,
        "summary": (row.holding_summary or row.key_issue or row.holding_points)[:240],
        "reason_category": row.reason_category,
    }


def next_reason_category(row: DecisionRow, removed_reason: str) -> list[str]:
    remaining = [reason for reason in row.reason_category if reason != removed_reason]
    return remaining or ["other"]


def build_update_payload(row: DecisionRow, removed_reason: str) -> dict[str, Any]:
    return {
        "id": row.id,
        "old_reason_category": row.reason_category,
        "new_reason_category": next_reason_category(row, removed_reason),
        "removed_reason": removed_reason,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def apply_updates(updates: list[dict[str, Any]], timeout: int, batch_size: int) -> int:
    if not updates:
        return 0

    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    updated = 0

    for start in range(0, len(updates), batch_size):
        batch = updates[start:start + batch_size]
        for update in batch:
            response = requests.patch(
                f"{supabase_url}/rest/v1/nlrc_decisions?id=eq.{update['id']}",
                headers=headers,
                json={"reason_category": update["new_reason_category"]},
                timeout=timeout,
            )
            if response.status_code not in (200, 204):
                raise RuntimeError(
                    f"update failed for {update['id']}: {response.status_code} {response.text[:400]}"
                )
            updated += 1
        time.sleep(0.1)

    return updated


def main() -> None:
    load_env_file()
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir)

    markdown_lines = [
        "# reason_category 정제 payload 생성",
        "",
        "이번 산출물은 browse/list 가드 기준으로 **DB 반영 직전 payload**를 생성한 결과입니다.",
        "",
    ]

    overall_counter: Counter[str] = Counter()
    report_rows: list[dict[str, Any]] = []
    all_updates: list[dict[str, Any]] = []

    for reason in args.categories:
        markers = REASON_TEXT_GUARDS.get(reason)
        if not markers:
            raise RuntimeError(f"unsupported category: {reason}")

        rows = fetch_reason_rows(reason=reason, timeout=args.timeout, limit_per_reason=args.limit_per_reason)
        kept = [row for row in rows if passes_guard(row, markers)]
        removed = [row for row in rows if not passes_guard(row, markers)]
        granted_before = sum(1 for row in rows if row.decision_result == "granted")
        granted_after = sum(1 for row in kept if row.decision_result == "granted")
        updates = [build_update_payload(row, reason) for row in removed]
        all_updates.extend(updates)

        overall_counter["total"] += len(rows)
        overall_counter["kept"] += len(kept)
        overall_counter["removed"] += len(removed)
        overall_counter["granted_before"] += granted_before
        overall_counter["granted_after"] += granted_after

        detail = {
            "reason": reason,
            "markers": markers,
            "total": len(rows),
            "kept": len(kept),
            "removed": len(removed),
            "kept_ratio": round((len(kept) / len(rows)) if rows else 0.0, 4),
            "granted_before": granted_before,
            "granted_after": granted_after,
            "kept_examples": [summarize_row(row) for row in kept[:15]],
            "removed_examples": [summarize_row(row) for row in removed[:15]],
        }
        (output_dir / f"{reason}_detail.json").write_text(
            json.dumps(detail, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        write_jsonl(output_dir / f"{reason}_updates.jsonl", updates)

        report_rows.append(
            {
                "reason": reason,
                "total": len(rows),
                "kept": len(kept),
                "removed": len(removed),
                "kept_ratio": round((len(kept) / len(rows)) if rows else 0.0, 4),
                "granted_before": granted_before,
                "granted_after": granted_after,
                "update_candidates": len(updates),
            }
        )

        markdown_lines.extend(
            [
                f"## {reason}",
                f"- 전체: {len(rows):,}",
                f"- 유지: {len(kept):,}",
                f"- 제거 후보: {len(removed):,}",
                f"- 인정(구제) 전/후: {granted_before:,} -> {granted_after:,}",
                f"- payload: `{reason}_updates.jsonl`",
                "",
                "### 유지 샘플",
            ]
        )
        for sample in detail["kept_examples"][:5]:
            markdown_lines.append(
                f"- `{sample['case_number']}` {sample['title']} | {sample['summary']}"
            )
        markdown_lines.extend(["", "### 제거 후보 샘플"])
        for sample in detail["removed_examples"][:5]:
            markdown_lines.append(
                f"- `{sample['case_number']}` {sample['title']} | {sample['summary']}"
            )
        markdown_lines.append("")

    write_jsonl(output_dir / "all_updates.jsonl", all_updates)

    applied_count = 0
    if args.apply_db:
        applied_count = apply_updates(all_updates, timeout=args.timeout, batch_size=args.batch_size)

    report = {
        "scope": "reason_category_refinement_payloads",
        "categories": args.categories,
        "total_rows": overall_counter["total"],
        "kept_rows": overall_counter["kept"],
        "removed_rows": overall_counter["removed"],
        "granted_before": overall_counter["granted_before"],
        "granted_after": overall_counter["granted_after"],
        "update_candidates": len(all_updates),
        "db_applied": bool(args.apply_db),
        "db_applied_count": applied_count,
        "rows": report_rows,
    }

    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "summary.md").write_text("\n".join(markdown_lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
