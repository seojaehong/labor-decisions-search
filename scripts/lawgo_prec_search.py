from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).parent.parent
OUTPUT_DIR = REPO_DIR / "evaluation" / "lawgo" / "prec_search"
API_URL = "https://www.law.go.kr/DRF/lawSearch.do"
DEFAULT_QUERIES = [
    "근로기준법",
    "근로기준",
    "근로자퇴직급여보장법",
    "퇴직급여보장법",
    "남녀고용평등과 일·가정 양립 지원에 관한 법률",
    "남녀고용평등법",
    "산업재해보상보험법",
    "산재보험법",
    "노동조합 및 노동관계조정법",
    "노조법",
    "기간제 및 단시간근로자 보호 등에 관한 법률",
    "기간제법",
    "최저임금법",
    "최저임금",
    "산업안전보건법",
    "산업안전보건",
    "고용보험법",
    "파견근로자보호 등에 관한 법률",
    "파견근로자보호법",
    "고용상 연령차별금지 및 고령자고용촉진에 관한 법률",
    "직업안정법",
    "외국인근로자의 고용 등에 관한 법률",
    "임금채권보장법",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search law.go.kr precedent list API by labor-law anchors")
    parser.add_argument("--query", dest="queries", action="append", help="검색 키워드. 여러 번 지정 가능")
    parser.add_argument("--query-file", help="검색어 목록 파일")
    parser.add_argument("--oc", help="법제처 Open API OC 값. 미지정 시 LAWGO_OC 또는 OC 환경변수 사용")
    parser.add_argument("--display", type=int, default=100)
    parser.add_argument("--limit-pages", type=int, default=0, help="키워드당 최대 페이지 수 제한")
    parser.add_argument("--survey-only", action="store_true", help="키워드당 1페이지만 조회하고 totalCnt만 집계")
    parser.add_argument("--timeout", type=int, default=60)
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


def require_oc(explicit: str | None) -> str:
    value = explicit or os.environ.get("LAWGO_OC") or os.environ.get("OC")
    if not value:
        raise SystemExit("Error: --oc or LAWGO_OC/OC environment variable must be set")
    return value


def load_queries(args: argparse.Namespace) -> list[str]:
    values: list[str] = []
    if args.queries:
        values.extend(args.queries)
    if args.query_file:
        values.extend(
            line.strip()
            for line in Path(args.query_file).read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    if not values:
        values = list(DEFAULT_QUERIES)

    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def fetch_page(oc_value: str, query: str, page: int, display: int, timeout: int) -> dict[str, Any]:
    response = requests.get(
        API_URL,
        params={
            "OC": oc_value,
            "target": "prec",
            "type": "JSON",
            "query": query,
            "display": str(display),
            "page": str(page),
        },
        timeout=timeout,
    )
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.json()


def normalize_item(query: str, item: dict[str, Any]) -> dict[str, Any]:
    detail_link = item.get("판례상세링크") or ""
    return {
        "query": query,
        "source_provider": "lawgo",
        "source_kind": "case",
        "api_id": str(item.get("판례일련번호") or ""),
        "title": str(item.get("사건명") or "").strip(),
        "reference_number": str(item.get("사건번호") or "").strip(),
        "decision_date": str(item.get("선고일자") or "").strip(),
        "court": str(item.get("법원명") or "").strip(),
        "court_type_code": str(item.get("법원종류코드") or "").strip(),
        "case_type_name": str(item.get("사건종류명") or "").strip(),
        "case_type_code": str(item.get("사건종류코드") or "").strip(),
        "judgment_type": str(item.get("판결유형") or "").strip(),
        "data_source_name": str(item.get("데이터출처명") or "").strip(),
        "detail_link": f"https://www.law.go.kr{detail_link}" if detail_link else "",
    }


def coerce_prec_items(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def main() -> None:
    load_env_file()
    args = parse_args()
    oc_value = require_oc(args.oc)
    queries = load_queries(args)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []
    unique_ids: set[str] = set()

    for index, query in enumerate(queries, start=1):
        first_payload = fetch_page(oc_value, query, 1, args.display, args.timeout)
        data = first_payload.get("PrecSearch", {})
        total_count = int(str(data.get("totalCnt") or "0"))
        pages = max(1, math.ceil(total_count / args.display)) if total_count else 1
        if args.limit_pages > 0:
            pages = min(pages, args.limit_pages)
        if args.survey_only:
            pages = 1

        items = coerce_prec_items(data.get("prec"))
        summary = {
            "query": query,
            "total_count": total_count,
            "pages": pages,
            "first_page_count": len(items),
        }
        summary_rows.append(summary)

        for item in items:
            row = normalize_item(query, item)
            all_rows.append(row)
            if row["api_id"]:
                unique_ids.add(row["api_id"])

        for page in range(2, pages + 1):
            payload = fetch_page(oc_value, query, page, args.display, args.timeout)
            page_items = coerce_prec_items(payload.get("PrecSearch", {}).get("prec"))
            for item in page_items:
                row = normalize_item(query, item)
                all_rows.append(row)
                if row["api_id"]:
                    unique_ids.add(row["api_id"])
        print(f"{index}/{len(queries)} done: {query} (total={total_count}, pages={pages})")

    summary_path = run_dir / "query_summary.json"
    summary_path.write_text(json.dumps(summary_rows, ensure_ascii=False, indent=2), encoding="utf-8")

    rows_path = run_dir / "search_results.jsonl"
    with rows_path.open("w", encoding="utf-8") as handle:
        for row in all_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    unique_ids_path = run_dir / "unique_prec_ids.txt"
    unique_ids_path.write_text("\n".join(sorted(unique_ids)), encoding="utf-8")

    report = {
        "query_count": len(queries),
        "raw_result_count": len(all_rows),
        "unique_prec_id_count": len(unique_ids),
        "survey_only": args.survey_only,
        "display": args.display,
        "summary_path": str(summary_path),
        "rows_path": str(rows_path),
        "unique_ids_path": str(unique_ids_path),
    }
    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
