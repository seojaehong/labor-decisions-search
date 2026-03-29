from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).parent.parent
DEFAULT_BATCH_SIZE = 50


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upsert law.go.kr precedents/documents into Supabase")
    parser.add_argument("--precedents", required=True, help="lawgo_precedents_ready.jsonl 경로")
    parser.add_argument("--documents", required=True, help="lawgo_precedent_documents_ready.jsonl 경로")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--dry-run", action="store_true")
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
        raise SystemExit(f"Error: {name} must be set")
    return value


def build_headers() -> dict[str, str]:
    service_key = require_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def check_table_exists(table: str) -> None:
    supabase_url = require_env("SUPABASE_URL")
    response = requests.get(
        f"{supabase_url}/rest/v1/{table}",
        headers=build_headers(),
        params={"select": "*", "limit": "1"},
        timeout=60,
    )
    if response.status_code == 404:
        raise SystemExit(
            f"Error: table {table} does not exist. Run the lawgo table SQL in supabase_schema.sql first."
        )
    response.raise_for_status()


def post_batch(table: str, rows: list[dict[str, Any]], on_conflict: str) -> None:
    supabase_url = require_env("SUPABASE_URL")
    response = requests.post(
        f"{supabase_url}/rest/v1/{table}?on_conflict={on_conflict}",
        headers=build_headers(),
        json=rows,
        timeout=120,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{table}: {response.status_code} {response.text[:1000]}")


def batched(rows: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [rows[index:index + batch_size] for index in range(0, len(rows), batch_size)]


def fetch_count(table: str) -> int:
    supabase_url = require_env("SUPABASE_URL")
    response = requests.get(
        f"{supabase_url}/rest/v1/{table}",
        headers={**build_headers(), "Prefer": "count=exact"},
        params={"select": "id", "limit": "1"},
        timeout=60,
    )
    response.raise_for_status()
    content_range = response.headers.get("Content-Range", "")
    if "/" in content_range:
        return int(content_range.split("/")[-1])
    return 0


def main() -> None:
    load_env_file()
    args = parse_args()

    precedents_rows = load_jsonl(Path(args.precedents))
    documents_rows = load_jsonl(Path(args.documents))

    if args.dry_run:
        print(json.dumps({
            "precedents": len(precedents_rows),
            "documents": len(documents_rows),
            "dry_run": True,
        }, ensure_ascii=False, indent=2))
        return

    check_table_exists("lawgo_precedents")
    check_table_exists("lawgo_precedent_documents")

    for batch in batched(precedents_rows, args.batch_size):
        post_batch("lawgo_precedents", batch, "api_id")
    for batch in batched(documents_rows, args.batch_size):
        post_batch("lawgo_precedent_documents", batch, "precedent_id,parse_version")

    print(json.dumps({
        "precedents_uploaded": len(precedents_rows),
        "documents_uploaded": len(documents_rows),
        "lawgo_precedents_count": fetch_count("lawgo_precedents"),
        "lawgo_precedent_documents_count": fetch_count("lawgo_precedent_documents"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
