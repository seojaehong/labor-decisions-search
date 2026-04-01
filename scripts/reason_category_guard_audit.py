from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = REPO_DIR / "evaluation" / "reason_category_guard_audit"
DEFAULT_TIMEOUT = 20
PAGE_SIZE = 1000

REASON_TEXT_GUARDS: dict[str, list[str]] = {
    "absence": ["무단결근", "무단 이탈", "연락 두절", "근태 불량", "지각", "결근", "출근하지"],
    "workplace_bullying": ["직장내괴롭힘", "괴롭힘", "괴롭힘 행위", "따돌림", "신고 후", "분리조치", "접촉금지"],
    "sexual_harassment": ["성희롱", "성추행", "성적 언동", "성폭력"],
    "violence": ["폭행", "폭언", "욕설", "협박", "모욕", "가혹행위"],
    "embezzlement": ["횡령", "배임", "공금 유용", "착복", "부정 수령", "금전 비위"],
    "incompetence": ["업무능력 부족", "저성과", "근무성적 불량", "부적격", "실적 최하위", "개선 기회", "본채용 거부"],
    "probation": ["수습", "시용", "본채용 거부", "수습기간", "수습 평가"],
    "redundancy": ["경영상 해고", "정리해고", "구조조정", "경영 악화", "인원 감축", "사업 폐지"],
    "transfer": ["전보", "인사발령", "배치전환", "대기발령", "전직명령", "보직 변경"],
    "misconduct": ["비위행위", "복무규정 위반", "복종의무 위반", "업무 지시 불이행", "허위 보고", "겸직", "징계사유"],
    "contract_expiry": ["갱신기대권", "계약만료", "기간제", "계약 갱신", "재계약", "근로계약 기간"],
    "no_dismissal": ["해고가 존재하지", "해고부존재", "권고사직", "사직서", "자발적 사직", "합의 퇴직"],
    "union_activity": ["부당노동행위", "노동조합", "지배개입", "불이익취급", "조합활동", "단체교섭", "단체협약"],
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
    ],
    "discrimination": ["차별시정", "차별적 처우", "비교 대상 근로자", "동일가치노동", "남녀고용평등"],
}


@dataclass(frozen=True)
class AuditRow:
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
    parser = argparse.ArgumentParser(description="Audit positive text guards for browse/list reason filters")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--output-dir")
    parser.add_argument("--limit-per-reason", type=int, default=0)
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
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
    }


def ensure_output_dir(path_arg: str | None) -> Path:
    if path_arg:
        output_dir = Path(path_arg)
    else:
        output_dir = DEFAULT_OUTPUT_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def fetch_reason_rows(reason: str, timeout: int, limit_per_reason: int) -> list[AuditRow]:
    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    rows: list[AuditRow] = []
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
                AuditRow(
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


def build_text(row: AuditRow) -> str:
    return " ".join(
        value for value in (row.title, row.key_issue, row.holding_summary, row.holding_points) if value
    ).lower()


def passes_guard(row: AuditRow, markers: list[str]) -> bool:
    haystack = build_text(row)
    return any(marker.lower() in haystack for marker in markers)


def summarize_row(row: AuditRow) -> dict[str, Any]:
    return {
        "id": row.id,
        "title": row.title,
        "case_number": row.case_number,
        "department": row.department,
        "decision_date": row.decision_date,
        "decision_result": row.decision_result,
        "summary": (row.holding_summary or row.key_issue or row.holding_points)[:220],
        "reason_category": row.reason_category,
    }


def main() -> None:
    load_env_file()
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir)

    report_rows: list[dict[str, Any]] = []
    summary_lines = ["# reason_category browse/list 가드 진단", ""]
    overall_counts = Counter()

    for reason, markers in REASON_TEXT_GUARDS.items():
        rows = fetch_reason_rows(reason, timeout=args.timeout, limit_per_reason=args.limit_per_reason)
        kept = [row for row in rows if passes_guard(row, markers)]
        removed = [row for row in rows if not passes_guard(row, markers)]
        granted_before = sum(1 for row in rows if row.decision_result == "granted")
        granted_after = sum(1 for row in kept if row.decision_result == "granted")
        overall_counts["total"] += len(rows)
        overall_counts["kept"] += len(kept)
        overall_counts["removed"] += len(removed)

        report_rows.append(
            {
                "reason": reason,
                "total": len(rows),
                "kept": len(kept),
                "removed": len(removed),
                "kept_ratio": round((len(kept) / len(rows)) if rows else 0.0, 4),
                "granted_before": granted_before,
                "granted_after": granted_after,
                "markers": markers,
            }
        )

        detail = {
            "reason": reason,
            "markers": markers,
            "total": len(rows),
            "kept": len(kept),
            "removed": len(removed),
            "kept_ratio": round((len(kept) / len(rows)) if rows else 0.0, 4),
            "granted_before": granted_before,
            "granted_after": granted_after,
            "kept_examples": [summarize_row(row) for row in kept[:10]],
            "removed_examples": [summarize_row(row) for row in removed[:10]],
        }
        (output_dir / f"{reason}.json").write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")

        summary_lines.append(f"## {reason}")
        summary_lines.append(f"- 전체: {len(rows):,}")
        summary_lines.append(f"- 가드 통과: {len(kept):,}")
        summary_lines.append(f"- 제거 후보: {len(removed):,}")
        summary_lines.append(f"- 인정(구제) 전/후: {granted_before:,} -> {granted_after:,}")
        summary_lines.append("")

    report = {
        "scope": "reason_category_guard_audit",
        "total_rows": overall_counts["total"],
        "kept_rows": overall_counts["kept"],
        "removed_rows": overall_counts["removed"],
        "rows": report_rows,
        "limit_per_reason": args.limit_per_reason,
    }
    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
