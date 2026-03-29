from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

from lawgo_keyword_tagger import TAG_RULES


REPO_DIR = Path(__file__).parent.parent
DEFAULT_OUTPUT_ROOT = REPO_DIR / "evaluation" / "data_refinement"
DEFAULT_BATCH_SIZE = 100
DEFAULT_TIMEOUT = 20
DEFAULT_BIGCASE_CASES_INPUT = REPO_DIR / "evaluation" / "bigcase_bulk" / "court_decisions_ready.jsonl"

VERDICT_RULES: list[tuple[str, str]] = [
    ("일부승소", r"일부승|일부 인용|일부 인정"),
    ("파기환송", r"파기환송"),
    ("화해", r"화해|조정성립|조정 갈음"),
    ("각하", r"각하"),
    ("기각", r"상고기각|항소기각|기각"),
    ("승소", r"원고승|피고패|인용|승소"),
    ("패소", r"원고패|피고승|패소"),
]

REASON_TO_LAWGO_KEYWORDS: dict[str, list[str]] = {
    "absence": ["부당해고", "취업규칙", "해고부존재"],
    "workplace_bullying": ["직장내괴롭힘", "성희롱", "폭언/폭행"],
    "sexual_harassment": ["성희롱", "직장내괴롭힘"],
    "violence": ["폭언/폭행", "비위행위"],
    "embezzlement": ["횡령/배임", "비위행위"],
    "incompetence": ["부당해고", "전보/인사이동"],
    "misconduct": ["비위행위", "부당해고", "취업규칙"],
    "redundancy": ["경영상해고", "부당해고"],
    "probation": ["수습", "본채용거부", "부당해고"],
    "transfer": ["전보/인사이동", "취업규칙"],
    "contract_expiry": ["갱신기대권", "기간제", "부당해고"],
    "no_dismissal": ["해고부존재", "부당해고"],
    "union_activity": ["노동조합", "부당노동행위", "단체교섭", "단체협약", "조합활동", "쟁의행위"],
    "worker_status": ["근로자성", "파견", "도급"],
    "discrimination": ["남녀고용평등", "근로조건"],
    "wage_dispute": ["임금체불", "통상임금", "최저임금", "퇴직금", "연장근로", "휴일근로", "연차휴가"],
    "contract_termination": ["부당해고", "갱신기대권", "기간제", "해고부존재"],
    "workplace_safety": ["산재", "산업안전보건", "폭언/폭행"],
    "union_related": ["노동조합", "부당노동행위", "단체교섭", "파업", "쟁의행위", "조합활동"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refine cases/lawgo metadata for summary-first search")
    parser.add_argument("--apply-db", action="store_true", help="Supabase에 직접 업데이트")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--output-dir", help="출력 디렉터리")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
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


def fetch_paginated(
    endpoint: str,
    params: dict[str, str],
    timeout: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    page_size = 1000
    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()

    while True:
        merged = dict(params)
        merged["limit"] = str(page_size)
        merged["offset"] = str(offset)
        response = requests.get(
            f"{supabase_url}/rest/v1/{endpoint}",
            headers=headers,
            params=merged,
            timeout=timeout,
        )
        response.raise_for_status()
        chunk = response.json()
        if not chunk:
            break
        rows.extend(chunk)
        if len(chunk) < page_size:
            break
        offset += page_size

    return rows


def clean_text(text: str | None) -> str:
    value = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    return re.sub(r"\n{3,}", "\n\n", value)


def normalize_case_number(case_number: str | None) -> str:
    return re.sub(r"\s+", "", str(case_number or "")).strip()


def normalize_court_label(court: str | None) -> str | None:
    text = clean_text(court)
    if not text:
        return None
    if "대법원" in text:
        return "대법원"
    if "행정법원" in text:
        return "행정법원"
    if "고등법원" in text:
        return "고등법원"
    if "지방법원" in text or "지원" in text:
        return "지방법원"
    return text


def compile_tag_rules() -> list[tuple[str, list[re.Pattern[str]]]]:
    return [
        (tag, [re.compile(pattern, re.IGNORECASE) for pattern in patterns])
        for tag, patterns in TAG_RULES
    ]


def match_keywords(text: str, compiled_rules: list[tuple[str, list[re.Pattern[str]]]]) -> list[str]:
    matched: list[str] = []
    for tag, patterns in compiled_rules:
        if any(pattern.search(text) for pattern in patterns):
            matched.append(tag)
    return matched


def infer_verdict_type(title: str, summary: str) -> str:
    haystack = f"{title} {summary}"
    for verdict_type, pattern in VERDICT_RULES:
        if re.search(pattern, haystack):
            return verdict_type
    return ""


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_local_bigcase_summary_map(path: Path) -> dict[str, str]:
    summary_map: dict[str, str] = {}
    if not path.exists():
        return summary_map
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        row = json.loads(raw_line)
        case_number = normalize_case_number(row.get("case_number"))
        summary = clean_text(row.get("summary"))
        if case_number and summary and case_number not in summary_map:
            summary_map[case_number] = summary
    return summary_map


def chunked(rows: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [rows[index:index + batch_size] for index in range(0, len(rows), batch_size)]


def post_upsert(endpoint: str, rows: list[dict[str, Any]], on_conflict: str, timeout: int) -> None:
    response = requests.post(
        f"{require_env('SUPABASE_URL')}/rest/v1/{endpoint}?on_conflict={on_conflict}",
        headers=build_headers(),
        json=rows,
        timeout=timeout,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{endpoint}: {response.status_code} {response.text[:1000]}")


def main() -> None:
    load_env_file()
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir)
    compiled_rules = compile_tag_rules()

    cases_rows = fetch_paginated(
        "cases",
        {
            "select": "id,case_number,court,title,decision_date,verdict_type,keywords_matched,summary,holding_points,url",
        },
        args.timeout,
    )
    lawgo_rows = fetch_paginated(
        "lawgo_precedents",
        {
            "select": "id,api_id,title,reference_number,decision_date,court,judgment_type,issue_text,summary_text,keywords_matched,bigcase_case_id",
        },
        args.timeout,
    )
    summary_source = "decision_source_documents"
    try:
        source_docs = fetch_paginated(
            "decision_source_documents",
            {
                "select": "source_case_id,summary_raw,source_provider",
                "source_provider": "eq.bigcase",
            },
            args.timeout,
        )
        summary_by_case_number: dict[str, str] = {}
        for row in source_docs:
            key = normalize_case_number(str(row.get("source_case_id") or ""))
            summary_raw = clean_text(row.get("summary_raw"))
            if key and summary_raw and key not in summary_by_case_number:
                summary_by_case_number[key] = summary_raw
    except Exception:  # noqa: BLE001
        source_docs = []
        summary_by_case_number = load_local_bigcase_summary_map(DEFAULT_BIGCASE_CASES_INPUT)
        summary_source = "local_bigcase_jsonl"

    cases_updates: list[dict[str, Any]] = []
    cases_summary_filled = 0
    cases_verdict_filled = 0
    cases_keywords_filled = 0
    cases_tag_counter: Counter[str] = Counter()

    for row in cases_rows:
        case_number = normalize_case_number(row.get("case_number"))
        existing_summary = clean_text(row.get("summary"))
        derived_summary = summary_by_case_number.get(case_number, "")
        new_summary = existing_summary or derived_summary

        verdict_type = clean_text(row.get("verdict_type"))
        inferred_verdict = verdict_type or infer_verdict_type(str(row.get("title") or ""), new_summary)

        existing_keywords = row.get("keywords_matched") or []
        new_keywords = existing_keywords
        if not existing_keywords:
            new_keywords = match_keywords(
                f"{row.get('title') or ''}\n{new_summary}",
                compiled_rules,
            )

        summary_changed = (existing_summary or "") != (new_summary or "")
        verdict_changed = verdict_type != inferred_verdict
        keywords_changed = list(existing_keywords) != list(new_keywords)

        if not existing_summary and new_summary:
            cases_summary_filled += 1
        if not verdict_type and inferred_verdict:
            cases_verdict_filled += 1
        if not existing_keywords and new_keywords:
            cases_keywords_filled += 1
        for keyword in new_keywords:
            cases_tag_counter[keyword] += 1

        if summary_changed or verdict_changed or keywords_changed:
            merged_row = dict(row)
            merged_row["summary"] = new_summary or None
            merged_row["verdict_type"] = inferred_verdict
            merged_row["keywords_matched"] = new_keywords
            cases_updates.append(merged_row)

    lawgo_updates: list[dict[str, Any]] = []
    lawgo_summary_filled = 0
    lawgo_court_normalized = 0

    for row in lawgo_rows:
        existing_summary = clean_text(row.get("summary_text"))
        fallback_summary = clean_text(row.get("issue_text"))
        normalized_summary = existing_summary or fallback_summary or None
        normalized_court = normalize_court_label(row.get("court"))

        summary_changed = (existing_summary or "") != (normalized_summary or "")
        court_changed = normalized_court != row.get("court")

        if not existing_summary and fallback_summary:
            lawgo_summary_filled += 1
        if normalized_court and court_changed:
            lawgo_court_normalized += 1

        if summary_changed or court_changed:
            merged_row = dict(row)
            merged_row["summary_text"] = normalized_summary
            merged_row["court"] = normalized_court
            lawgo_updates.append(merged_row)

    cases_updates_path = output_dir / "cases_updates.jsonl"
    lawgo_updates_path = output_dir / "lawgo_updates.jsonl"
    write_jsonl(cases_updates_path, cases_updates)
    write_jsonl(lawgo_updates_path, lawgo_updates)
    mapped_keywords = sorted({keyword for keywords in REASON_TO_LAWGO_KEYWORDS.values() for keyword in keywords})
    available_keywords = sorted(tag for tag, _patterns in TAG_RULES)
    unmapped_keywords = [keyword for keyword in available_keywords if keyword not in mapped_keywords]

    db_status: dict[str, Any] = {"attempted": False, "success": None}
    if args.apply_db:
        db_status["attempted"] = True
        try:
            for batch in chunked(cases_updates, args.batch_size):
                post_upsert("cases", batch, "id", args.timeout)
                time.sleep(0.2)
            for batch in chunked(lawgo_updates, args.batch_size):
                post_upsert("lawgo_precedents", batch, "api_id", args.timeout)
                time.sleep(0.2)
            db_status["success"] = True
            db_status["cases_updated"] = len(cases_updates)
            db_status["lawgo_updated"] = len(lawgo_updates)
        except Exception as exc:  # noqa: BLE001
            db_status["success"] = False
            db_status["error"] = str(exc)

    report = {
        "cases_total": len(cases_rows),
        "cases_summary_filled": cases_summary_filled,
        "cases_verdict_filled": cases_verdict_filled,
        "cases_keywords_filled": cases_keywords_filled,
        "cases_top_keywords": cases_tag_counter.most_common(30),
        "lawgo_total": len(lawgo_rows),
        "lawgo_summary_filled": lawgo_summary_filled,
        "lawgo_court_normalized": lawgo_court_normalized,
        "decision_source_docs_total": len(source_docs),
        "summary_join_keys": len(summary_by_case_number),
        "summary_source": summary_source,
        "cases_updates_path": str(cases_updates_path),
        "lawgo_updates_path": str(lawgo_updates_path),
        "db_update": db_status,
        "reason_to_lawgo_keywords_size": len(REASON_TO_LAWGO_KEYWORDS),
        "tag_rule_count": len(TAG_RULES),
        "mapped_keywords_count": len(mapped_keywords),
        "unmapped_tag_rules": unmapped_keywords,
    }
    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
