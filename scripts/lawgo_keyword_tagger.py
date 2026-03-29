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


REPO_DIR = Path(__file__).parent.parent
DEFAULT_BATCH_SIZE = 100
DEFAULT_PARSE_VERSION = "lawgo-keyword-v1"
DEFAULT_OUTPUT_ROOT = REPO_DIR / "evaluation" / "lawgo" / "keyword_tagging"
DEFAULT_LAWGO_INPUTS = [
    REPO_DIR / "evaluation" / "lawgo" / "db_ready" / "20260329_162357" / "lawgo_precedents_ready.jsonl",
    REPO_DIR / "evaluation" / "lawgo" / "db_ready" / "20260329_221246" / "lawgo_precedents_ready.jsonl",
    REPO_DIR / "evaluation" / "lawgo" / "db_ready" / "20260329_222623" / "lawgo_precedents_ready.jsonl",
]
DEFAULT_BIGCASE_INPUT = REPO_DIR / "evaluation" / "bigcase_bulk" / "court_decisions_ready.jsonl"

TAG_RULES: list[tuple[str, list[str]]] = [
    ("단체협약", [r"단체협약"]),
    ("노동조합", [r"노동조합", r"\b노조\b"]),
    ("도급", [r"도급", r"용역계약", r"하도급"]),
    ("노동위원회", [r"노동위원회", r"중앙노동위원회", r"지방노동위원회"]),
    ("조합원", [r"조합원"]),
    ("손해배상", [r"손해배상", r"위자료", r"구상금"]),
    ("부당노동행위", [r"부당노동행위"]),
    ("파견", [r"파견", r"파견근로", r"불법파견"]),
    ("단체교섭", [r"단체교섭", r"교섭창구", r"교섭대표"]),
    ("파업", [r"파업", r"동맹파업"]),
    ("쟁의행위", [r"쟁의행위", r"쟁의조정", r"쟁의"]),
    ("조합활동", [r"조합활동", r"노조활동"]),
    ("부당해고", [r"부당해고", r"해고무효", r"해고무효확인", r"해고취소"]),
    ("임금체불", [r"임금체불", r"체불임금", r"미지급임금"]),
    ("산재", [r"산재", r"산업재해", r"업무상 재해", r"산재보험"]),
    ("성희롱", [r"성희롱", r"직장 내 성희롱"]),
    ("폭언/폭행", [r"폭언", r"폭행", r"폭행·폭언", r"폭언·폭행"]),
    ("횡령/배임", [r"횡령", r"배임"]),
    ("비위행위", [r"비위행위", r"비위", r"징계사유", r"품위손상"]),
    ("경영상해고", [r"경영상 해고", r"정리해고", r"경영상 이유"]),
    ("전보/인사이동", [r"전보", r"인사이동", r"인사발령", r"전직", r"배치전환"]),
    ("갱신기대권", [r"갱신기대권", r"계약갱신", r"갱신거절"]),
    ("해고부존재", [r"해고부존재", r"사직의사 없는", r"의원면직 취소"]),
    ("근로자성", [r"근로자성", r"근로자에 해당", r"사용종속관계"]),
    ("취업규칙", [r"취업규칙"]),
    ("퇴직금", [r"퇴직금", r"퇴직급여", r"퇴직급여보장"]),
    ("통상임금", [r"통상임금", r"평균임금"]),
    ("최저임금", [r"최저임금"]),
    ("연장근로", [r"연장근로", r"초과근로", r"시간외근로"]),
    ("휴게시간", [r"휴게시간"]),
    ("휴일근로", [r"휴일근로", r"주휴", r"휴일수당"]),
    ("연차휴가", [r"연차휴가", r"연차수당", r"유급휴가"]),
    ("기간제", [r"기간제", r"기간의 정함이 있는", r"무기계약직", r"계약직"]),
    ("수습", [r"수습", r"시용"]),
    ("본채용거부", [r"본채용거부", r"본채용 거부", r"채용거부"]),
    ("직장내괴롭힘", [r"직장내괴롭힘", r"직장 내 괴롭힘", r"괴롭힘"]),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tag lawgo_precedents with keywords_matched and duplicate mappings")
    parser.add_argument("--input", action="append", help="lawgo_precedents_ready.jsonl 경로. 여러 번 지정 가능")
    parser.add_argument("--bigcase-input", default=str(DEFAULT_BIGCASE_INPUT))
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--parse-version", default=DEFAULT_PARSE_VERSION)
    parser.add_argument("--output-dir", help="결과 출력 디렉터리")
    parser.add_argument("--apply-db", action="store_true", help="Supabase lawgo_precedents에 배치 업데이트")
    parser.add_argument("--limit", type=int, help="테스트용 제한")
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip())


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
        out = Path(path_arg)
    else:
        out = DEFAULT_OUTPUT_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    return out


def load_jsonl_rows(paths: list[Path], limit: int | None = None) -> list[dict[str, Any]]:
    rows_by_id: dict[str, dict[str, Any]] = {}
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            rows_by_id[row["id"]] = row
    rows = list(rows_by_id.values())
    rows.sort(key=lambda row: row["id"])
    if limit is not None:
        rows = rows[:limit]
    return rows


