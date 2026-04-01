from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = REPO_DIR / "evaluation" / "worker_status_pilot"
DEFAULT_BATCH_SIZE = 100
DEFAULT_TIMEOUT = 20

KEEP_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"근로자성"),
    re.compile(r"근로자에\s*해당"),
    re.compile(r"근로기준법상\s*근로자"),
    re.compile(r"당사자적격"),
    re.compile(r"사용종속관계"),
    re.compile(r"종속적\s*관계"),
    re.compile(r"종속관계"),
    re.compile(r"계약의\s*형식"),
    re.compile(r"실질에\s*있어"),
    re.compile(r"고용계약인지"),
    re.compile(r"도급계약인지"),
    re.compile(r"위임계약인지"),
    re.compile(r"임금을\s*목적으로"),
    re.compile(r"지휘\s*감독"),
    re.compile(r"출퇴근"),
    re.compile(r"사업소득세"),
    re.compile(r"4대보험"),
    re.compile(r"독자적\s*사업"),
    re.compile(r"업무수행\s*과정"),
)

FALSE_POSITIVE_BUCKETS: dict[str, tuple[re.Pattern[str], ...]] = {
    "도급만": (
        re.compile(r"도급"),
        re.compile(r"위임계약"),
        re.compile(r"운영계약"),
    ),
    "파견만": (
        re.compile(r"파견"),
        re.compile(r"근로자파견"),
    ),
    "전보": (
        re.compile(r"전보"),
        re.compile(r"인사발령"),
        re.compile(r"배치전환"),
        re.compile(r"대기발령"),
    ),
    "양정": (
        re.compile(r"양정"),
        re.compile(r"과도"),
        re.compile(r"과중"),
        re.compile(r"비례원칙"),
        re.compile(r"감봉"),
        re.compile(r"정직"),
    ),
    "괴롭힘": (
        re.compile(r"직장\s*내\s*괴롭힘"),
        re.compile(r"괴롭힘"),
        re.compile(r"성희롱"),
    ),
}


@dataclass(frozen=True)
class PilotRow:
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
    parser = argparse.ArgumentParser(description="Diagnose worker_status over-tagging without mutating DB by default")
    parser.add_argument("--apply-db", action="store_true", help="worker_status 제거 업데이트를 실제 DB에 반영")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--output-dir", help="출력 디렉터리")
    parser.add_argument("--limit", type=int, help="처리 건수 제한")
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
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }


def ensure_output_dir(path_arg: str | None) -> Path:
    if path_arg:
        output_dir = Path(path_arg)
    else:
        output_dir = DEFAULT_OUTPUT_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def fetch_worker_status_rows(timeout: int, limit: int | None) -> list[PilotRow]:
    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    rows: list[PilotRow] = []
    offset = 0
    page_size = 1000

    while True:
        current_limit = page_size if limit is None else min(page_size, max(limit - len(rows), 0))
        if current_limit <= 0:
            break
        params = {
            "select": "id,title,case_number,department,decision_date,decision_result,key_issue,holding_summary,holding_points,reason_category",
            "reason_category": "cs.{worker_status}",
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
                PilotRow(
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
        if len(chunk) < current_limit or (limit is not None and len(rows) >= limit):
            break
        offset += len(chunk)

    return rows


def build_text(row: PilotRow) -> str:
    return " ".join(
        value for value in (row.title, row.key_issue, row.holding_summary, row.holding_points) if value
    )


def classify_row(row: PilotRow) -> tuple[bool, str]:
    text = build_text(row)
    if any(pattern.search(text) for pattern in KEEP_PATTERNS):
        return True, "정탐"

    for bucket, patterns in FALSE_POSITIVE_BUCKETS.items():
        if any(pattern.search(text) for pattern in patterns):
            return False, bucket

    return False, "기타"


def summarize_row(row: PilotRow) -> dict[str, Any]:
    return {
        "id": row.id,
        "case_number": row.case_number,
        "department": row.department,
        "decision_date": row.decision_date,
        "decision_result": row.decision_result,
        "title": row.title,
        "key_issue": row.key_issue[:240],
        "holding_summary": row.holding_summary[:240],
        "holding_points": row.holding_points[:240],
        "reason_category": row.reason_category,
    }


def apply_updates(rows_to_update: list[PilotRow], timeout: int, batch_size: int) -> int:
    if not rows_to_update:
        return 0

    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    updated = 0

    for start in range(0, len(rows_to_update), batch_size):
        batch = rows_to_update[start:start + batch_size]
        for row in batch:
            next_reasons = [reason for reason in row.reason_category if reason != "worker_status"]
            if not next_reasons:
                next_reasons = ["other"]
            response = requests.patch(
                f"{supabase_url}/rest/v1/nlrc_decisions?id=eq.{row.id}",
                headers=headers,
                json={"reason_category": next_reasons},
                timeout=timeout,
            )
            if response.status_code not in (200, 204):
                raise RuntimeError(f"update failed for {row.id}: {response.status_code} {response.text[:400]}")
            updated += 1
        time.sleep(0.1)

    return updated


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    load_env_file()
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir)

    rows = fetch_worker_status_rows(timeout=args.timeout, limit=args.limit)
    kept: list[PilotRow] = []
    removed: list[PilotRow] = []
    bucket_counter: Counter[str] = Counter()

    for row in rows:
        keep, bucket = classify_row(row)
        bucket_counter[bucket] += 1
        if keep:
            kept.append(row)
        else:
            removed.append(row)

    before_granted = [row for row in rows if row.decision_result == "granted"][:20]
    after_granted = [row for row in kept if row.decision_result == "granted"][:20]

    removed_payload = []
    for row in removed:
        next_reasons = [reason for reason in row.reason_category if reason != "worker_status"]
        if not next_reasons:
            next_reasons = ["other"]
        removed_payload.append({
            "id": row.id,
            "before_reason_category": row.reason_category,
            "after_reason_category": next_reasons,
            "title": row.title,
            "case_number": row.case_number,
        })

    applied_updates = 0
    if args.apply_db:
        applied_updates = apply_updates(removed, timeout=args.timeout, batch_size=args.batch_size)

    report = {
        "scope": "worker_status_pilot",
        "total_worker_status_rows": len(rows),
        "kept_worker_status_rows": len(kept),
        "removed_worker_status_rows": len(removed),
        "removed_ratio": round((len(removed) / len(rows)) if rows else 0.0, 4),
        "bucket_breakdown": dict(bucket_counter),
        "granted_before_count": sum(1 for row in rows if row.decision_result == "granted"),
        "granted_after_count": sum(1 for row in kept if row.decision_result == "granted"),
        "applied_updates": applied_updates,
        "limit": args.limit,
    }

    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_jsonl(output_dir / "worker_status_removal_candidates.jsonl", removed_payload)

    sample_lines = ["# worker_status 시범 정제 샘플", "", "## 정탐 예시", ""]
    for row in kept[:25]:
        sample_lines.append(f"- `{row.id}` {row.title}")
        sample_lines.append(f"  - 사건번호: {row.case_number} | 결과: {row.decision_result}")
        sample_lines.append(f"  - 요약: {(row.holding_summary or row.key_issue or row.holding_points)[:180]}")
    sample_lines.extend(["", "## 오탐 예시", ""])
    for row in removed[:25]:
        keep, bucket = classify_row(row)
        sample_lines.append(f"- `{row.id}` [{bucket}] {row.title}")
        sample_lines.append(f"  - 사건번호: {row.case_number} | 결과: {row.decision_result}")
        sample_lines.append(f"  - 요약: {(row.holding_summary or row.key_issue or row.holding_points)[:180]}")
    (output_dir / "worker_status_samples.md").write_text("\n".join(sample_lines), encoding="utf-8")

    compare_lines = [
        "# browse/list 전후 비교",
        "",
        "조건: 검색어 없음 · 사유 근로자성 분쟁 · 결과 인정(구제) · mode=baseline",
        "",
        f"- 전체 worker_status 태그 건수: {len(rows):,}",
        f"- 정제 후 유지 건수: {len(kept):,}",
        f"- 제거 후보 건수: {len(removed):,}",
        "",
        "## 정제 전 상위 20건",
        "",
    ]
    for row in before_granted:
        compare_lines.append(f"- `{row.id}` {row.title}")
        compare_lines.append(f"  - {row.department} | {row.decision_date} | {row.case_number}")
    compare_lines.extend(["", "## 정제 후 상위 20건", ""])
    for row in after_granted:
        compare_lines.append(f"- `{row.id}` {row.title}")
        compare_lines.append(f"  - {row.department} | {row.decision_date} | {row.case_number}")
    (output_dir / "browse_list_compare.md").write_text("\n".join(compare_lines), encoding="utf-8")

    summary_doc = [
        "# worker_status 시범 정제 기준",
        "",
        "## 유지 기준",
        "- `근로자성`, `근로자에 해당`, `근로기준법상 근로자`, `당사자적격`, `사용종속관계`, `종속적 관계`, `종속관계` 직접 표현이 있는 경우 유지",
        "- `계약의 형식보다 실질`, `고용계약인지 도급계약인지`, `임금을 목적으로`, `지휘감독`, `출퇴근`, `사업소득세`, `4대보험`처럼 근로자성 판단 문맥이 있는 경우 유지",
        "",
        "## 제거 우선 기준",
        "- `도급`, `위임계약`, `운영계약`, `파견`이 있어도 근로자성 판단 문맥이 없으면 제거 후보로 분류",
        "- `전보`, `인사발령`, `배치전환`, `대기발령` 중심 사건",
        "- `양정`, `과도`, `과중`, `비례원칙`, `감봉`, `정직` 중심 징계양정 사건",
        "- `직장내괴롭힘`, `괴롭힘`, `성희롱` 중심 사건",
        "",
        "## 확장 순서",
        "1. worker_status",
        "2. contract_expiry / probation / no_dismissal",
        "3. transfer / incompetence",
        "4. misconduct / violence / embezzlement",
        "5. workplace_bullying / sexual_harassment",
        "6. union_activity / discrimination / redundancy",
    ]
    (REPO_DIR / "docs" / "worker_status_refinement_rules.md").write_text("\n".join(summary_doc), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
