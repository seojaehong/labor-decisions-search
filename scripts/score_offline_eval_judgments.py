import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Score completed human judgments for offline eval package.")
    parser.add_argument(
        "--judgment-csv",
        default=r"C:\dev\labor-decisions-search\retagging\evaluation\dry_run_24q\24q_human_judgment_template.csv",
    )
    parser.add_argument(
        "--blind-key",
        default=r"C:\dev\labor-decisions-search\retagging\evaluation\dry_run_24q\24q_blind_key.json",
    )
    parser.add_argument(
        "--output",
        default=r"C:\dev\labor-decisions-search\retagging\evaluation\dry_run_24q\24q_scored_summary.md",
    )
    return parser.parse_args()


def precision_at_5(rows):
    return round(sum(1 for row in rows if row["rel"] >= 1) / 5, 3)


def weighted_score_at_5(rows):
    return sum(row["rel"] for row in rows)


def first_relevant_rank(rows):
    for row in rows:
        if row["rel"] >= 1:
            return row["rank"]
    return "NR"


def compare_systems(a, b):
    if a["weighted_score_at_5"] != b["weighted_score_at_5"]:
        return "A" if a["weighted_score_at_5"] > b["weighted_score_at_5"] else "B"
    if a["precision_at_5"] != b["precision_at_5"]:
        return "A" if a["precision_at_5"] > b["precision_at_5"] else "B"
    if a["first_relevant_rank"] == "NR" and b["first_relevant_rank"] == "NR":
        return "tie"
    if a["first_relevant_rank"] == "NR":
        return "B"
    if b["first_relevant_rank"] == "NR":
        return "A"
    if a["first_relevant_rank"] != b["first_relevant_rank"]:
        return "A" if a["first_relevant_rank"] < b["first_relevant_rank"] else "B"
    return "tie"


def main():
    args = parse_args()
    blind_key = json.loads(Path(args.blind_key).read_text(encoding="utf-8"))
    grouped = defaultdict(list)

    with open(args.judgment_csv, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row["case_id"]:
                continue
            try:
                rel = int(row["relevance"]) if row["relevance"] != "" else None
            except ValueError:
                rel = None
            grouped[(row["query_id"], row["blind_system"])].append(
                {
                    "rank": int(row["rank"]),
                    "rel": rel,
                    "case_id": row["case_id"],
                }
            )

    lines = ["# Offline Eval Scored Summary\n\n"]
    lines.append("| query_id | A actual | B actual | A p@5 | B p@5 | A wrs@5 | B wrs@5 | A FRR | B FRR | outcome |\n")
    lines.append("|----------|----------|----------|-------|-------|----------|----------|-------|-------|---------|\n")

    for query_id in sorted({key[0] for key in grouped}):
        if not grouped[(query_id, "A")] or not grouped[(query_id, "B")]:
            continue
        if any(row["rel"] is None for row in grouped[(query_id, "A")] + grouped[(query_id, "B")]):
            continue

        a_rows = sorted(grouped[(query_id, "A")], key=lambda row: row["rank"])
        b_rows = sorted(grouped[(query_id, "B")], key=lambda row: row["rank"])
        a_metrics = {
            "precision_at_5": precision_at_5(a_rows),
            "weighted_score_at_5": weighted_score_at_5(a_rows),
            "first_relevant_rank": first_relevant_rank(a_rows),
        }
        b_metrics = {
            "precision_at_5": precision_at_5(b_rows),
            "weighted_score_at_5": weighted_score_at_5(b_rows),
            "first_relevant_rank": first_relevant_rank(b_rows),
        }
        outcome = compare_systems(a_metrics, b_metrics)
        lines.append(
            "| {qid} | {aa} | {ba} | {ap} | {bp} | {aw} | {bw} | {af} | {bf} | {outcome} |\n".format(
                qid=query_id,
                aa=blind_key[query_id]["A"],
                ba=blind_key[query_id]["B"],
                ap=a_metrics["precision_at_5"],
                bp=b_metrics["precision_at_5"],
                aw=a_metrics["weighted_score_at_5"],
                bw=b_metrics["weighted_score_at_5"],
                af=a_metrics["first_relevant_rank"],
                bf=b_metrics["first_relevant_rank"],
                outcome=outcome,
            )
        )

    Path(args.output).write_text("".join(lines), encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
