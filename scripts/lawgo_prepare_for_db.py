from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_DIR = Path(__file__).parent.parent
OUTPUT_DIR = REPO_DIR / "evaluation" / "lawgo" / "db_ready"
DEFAULT_PARSE_VERSION = "lawgo-prec-v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare law.go.kr precedent JSONL for DB upsert")
    parser.add_argument("--input", required=True, help="lawgo_cases_ready.jsonl 또는 results.jsonl 경로")
    parser.add_argument("--parse-version", default=DEFAULT_PARSE_VERSION)
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("error"):
            continue
        rows.append(row)
    return rows


def build_source_url(api_id: str) -> str:
    return f"https://www.law.go.kr/DRF/lawService.do?target=prec&ID={api_id}&type=HTML"


def normalize_precedent(row: dict[str, Any]) -> dict[str, Any]:
    api_id = str(row.get("api_id") or row.get("source_id") or "").strip()
    precedent_id = f"prec_{api_id}"
    created_at = datetime.now(timezone.utc).isoformat()
    return {
        "id": precedent_id,
        "api_id": api_id,
        "title": row.get("title") or "",
        "reference_number": row.get("reference_number") or None,
        "decision_date": row.get("decision_date") or None,
        "court": row.get("court") or None,
        "court_type_code": row.get("court_type_code") or None,
        "case_type_name": row.get("case_type_name") or None,
        "case_type_code": row.get("case_type_code") or None,
        "judgment_type": row.get("judgment_type") or None,
        "issue_text": row.get("issue_text") or None,
        "summary_text": row.get("summary_text") or None,
        "reference_statutes": row.get("reference_statutes") or None,
        "reference_cases": row.get("reference_cases") or None,
        "source_url": build_source_url(api_id),
        "source_provider": "lawgo",
        "created_at": created_at,
    }


def normalize_document(row: dict[str, Any], parse_version: str) -> dict[str, Any]:
    api_id = str(row.get("api_id") or row.get("source_id") or "").strip()
    body_text = row.get("body_text") or ""
    return {
        "precedent_id": f"prec_{api_id}",
        "body_text": body_text,
        "body_sections": row.get("body_sections") or None,
        "body_length": int(row.get("body_length") or len(body_text)),
        "parse_version": parse_version,
        "content_hash": hashlib.md5(body_text.encode("utf-8", errors="replace")).hexdigest(),
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    rows = load_rows(input_path)

    precedents: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    seen_api_ids: set[str] = set()

    for row in rows:
        api_id = str(row.get("api_id") or row.get("source_id") or "").strip()
        if not api_id:
            continue
        if api_id not in seen_api_ids:
            precedents.append(normalize_precedent(row))
            seen_api_ids.add(api_id)
        documents.append(normalize_document(row, args.parse_version))

    run_dir = OUTPUT_DIR / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    precedents_path = run_dir / "lawgo_precedents_ready.jsonl"
    with precedents_path.open("w", encoding="utf-8") as handle:
        for row in precedents:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    documents_path = run_dir / "lawgo_precedent_documents_ready.jsonl"
    with documents_path.open("w", encoding="utf-8") as handle:
        for row in documents:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    report = {
        "input_path": str(input_path),
        "precedent_count": len(precedents),
        "document_count": len(documents),
        "precedents_path": str(precedents_path),
        "documents_path": str(documents_path),
        "parse_version": args.parse_version,
    }
    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
