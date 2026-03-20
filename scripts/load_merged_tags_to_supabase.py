"""
merged_final_v1.jsonl -> nlrc_decisions candidate tag columns update

기본은 dry-run이며, apply 모드에서만 실제 업데이트한다.

사용 예:
  python scripts/load_merged_tags_to_supabase.py --dry-run
  python scripts/load_merged_tags_to_supabase.py --limit 20 --dry-run
  python scripts/load_merged_tags_to_supabase.py --apply
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from supabase import create_client


DEFAULT_INPUT = Path(r"C:\dev\labor-decisions-search\retagging\output\merged\merged_final_v1.jsonl")
DEFAULT_REPORT = Path(r"C:\dev\labor-decisions-search\retagging\implementation\load_merged_tags_report.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load merged retag payload into nlrc_decisions.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check-existing", action="store_true")
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument(
        "--target-table",
        default="nlrc_decisions",
        choices=["nlrc_decisions", "nlrc_decision_tag_candidates"],
    )
    parser.add_argument("--source-basis", default="retagging/output/merged/merged_final_v1.jsonl")
    parser.add_argument("--snapshot-version", default="merged_final_v1")
    return parser.parse_args()


def get_supabase_client():
    url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("Supabase env vars are required: NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
    return create_client(url, key)


def load_jsonl(path: Path, limit: int | None = None) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
            if limit and len(rows) >= limit:
                break
    return rows


def build_update_payload(
    row: dict,
    source_basis: str,
    snapshot_version: str,
    loaded_at: str,
    target_table: str,
) -> dict:
    payload = {
        "summary_short": row.get("summary_short"),
        "holding_summary": row.get("holding_summary"),
        "retrieval_note": row.get("retrieval_note"),
        "employment_stage": row.get("employment_stage"),
        "issue_type_primary": row.get("issue_type_primary"),
        "issue_type_secondary": row.get("issue_type_secondary") or [],
        "disposition_type": row.get("disposition_type") or [],
        "fact_markers": row.get("fact_markers") or [],
        "legal_focus": row.get("legal_focus") or [],
        "industry_context": row.get("industry_context"),
        "exclusion_flags": row.get("exclusion_flags") or [],
        "include_for_queries": row.get("include_for_queries") or [],
        "exclude_for_queries": row.get("exclude_for_queries") or [],
        "tag_confidence": row.get("confidence"),
        "retag_notes": row.get("notes"),
        "retag_version": row.get("tag_version"),
        "review_status": row.get("review_status"),
        "retag_source_basis": source_basis,
        "retag_snapshot_version": snapshot_version,
        "retag_loaded_at": loaded_at,
        "retag_payload": row,
    }
    if target_table == "nlrc_decisions":
        payload["tag_search_enabled"] = True
    else:
        payload["case_id"] = row["case_id"]
        payload["source_decision_id"] = row["case_id"]
        payload["promoted_to_live"] = False
    return payload


def write_report(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    rows = load_jsonl(input_path, limit=args.limit)
    loaded_at = datetime.now(timezone.utc).isoformat()

    lines = ["# Load Merged Tags Report\n\n"]
    lines.append(f"- input: `{input_path}`\n")
    lines.append(f"- rows read: `{len(rows)}`\n")
    lines.append(f"- mode: `{'apply' if args.apply else 'dry-run'}`\n")
    lines.append(f"- target table: `{args.target_table}`\n")
    lines.append(f"- snapshot version: `{args.snapshot_version}`\n\n")

    primary_counts = Counter(row.get("issue_type_primary", "unknown") for row in rows)
    lines.append("## Primary Distribution\n\n")
    for key, count in primary_counts.most_common(10):
        lines.append(f"- `{key}`: `{count}`\n")
    lines.append("\n")

    sample = rows[:3]
    lines.append("## Sample Mapping\n\n")
    for row in sample:
        payload = build_update_payload(row, args.source_basis, args.snapshot_version, loaded_at, args.target_table)
        lines.append(f"- `{row['case_id']}` -> primary `{payload['issue_type_primary']}`, stage `{payload['employment_stage']}`\n")
    lines.append("\n")

    if args.dry_run or not args.apply:
        if args.check_existing and args.target_table == "nlrc_decisions":
            lines.append("## Existing ID Check\n\n")
            try:
                client = get_supabase_client()
                existing_count = 0
                missing = []
                for row in rows:
                    case_id = row["case_id"]
                    existing = client.table("nlrc_decisions").select("id").eq("id", case_id).limit(1).execute()
                    if existing.data:
                        existing_count += 1
                    else:
                        missing.append(case_id)
                lines.append(f"- existing rows in target: `{existing_count}`\n")
                lines.append(f"- missing ids: `{len(missing)}`\n")
                for case_id in missing[:20]:
                    lines.append(f"- missing: `{case_id}`\n")
            except Exception as exc:
                lines.append(f"- existing check unavailable: `{exc}`\n")
            lines.append("\n")
        lines.append("## Dry-Run Result\n\n")
        lines.append("- no DB writes executed\n")
        lines.append("- rerun safe: `yes` (same snapshot payload can be re-applied)\n")
        write_report(Path(args.report), lines)
        print(f"wrote {args.report}")
        return

    client = get_supabase_client()
    updated = 0
    missing = []

    if args.target_table == "nlrc_decisions":
        for row in rows:
            case_id = row["case_id"]
            payload = build_update_payload(row, args.source_basis, args.snapshot_version, loaded_at, args.target_table)

            existing = client.table("nlrc_decisions").select("id").eq("id", case_id).limit(1).execute()
            if not existing.data:
                missing.append(case_id)
                continue

            client.table("nlrc_decisions").update(payload).eq("id", case_id).execute()
            updated += 1
    else:
        for row in rows:
            payload = build_update_payload(row, args.source_basis, args.snapshot_version, loaded_at, args.target_table)
            client.table(args.target_table).upsert(payload).execute()
            updated += 1

    lines.append("## Apply Result\n\n")
    lines.append(f"- updated rows: `{updated}`\n")
    lines.append(f"- missing ids: `{len(missing)}`\n")
    lines.append("- rerun safe: `yes`\n")
    if missing:
        for case_id in missing[:20]:
            lines.append(f"- missing: `{case_id}`\n")

    write_report(Path(args.report), lines)
    print(f"wrote {args.report}")
    if missing and args.fail_on_missing:
        raise RuntimeError(f"missing case_id count: {len(missing)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise
