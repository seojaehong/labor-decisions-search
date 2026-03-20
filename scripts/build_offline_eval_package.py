import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"[가-힣A-Za-z0-9_]+")


def parse_args():
    parser = argparse.ArgumentParser(description="Build blind dry-run evaluation package for baseline vs candidate.")
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
        default=r"C:\dev\labor-decisions-search\retagging\evaluation\baseline_results.json",
    )
    parser.add_argument(
        "--output-dir",
        default=r"C:\dev\labor-decisions-search\retagging\evaluation\dry_run_24q",
    )
    return parser.parse_args()


def tokenize(text):
    text = text or ""
    tokens = [m.group(0).lower() for m in TOKEN_RE.finditer(text)]
    return [t for t in tokens if len(t) >= 2]


def load_jsonl(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def derive_reason_categories(record):
    categories = set()
    primary = record.get("issue_type_primary")
    secondary = set(record.get("issue_type_secondary", []))
    dispositions = set(record.get("disposition_type", []))
    summary = record.get("holding_summary", "") or ""
    notes = record.get("notes", "") or ""
    text = f"{summary} {notes} {' '.join(record.get('include_for_queries', []))} {' '.join(record.get('exclude_for_queries', []))}"

    if primary in {"absence_without_leave", "attendance"} or "unauthorized_absence" in record.get("fact_markers", []):
        categories.add("absence")
    if primary in {"work_ability", "performance", "low_sales"}:
        categories.add("incompetence")
    if primary in {"workplace_harassment", "harassment_report", "harassment_investigation", "retaliation"}:
        categories.add("workplace_bullying")
    if primary == "transfer_validity" or "transfer" in dispositions:
        categories.add("transfer")
    if primary == "renewal_expectation" or "contract_termination" in dispositions or "nonrenewal" in dispositions:
        categories.add("contract_expiry")
    if primary == "worker_status":
        categories.add("worker_status")
    if primary == "discrimination":
        categories.add("discrimination")
    if primary == "redundancy":
        categories.add("redundancy")
    if record.get("employment_stage") == "probation" or dispositions & {"rejection_of_regular_employment", "probation_termination"}:
        categories.add("probation")
    if primary in {"misconduct", "disciplinary_severity", "procedure", "dismissal_validity", "unfair_treatment"}:
        if any(token in text for token in ["폭행", "폭언", "욕설", "폭력", "가혹행위", "모욕"]):
            categories.add("violence")
        if any(token in text for token in ["성희롱", "성추행", "성적 언동", "성폭력"]):
            categories.add("sexual_harassment")
        if any(token in text for token in ["횡령", "배임", "공금", "유용", "착복"]):
            categories.add("embezzlement")
        if any(token in text for token in ["부당노동행위", "노조", "지배개입", "불이익취급"]):
            categories.add("union_activity")
        if any(token in text for token in ["사직", "권고사직", "합의퇴직", "퇴직", "퇴사"]):
            categories.add("no_dismissal")
        if not categories & {"violence", "sexual_harassment", "embezzlement"} and primary == "misconduct":
            categories.add("misconduct")
    if not categories:
        categories.add("other")
    return sorted(categories)


def text_overlap_score(query_text, record):
    haystack = " ".join(
        [
            record.get("case_name", ""),
            record.get("summary_short", ""),
            record.get("holding_summary", ""),
            record.get("retrieval_note", ""),
            " ".join(record.get("include_for_queries", [])),
        ]
    ).lower()
    q_tokens = tokenize(query_text)
    return sum(1 for token in q_tokens if token in haystack)


def baseline_score(query, record, pseudo_categories):
    score = 0
    reasons = []
    overlap = set(query["baseline_reason_categories"]) & set(pseudo_categories)
    if overlap:
        score += len(overlap) * 8
        reasons.append(f"reason_category overlap: {', '.join(sorted(overlap))}")

    text_hits = text_overlap_score(query["query"], record)
    if text_hits:
        score += min(text_hits, 4)
        reasons.append(f"text overlap x{text_hits}")

    if query["topic"] == "workplace_bullying" and "not_really_harassment_case" in record.get("exclusion_flags", []):
        score -= 3
        reasons.append("background harassment penalty")
    if query["topic"] == "absence" and "not_really_absence_case" in record.get("exclusion_flags", []):
        score -= 3
        reasons.append("background absence penalty")

    return score, reasons


def candidate_score(query, record):
    profile = query["candidate_profile"]
    score = 0
    reasons = []

    if profile.get("employment_stage") and record.get("employment_stage") in profile["employment_stage"]:
        score += 5
        reasons.append("employment_stage")
    if profile.get("issue_type_primary") and record.get("issue_type_primary") in profile["issue_type_primary"]:
        score += 6
        reasons.append("issue_type_primary")

    secondary_hits = len(set(profile.get("issue_type_secondary", [])) & set(record.get("issue_type_secondary", [])))
    if secondary_hits:
        score += secondary_hits * 3
        reasons.append(f"issue_type_secondary x{secondary_hits}")

    disposition_hits = len(set(profile.get("disposition_type", [])) & set(record.get("disposition_type", [])))
    if disposition_hits:
        score += disposition_hits * 4
        reasons.append(f"disposition_type x{disposition_hits}")

    marker_hits = len(set(profile.get("fact_markers", [])) & set(record.get("fact_markers", [])))
    if marker_hits:
        score += marker_hits * 3
        reasons.append(f"fact_markers x{marker_hits}")

    focus_hits = len(set(profile.get("legal_focus", [])) & set(record.get("legal_focus", [])))
    if focus_hits:
        score += focus_hits * 3
        reasons.append(f"legal_focus x{focus_hits}")

    if profile.get("industry_context") and record.get("industry_context") in profile["industry_context"]:
        score += 2
        reasons.append("industry_context")

    exclusion_hits = len(set(profile.get("exclusion_flags", [])) & set(record.get("exclusion_flags", [])))
    if exclusion_hits:
        score -= exclusion_hits * 4
        reasons.append(f"exclusion_penalty x{exclusion_hits}")

    text_hits = text_overlap_score(query["query"], record)
    if text_hits:
        score += min(text_hits, 4)
        reasons.append(f"text overlap x{text_hits}")

    return score, reasons


def rank_records(query, records):
    baseline_ranked = []
    candidate_ranked = []
    for record in records:
        pseudo_categories = derive_reason_categories(record)
        b_score, b_reasons = baseline_score(query, record, pseudo_categories)
        if b_score > 0:
            baseline_ranked.append(
                {
                    "score": b_score,
                    "why": b_reasons,
                    "pseudo_reason_categories": pseudo_categories,
                    "record": record,
                }
            )
        c_score, c_reasons = candidate_score(query, record)
        if c_score > 0:
            candidate_ranked.append(
                {
                    "score": c_score,
                    "why": c_reasons,
                    "pseudo_reason_categories": pseudo_categories,
                    "record": record,
                }
            )

    sort_key = lambda item: (
        -item["score"],
        -text_overlap_score(query["query"], item["record"]),
        item["record"].get("issue_type_primary", ""),
        item["record"].get("case_id", ""),
    )
    baseline_ranked.sort(key=sort_key)
    candidate_ranked.sort(key=sort_key)
    return baseline_ranked[:5], candidate_ranked[:5]


def diversity_ratio(rows):
    if not rows:
        return 0.0
    unique_primary = len({row["record"].get("issue_type_primary") for row in rows})
    return round(unique_primary / len(rows), 3)


def top1_overlap(baseline_rows, candidate_rows):
    if not baseline_rows or not candidate_rows:
        return 0
    return int(baseline_rows[0]["record"]["case_id"] == candidate_rows[0]["record"]["case_id"])


def result_diversity_ratio(result_lists):
    flattened = [row["record"]["case_id"] for rows in result_lists for row in rows]
    if not flattened:
        return 0.0
    return round(len(set(flattened)) / len(flattened), 3)


def top1_duplicate_rate(result_lists):
    top1_ids = [rows[0]["record"]["case_id"] for rows in result_lists if rows]
    if not top1_ids:
        return 0.0
    return round((len(top1_ids) - len(set(top1_ids))) / len(top1_ids), 3)


def format_result_table(rows):
    lines = [
        "| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |\n",
        "|------|---------|-------|---------|-------|-------------|--------------|-----------|------|\n",
    ]
    for idx in range(5):
        if idx < len(rows):
            row = rows[idx]
            record = row["record"]
            lines.append(
                "| {rank} | {case_id} | {title} | {primary} | {stage} | {disp} | {why} |  |  |\n".format(
                    rank=idx + 1,
                    case_id=record.get("case_id", ""),
                    title=(record.get("case_name", "") or "").replace("\n", " "),
                    primary=record.get("issue_type_primary", ""),
                    stage=record.get("employment_stage", ""),
                    disp=", ".join(record.get("disposition_type", [])),
                    why=", ".join(row["why"]) or "-",
                )
            )
        else:
            lines.append(f"| {idx + 1} |  |  |  |  |  |  |  |  |\n")
    return "".join(lines)


def stable_blind_order(query_id):
    digest = hashlib.sha256(query_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 2


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "query_id",
                "query",
                "blind_system",
                "rank",
                "case_id",
                "title",
                "primary",
                "employment_stage",
                "disposition_type",
                "why_surfaced",
                "relevance",
                "memo",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    args = parse_args()
    merged = load_jsonl(Path(args.merged))
    queries = json.loads(Path(args.queries).read_text(encoding="utf-8"))
    baseline_results = {}
    baseline_path = Path(args.baseline_results)
    if baseline_path.exists():
        baseline_results = json.loads(baseline_path.read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    by_case_id = {record["case_id"]: record for record in merged}

    comparison_data = []
    blind_key = {}
    judgment_rows = []
    all_baseline_rows = []
    all_candidate_rows = []

    blind_lines = ["# 24-Query Blind Side-by-Side Package\n\n"]
    nonblind_lines = ["# 24-Query Non-Blind Top Results\n\n"]
    metric_lines = [
        "# 24-Query Pre-Judgment Metrics\n\n",
        "주의: `precision@5`, `weighted relevance score@5`, `first relevant rank`, `win/loss/tie`는 사람 relevance 입력 후 확정한다.\n",
        "이 문서의 수치는 dry-run 단계에서 자동 계산 가능한 지표만 포함한다.\n\n",
        "| query_id | topic | baseline diversity ratio | candidate diversity ratio | top-1 overlap | baseline top1 case | candidate top1 case |\n",
        "|----------|-------|--------------------------|---------------------------|---------------|--------------------|---------------------|\n",
    ]

    top1_overlap_sum = 0

    for query in queries:
        _, candidate_rows = rank_records(query, merged)
        baseline_rows = []
        for case_id in baseline_results.get(query["id"], [])[:5]:
            record = by_case_id.get(case_id)
            if not record:
                continue
            baseline_rows.append(
                {
                    "score": 0,
                    "why": ["baseline_export"],
                    "pseudo_reason_categories": derive_reason_categories(record),
                    "record": record,
                }
            )
        if not baseline_rows:
            baseline_rows, _ = rank_records(query, merged)

        b_div = diversity_ratio(baseline_rows)
        c_div = diversity_ratio(candidate_rows)
        overlap = top1_overlap(baseline_rows, candidate_rows)
        top1_overlap_sum += overlap
        all_baseline_rows.append(baseline_rows)
        all_candidate_rows.append(candidate_rows)

        blind_swap = stable_blind_order(query["id"])
        system_a_rows, system_b_rows = (
            (candidate_rows, baseline_rows) if blind_swap else (baseline_rows, candidate_rows)
        )
        system_a_name, system_b_name = (
            ("candidate", "baseline") if blind_swap else ("baseline", "candidate")
        )
        blind_key[query["id"]] = {"A": system_a_name, "B": system_b_name}

        comparison_data.append(
            {
                "query": query,
                "baseline": baseline_rows,
                "candidate": candidate_rows,
                "blind_mapping": blind_key[query["id"]],
                "pre_metrics": {
                    "baseline_diversity_ratio": b_div,
                    "candidate_diversity_ratio": c_div,
                    "top1_overlap": overlap,
                    "baseline_top1_case_id": baseline_rows[0]["record"]["case_id"] if baseline_rows else None,
                    "candidate_top1_case_id": candidate_rows[0]["record"]["case_id"] if candidate_rows else None,
                    "weighted_score_at_5": "TBD_after_human_judgment",
                    "precision_at_5": "TBD_after_human_judgment",
                    "first_relevant_rank": "TBD_after_human_judgment",
                    "win_loss_tie": "TBD_after_human_judgment",
                },
            }
        )

        blind_lines.append(f"## {query['id']} — {query['query']}\n\n")
        blind_lines.append(f"- topic: `{query['topic']}`\n")
        blind_lines.append(f"- query_type: `{query['query_type']}`\n")
        blind_lines.append(f"- evaluator task: 각 결과에 relevance `2/1/0` 부여\n\n")
        blind_lines.append("### System A\n\n")
        blind_lines.append(format_result_table(system_a_rows))
        blind_lines.append("\n### System B\n\n")
        blind_lines.append(format_result_table(system_b_rows))
        blind_lines.append(
            "\n### Query-level Scorecard\n\n"
            "- System A precision@5: \n"
            "- System B precision@5: \n"
            "- System A weighted relevance score@5: \n"
            "- System B weighted relevance score@5: \n"
            "- System A first relevant rank: \n"
            "- System B first relevant rank: \n"
            "- win/loss/tie: \n"
            "- memo: \n\n"
        )

        nonblind_lines.append(f"## {query['id']} — {query['query']}\n\n")
        nonblind_lines.append(f"- baseline_reason_categories: `{', '.join(query['baseline_reason_categories'])}`\n")
        nonblind_lines.append(f"- candidate_profile: `{json.dumps(query['candidate_profile'], ensure_ascii=False)}`\n")
        nonblind_lines.append(f"- baseline diversity ratio: `{b_div}`\n")
        nonblind_lines.append(f"- candidate diversity ratio: `{c_div}`\n")
        nonblind_lines.append(f"- top-1 overlap: `{overlap}`\n\n")
        nonblind_lines.append("### Baseline Top-5\n\n")
        nonblind_lines.append(format_result_table(baseline_rows))
        nonblind_lines.append("\n### Candidate Top-5\n\n")
        nonblind_lines.append(format_result_table(candidate_rows))
        nonblind_lines.append("\n")

        metric_lines.append(
            "| {qid} | {topic} | {bdiv} | {cdiv} | {overlap} | {btop} | {ctop} |\n".format(
                qid=query["id"],
                topic=query["topic"],
                bdiv=b_div,
                cdiv=c_div,
                overlap=overlap,
                btop=baseline_rows[0]["record"]["case_id"] if baseline_rows else "-",
                ctop=candidate_rows[0]["record"]["case_id"] if candidate_rows else "-",
            )
        )

        for blind_system, actual_system, rows in [
            ("A", system_a_name, system_a_rows),
            ("B", system_b_name, system_b_rows),
        ]:
            for idx in range(5):
                if idx < len(rows):
                    record = rows[idx]["record"]
                    judgment_rows.append(
                        {
                            "query_id": query["id"],
                            "query": query["query"],
                            "blind_system": blind_system,
                            "rank": idx + 1,
                            "case_id": record.get("case_id", ""),
                            "title": record.get("case_name", ""),
                            "primary": record.get("issue_type_primary", ""),
                            "employment_stage": record.get("employment_stage", ""),
                            "disposition_type": ", ".join(record.get("disposition_type", [])),
                            "why_surfaced": ", ".join(rows[idx]["why"]) or "-",
                            "relevance": "",
                            "memo": "",
                        }
                    )
                else:
                    judgment_rows.append(
                        {
                            "query_id": query["id"],
                            "query": query["query"],
                            "blind_system": blind_system,
                            "rank": idx + 1,
                            "case_id": "",
                            "title": "",
                            "primary": "",
                            "employment_stage": "",
                            "disposition_type": "",
                            "why_surfaced": "",
                            "relevance": "",
                            "memo": "",
                        }
        )

    baseline_global_div = result_diversity_ratio(all_baseline_rows)
    candidate_global_div = result_diversity_ratio(all_candidate_rows)
    baseline_top1_dup = top1_duplicate_rate(all_baseline_rows)
    candidate_top1_dup = top1_duplicate_rate(all_candidate_rows)

    metric_lines.extend(
        [
            "\n## Aggregate Pre-Metrics\n\n",
            f"- query count: `{len(queries)}`\n",
            f"- cross-system top-1 same-case count: `{top1_overlap_sum}`\n",
            f"- cross-system top-1 same-case ratio: `{round(top1_overlap_sum / len(queries), 3)}`\n",
            f"- baseline diversity ratio (global): `{baseline_global_div}`\n",
            f"- candidate diversity ratio (global): `{candidate_global_div}`\n",
            f"- baseline top-1 duplicate rate: `{baseline_top1_dup}`\n",
            f"- candidate top-1 duplicate rate: `{candidate_top1_dup}`\n",
            "- weighted score / precision / FRR / win-loss-tie: human relevance 입력 후 계산\n",
        ]
    )

    write_json(output_dir / "24q_comparison_data.json", comparison_data)
    write_json(output_dir / "24q_blind_key.json", blind_key)
    (output_dir / "24q_blind_side_by_side.md").write_text("".join(blind_lines), encoding="utf-8")
    (output_dir / "24q_nonblind_top_results.md").write_text("".join(nonblind_lines), encoding="utf-8")
    (output_dir / "24q_prejudgment_metrics.md").write_text("".join(metric_lines), encoding="utf-8")
    write_csv(output_dir / "24q_human_judgment_template.csv", judgment_rows)
    print(f"wrote dry-run package to {output_dir}")


if __name__ == "__main__":
    main()
