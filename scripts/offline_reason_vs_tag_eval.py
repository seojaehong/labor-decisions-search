import argparse
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Offline evaluation scaffold for reason_category vs 8-axis tags.")
    parser.add_argument(
        "--merged",
        default=r"C:\dev\labor-decisions-search\retagging\output\merged\merged_final_v1.jsonl",
    )
    parser.add_argument(
        "--queries",
        default=r"C:\dev\labor-decisions-search\retagging\evaluation\representative_queries_v1.json",
    )
    parser.add_argument(
        "--baseline-results",
        help="Optional JSON file keyed by query_id with baseline top-k case_ids exported from DB/service.",
    )
    parser.add_argument(
        "--output",
        default=r"C:\dev\labor-decisions-search\retagging\evaluation\offline_eval_run.md",
    )
    return parser.parse_args()


def load_jsonl(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def overlap_count(values, expected):
    actual = set(values or [])
    wanted = set(expected or [])
    return len(actual & wanted)


def score_candidate(record, profile):
    score = 0
    reasons = []

    if profile.get("employment_stage") and record.get("employment_stage") in profile["employment_stage"]:
        score += 4
        reasons.append("employment_stage")

    if profile.get("issue_type_primary") and record.get("issue_type_primary") in profile["issue_type_primary"]:
        score += 5
        reasons.append("issue_type_primary")

    secondary_hits = overlap_count(record.get("issue_type_secondary", []), profile.get("issue_type_secondary", []))
    if secondary_hits:
        score += secondary_hits * 2
        reasons.append(f"issue_type_secondary x{secondary_hits}")

    disposition_hits = overlap_count(record.get("disposition_type", []), profile.get("disposition_type", []))
    if disposition_hits:
        score += disposition_hits * 3
        reasons.append(f"disposition_type x{disposition_hits}")

    marker_hits = overlap_count(record.get("fact_markers", []), profile.get("fact_markers", []))
    if marker_hits:
        score += marker_hits * 2
        reasons.append(f"fact_markers x{marker_hits}")

    focus_hits = overlap_count(record.get("legal_focus", []), profile.get("legal_focus", []))
    if focus_hits:
        score += focus_hits * 2
        reasons.append(f"legal_focus x{focus_hits}")

    if profile.get("industry_context") and record.get("industry_context") in profile["industry_context"]:
        score += 1
        reasons.append("industry_context")

    exclusion_hits = overlap_count(record.get("exclusion_flags", []), profile.get("exclusion_flags", []))
    if exclusion_hits:
        score -= exclusion_hits * 3
        reasons.append(f"exclusion_penalty x{exclusion_hits}")

    query_text = " ".join(profile.get("query_hints", []))
    include_hits = sum(1 for phrase in record.get("include_for_queries", []) if phrase and phrase in query_text)
    exclude_hits = sum(1 for phrase in record.get("exclude_for_queries", []) if phrase and phrase in query_text)
    if include_hits:
        score += include_hits
        reasons.append(f"include_for_queries x{include_hits}")
    if exclude_hits:
        score -= exclude_hits * 2
        reasons.append(f"exclude_for_queries x{exclude_hits}")

    return score, reasons


def format_result_row(rank, record, reasons):
    title = record.get("case_name", "").replace("\n", " ").strip()
    return f"| {rank} | {record.get('case_id')} | {title} | {', '.join(reasons) or '-'} |  |  |\n"


def main():
    args = parse_args()
    merged_records = load_jsonl(Path(args.merged))
    queries = json.loads(Path(args.queries).read_text(encoding="utf-8"))

    baseline_results = {}
    if args.baseline_results:
        baseline_results = json.loads(Path(args.baseline_results).read_text(encoding="utf-8"))

    by_case_id = {record["case_id"]: record for record in merged_records}
    lines = ["# Offline Eval Run\n\n"]

    for query in queries:
        profile = dict(query["candidate_profile"])
        profile["query_hints"] = [query["query"]]

        scored = []
        for record in merged_records:
            score, reasons = score_candidate(record, profile)
            if score > 0:
                scored.append((score, record, reasons))

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1].get("issue_type_primary", ""),
                item[1].get("case_id", ""),
            )
        )
        top_candidate = scored[:5]

        lines.append(f"## {query['id']} — {query['query']}\n\n")
        lines.append(f"- query_type: `{query['query_type']}`\n")
        lines.append(f"- topic: `{query['topic']}`\n")
        lines.append(f"- baseline_reason_categories: `{', '.join(query['baseline_reason_categories'])}`\n")
        lines.append(f"- candidate_profile: `{json.dumps(query['candidate_profile'], ensure_ascii=False)}`\n\n")

        lines.append("### Baseline Top-5\n\n")
        lines.append("| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |\n")
        lines.append("|------|---------|-------|--------------|-------------------|------|\n")
        baseline_case_ids = baseline_results.get(query["id"], [])
        for idx in range(5):
            if idx < len(baseline_case_ids) and baseline_case_ids[idx] in by_case_id:
                record = by_case_id[baseline_case_ids[idx]]
                lines.append(format_result_row(idx + 1, record, ["baseline_export"]))
            else:
                lines.append(f"| {idx + 1} |  |  |  |  |  |\n")
        lines.append("\n")

        lines.append("### Candidate Top-5\n\n")
        lines.append("| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |\n")
        lines.append("|------|---------|-------|--------------|-------------------|------|\n")
        for idx in range(5):
            if idx < len(top_candidate):
                _, record, reasons = top_candidate[idx]
                lines.append(format_result_row(idx + 1, record, reasons))
            else:
                lines.append(f"| {idx + 1} |  |  |  |  |  |\n")
        lines.append("\n")

        lines.append("### Query Summary\n\n")
        lines.append("- baseline precision@5: \n")
        lines.append("- candidate precision@5: \n")
        lines.append("- baseline weighted relevance score@5: \n")
        lines.append("- candidate weighted relevance score@5: \n")
        lines.append("- baseline first relevant rank: \n")
        lines.append("- candidate first relevant rank: \n")
        lines.append("- win/loss/tie: \n")
        lines.append("- memo: \n\n")

    Path(args.output).write_text("".join(lines), encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