def load_bigcase_case_map(path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not path.exists():
        return mapping
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        case_number = normalize_case_number(str(row.get("case_number") or ""))
        if case_number and case_number not in mapping:
            mapping[case_number] = str(row.get("id") or "")
    return mapping


def normalize_case_number(value: str) -> str:
    return re.sub(r"\s+", "", value).strip()


def extract_estimated_year(reference_number: str | None) -> int | None:
    match = re.search(r"(19|20)\d{2}", str(reference_number or ""))
    if not match:
        return None
    return int(match.group(0))


def build_tag_patterns() -> list[tuple[str, list[re.Pattern[str]]]]:
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


def tag_row(
    row: dict[str, Any],
    bigcase_case_map: dict[str, str],
    compiled_rules: list[tuple[str, list[re.Pattern[str]]]],
) -> dict[str, Any]:
    combined_text = " ".join(
        str(row.get(field) or "") for field in ("title", "issue_text", "summary_text")
    )
    keywords_matched = match_keywords(combined_text, compiled_rules)
    case_number = normalize_case_number(str(row.get("reference_number") or ""))
    estimated_year = None
    decision_date = str(row.get("decision_date") or "")
    if decision_date == "00010101":
        estimated_year = extract_estimated_year(case_number)
        if estimated_year is not None:
            decision_date = f"{estimated_year}0101"

    tagged = dict(row)
    tagged["keywords_matched"] = keywords_matched
    tagged["decision_date"] = decision_date
    tagged["estimated_year"] = estimated_year
    tagged["bigcase_case_id"] = bigcase_case_map.get(case_number)
    return tagged


def build_update_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "api_id": row["api_id"],
        "keywords_matched": row.get("keywords_matched") or [],
        "decision_date": row.get("decision_date"),
        "estimated_year": row.get("estimated_year"),
        "bigcase_case_id": row.get("bigcase_case_id"),
    }


def chunk_rows(rows: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [rows[index:index + batch_size] for index in range(0, len(rows), batch_size)]


def post_batch(rows: list[dict[str, Any]]) -> None:
    supabase_url = require_env("SUPABASE_URL")
    response = requests.post(
        f"{supabase_url}/rest/v1/lawgo_precedents?on_conflict=api_id",
        headers=build_headers(),
        json=rows,
        timeout=120,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{response.status_code} {response.text[:1000]}")


def main() -> None:
    load_env_file()
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir)

    input_paths = [Path(path) for path in args.input] if args.input else DEFAULT_LAWGO_INPUTS
    bigcase_case_map = load_bigcase_case_map(Path(args.bigcase_input))
    compiled_rules = build_tag_patterns()

    raw_rows = load_jsonl_rows(input_paths, limit=args.limit)
    tagged_rows = [tag_row(row, bigcase_case_map, compiled_rules) for row in raw_rows]

    updates = [build_update_row(row) for row in tagged_rows]
    top_keywords = Counter(
        keyword
        for row in tagged_rows
        for keyword in row.get("keywords_matched") or []
    )

    tagged_path = output_dir / "lawgo_precedents_tagged.jsonl"
    updates_path = output_dir / "lawgo_precedents_updates.jsonl"
    duplicate_path = output_dir / "lawgo_bigcase_duplicates.jsonl"

    with tagged_path.open("w", encoding="utf-8") as handle:
        for row in tagged_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    with updates_path.open("w", encoding="utf-8") as handle:
        for row in updates:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    with duplicate_path.open("w", encoding="utf-8") as handle:
        for row in tagged_rows:
            if row.get("bigcase_case_id"):
                handle.write(
                    json.dumps(
                        {
                            "lawgo_id": row["id"],
                            "api_id": row["api_id"],
                            "reference_number": row.get("reference_number"),
                            "bigcase_case_id": row.get("bigcase_case_id"),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    db_status: dict[str, Any] = {"attempted": False}
    if args.apply_db:
        db_status["attempted"] = True
        try:
            for batch_index, batch in enumerate(chunk_rows(updates, args.batch_size), start=1):
                post_batch(batch)
                time.sleep(0.2)
            db_status["success"] = True
            db_status["updated_rows"] = len(updates)
        except Exception as exc:  # noqa: BLE001
            db_status["success"] = False
            db_status["error"] = str(exc)
    else:
        db_status["success"] = None

    report = {
        "input_count": len(raw_rows),
        "tagged_count": len(tagged_rows),
        "keywords_nonempty_count": sum(1 for row in tagged_rows if row.get("keywords_matched")),
        "decision_date_zero_count_before": sum(1 for row in raw_rows if str(row.get("decision_date") or "") == "00010101"),
        "decision_date_fixed_count": sum(1 for row in tagged_rows if row.get("estimated_year") is not None),
        "duplicate_bigcase_mapping_count": sum(1 for row in tagged_rows if row.get("bigcase_case_id")),
        "top_keywords": top_keywords.most_common(50),
        "input_paths": [str(path) for path in input_paths],
        "bigcase_input": str(Path(args.bigcase_input)),
        "tagged_path": str(tagged_path),
        "updates_path": str(updates_path),
        "duplicate_path": str(duplicate_path),
        "db_update": db_status,
        "batch_size": args.batch_size,
        "parse_version": args.parse_version,
    }

    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
