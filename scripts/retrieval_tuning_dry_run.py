import json
from pathlib import Path


ROOT = Path(r"C:\dev\labor-decisions-search")
MERGED_PATH = ROOT / "retagging/output/merged/merged_final_v1.jsonl"
QUERIES_PATH = ROOT / "retagging/evaluation/representative_queries_v1.json"
CURRENT_PATH = ROOT / "retagging/evaluation/dry_run_24q/24q_comparison_data.json"
OUT_DIR = ROOT / "retagging/implementation"


TARGETS = {
    "Q12": {
        "label": "Q8 징계사유는 인정되지만 해고까지는 과하다고 본 사건",
        "scenario": "severity_excessive",
        "observed_before": "실패",
    },
    "Q10": {
        "label": "Q7 정규직 저성과/업무능력 부족 해고",
        "scenario": "regular_work_ability",
        "observed_before": "대체로 양호",
    },
    "Q02": {
        "label": "Q2 무단결근 + 절차위반",
        "scenario": "absence_procedure",
        "observed_before": "실패",
    },
    "Q05": {
        "label": "Q4 괴롭힘 신고 후 보복성 인사조치",
        "scenario": "retaliation",
        "observed_before": "실패",
    },
}

KEYWORD_TO_STAGE = [
    ("정규직", "regular"),
    ("상용직", "regular"),
    ("기간의 정함이 없는", "regular"),
    ("수습", "probation"),
    ("시용", "probation"),
    ("본채용", "probation"),
    ("기간제", "fixed_term"),
    ("계약직", "fixed_term"),
    ("계약기간 만료", "fixed_term"),
    ("갱신", "fixed_term"),
    ("채용내정", "pre_hire"),
    ("채용 전", "pre_hire"),
    ("입사 전", "pre_hire"),
]


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def includes_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def arr(row, key):
    value = row.get(key)
    return value if isinstance(value, list) else []


def extract_stage_hints(query_text: str) -> list[str]:
    hints = []
    for keyword, stage in KEYWORD_TO_STAGE:
        if keyword in query_text and stage not in hints:
            hints.append(stage)
    return hints


def build_profile(query_text: str):
    lowered = query_text.lower()
    stage_hints = extract_stage_hints(query_text)
    has_absence = includes_any(lowered, ["무단결근", "결근", "근무태만", "근무지 이탈"])
    has_procedure = includes_any(lowered, ["절차", "서면통지", "서면 통지", "소명", "인사위원회"])
    has_regular = includes_any(lowered, ["정규직"])
    has_work_ability = includes_any(lowered, ["업무능력", "저성과", "성과 부족", "성과부족"])
    has_retaliation = includes_any(lowered, ["보복", "불이익", "신고 이후", "신고자"])
    has_harassment = includes_any(lowered, ["직장내괴롭힘", "괴롭힘"])
    has_severity = includes_any(lowered, ["양정", "과하", "과도", "너무 과", "수위"])
    has_dismissal = includes_any(lowered, ["해고"])

    if has_absence and has_procedure:
        return {
            "scenario": "absence_procedure",
            "primary_pool": ["procedure", "dismissal_validity", "absence_without_leave"],
            "primary_boosts": {"procedure": 16, "dismissal_validity": 10, "absence_without_leave": 4},
            "preferred_stages": [],
            "penalized_stages": [],
            "preferred_secondary": ["procedure", "absence_without_leave"],
            "preferred_dispositions": [],
            "preferred_fact_markers": ["unauthorized_absence", "written_notice_missing"],
            "preferred_legal_focus": ["procedural_due_process"],
            "boosted_results": [],
            "excluded_results": ["dismissed", "settled"],
            "penalized_keywords": ["구제이익", "복직명령", "상시근로자 수", "채용내정"],
        }

    if has_regular and has_work_ability:
        return {
            "scenario": "regular_work_ability",
            "primary_pool": ["work_ability", "dismissal_validity"],
            "primary_boosts": {"work_ability": 15, "dismissal_validity": 7},
            "preferred_stages": ["regular"] if "regular" in stage_hints else ["regular"],
            "penalized_stages": ["probation"] if "regular" in stage_hints else [],
            "preferred_secondary": [],
            "preferred_dispositions": [],
            "preferred_fact_markers": ["qualitative_evaluation", "quantitative_evaluation", "warning_given", "improvement_opportunity_given", "training_provided"],
            "preferred_legal_focus": ["just_cause", "social_norm_reasonableness"],
            "boosted_results": [],
            "excluded_results": [],
            "penalized_keywords": ["수습", "본채용", "시용"],
        }

    if has_harassment and has_retaliation:
        return {
            "scenario": "retaliation",
            "primary_pool": ["retaliation", "unfair_treatment", "workplace_harassment"],
            "primary_boosts": {"retaliation": 16, "unfair_treatment": 13, "workplace_harassment": 3},
            "preferred_stages": stage_hints,
            "penalized_stages": ["probation"] if "regular" in stage_hints else [],
            "preferred_secondary": ["workplace_harassment", "unfair_treatment"],
            "preferred_dispositions": ["dismissal", "disciplinary_dismissal", "transfer", "suspension", "pay_cut", "reprimand"],
            "preferred_fact_markers": ["harassment_report_filed"],
            "preferred_legal_focus": ["protection_against_retaliation"],
            "boosted_results": [],
            "excluded_results": [],
            "penalized_keywords": ["2차 가해", "성희롱", "쟁의행위", "노동조합", "조합원"],
        }

    if has_severity and has_dismissal:
        return {
            "scenario": "severity_excessive",
            "primary_pool": ["disciplinary_severity", "misconduct"],
            "primary_boosts": {"disciplinary_severity": 16, "misconduct": 5},
            "preferred_stages": [],
            "penalized_stages": [],
            "preferred_secondary": ["misconduct"],
            "preferred_dispositions": ["dismissal", "disciplinary_dismissal", "suspension", "pay_cut"],
            "preferred_fact_markers": [],
            "preferred_legal_focus": ["proportionality", "appropriateness_of_discipline"],
            "boosted_results": ["granted", "partial", "overturned"],
            "excluded_results": ["dismissed", "settled"],
            "penalized_keywords": ["구제이익", "채용내정", "상시근로자 수", "복직명령", "계약기간 만료"],
        }

    return {
        "scenario": "generic",
        "primary_pool": [],
        "primary_boosts": {},
        "preferred_stages": stage_hints,
        "penalized_stages": [],
        "preferred_secondary": [],
        "preferred_dispositions": [],
        "preferred_fact_markers": [],
        "preferred_legal_focus": [],
        "boosted_results": [],
        "excluded_results": [],
        "penalized_keywords": [],
    }


def score_record(row, query_text, profile):
    score = 0
    reasons = []
    primary = row.get("issue_type_primary", "")
    secondary = arr(row, "issue_type_secondary")
    dispositions = arr(row, "disposition_type")
    fact_markers = arr(row, "fact_markers")
    legal_focus = arr(row, "legal_focus")
    exclusions = arr(row, "exclusion_flags")
    stage = row.get("employment_stage", "")
    decision_result = row.get("decision_result", "")
    haystack = " ".join([
        row.get("case_name", ""),
        row.get("summary_short", ""),
        row.get("holding_summary", ""),
        row.get("retrieval_note", ""),
    ])

    if primary in profile["primary_boosts"]:
        score += profile["primary_boosts"][primary]
        reasons.append(f"primary:{primary}")

    hits = [x for x in profile["preferred_secondary"] if x in secondary]
    if hits:
        score += 4 * len(hits)
        reasons.append(f"secondary:{','.join(hits)}")

    hits = [x for x in profile["preferred_dispositions"] if x in dispositions]
    if hits:
        score += 4 * len(hits)
        reasons.append(f"disposition:{','.join(hits)}")

    hits = [x for x in profile["preferred_fact_markers"] if x in fact_markers]
    if hits:
        score += 5 * len(hits)
        reasons.append(f"fact:{','.join(hits)}")

    hits = [x for x in profile["preferred_legal_focus"] if x in legal_focus]
    if hits:
        score += 6 * len(hits)
        reasons.append(f"focus:{','.join(hits)}")

    if stage in profile["preferred_stages"]:
        score += 7
        reasons.append(f"stage:{stage}")
    if stage in profile["penalized_stages"]:
        score -= 9
        reasons.append(f"stage_penalty:{stage}")

    if decision_result in profile["boosted_results"]:
        score += 4
        reasons.append(f"result_boost:{decision_result}")

    if "결근" in query_text and "not_really_absence_case" in exclusions:
        score -= 10
        reasons.append("exclude:not_really_absence_case")
    if "괴롭힘" in query_text and "not_really_harassment_case" in exclusions and profile["scenario"] != "retaliation":
        score -= 10
        reasons.append("exclude:not_really_harassment_case")

    for keyword in profile["penalized_keywords"]:
        if keyword in haystack:
            score -= 6
            reasons.append(f"keyword_penalty:{keyword}")

    query_tokens = [token for token in query_text.split() if len(token) >= 2]
    text_hits = sum(1 for token in query_tokens if token in haystack)
    if text_hits:
        score += min(text_hits, 4)
        reasons.append(f"text:{text_hits}")

    if profile["scenario"] == "absence_procedure":
        has_procedure = primary == "procedure" or "procedure" in secondary or "procedural_due_process" in legal_focus
        has_absence = primary == "absence_without_leave" or "absence_without_leave" in secondary or "unauthorized_absence" in fact_markers
        if has_procedure and has_absence:
            score += 7
            reasons.append("cross:absence+procedure")
        elif primary == "absence_without_leave":
            score -= 6
            reasons.append("cross_penalty:absence_only")

    if profile["scenario"] == "regular_work_ability":
        if primary == "work_ability" and stage == "regular":
            score += 7
            reasons.append("cross:regular_work_ability")
        if stage == "probation":
            score -= 6
            reasons.append("cross_penalty:probation_mix")

    if profile["scenario"] == "retaliation":
        has_retaliation = (
            primary in {"retaliation", "unfair_treatment"}
            or "protection_against_retaliation" in legal_focus
            or "harassment_report_filed" in fact_markers
        )
        if has_retaliation:
            score += 7
            reasons.append("cross:retaliation_structure")
        if primary == "workplace_harassment" and not has_retaliation:
            score -= 7
            reasons.append("cross_penalty:harassment_only")

    if profile["scenario"] == "severity_excessive":
        has_severity = (
            primary == "disciplinary_severity"
            and ("proportionality" in legal_focus or "appropriateness_of_discipline" in legal_focus)
        )
        if has_severity:
            score += 8
            reasons.append("cross:severity_proportionality")
        if decision_result in {"dismissed", "rejected"}:
            score -= 4
            reasons.append("cross_penalty:non_excessive_outcome")

    return score, reasons


def relevance_like(row, scenario):
    primary = row.get("issue_type_primary", "")
    stage = row.get("employment_stage", "")
    secondary = set(arr(row, "issue_type_secondary"))
    dispositions = set(arr(row, "disposition_type"))
    fact_markers = set(arr(row, "fact_markers"))
    legal_focus = set(arr(row, "legal_focus"))
    decision_result = row.get("decision_result", "")
    text = " ".join([row.get("summary_short", ""), row.get("holding_summary", ""), row.get("retrieval_note", ""), row.get("notes", "")])

    if scenario == "severity_excessive":
        if primary == "disciplinary_severity" and {"proportionality", "appropriateness_of_discipline"} & legal_focus and decision_result not in {"dismissed", "rejected", "settled"}:
            return 2
        if primary == "disciplinary_severity" and ("misconduct" in secondary or "dismissal" in dispositions or "disciplinary_dismissal" in dispositions):
            return 1
        return 0

    if scenario == "regular_work_ability":
        if primary == "work_ability" and stage == "regular":
            return 2
        if primary in {"work_ability", "dismissal_validity"} and stage != "probation":
            return 1
        return 0

    if scenario == "absence_procedure":
        has_procedure = primary == "procedure" or "procedure" in secondary or "procedural_due_process" in legal_focus
        has_absence = primary == "absence_without_leave" or "absence_without_leave" in secondary or "unauthorized_absence" in fact_markers or "무단결근" in text
        if has_procedure and has_absence:
            return 2
        if has_procedure:
            return 1
        return 0

    if scenario == "retaliation":
        if primary in {"retaliation", "unfair_treatment"} and ("harassment_report_filed" in fact_markers or "protection_against_retaliation" in legal_focus or dispositions & {"dismissal", "disciplinary_dismissal", "transfer", "suspension", "pay_cut"}):
            return 2
        if primary in {"retaliation", "unfair_treatment", "workplace_harassment"}:
            return 1
        return 0

    return 0


def final_status(rows, scenario):
    rels = [relevance_like(row["record"], scenario) for row in rows[:5]]
    weighted = sum(rels)
    top3 = sum(1 for rel in rels[:3] if rel >= 1)
    if weighted >= 8 and top3 >= 2:
        return "양호"
    if weighted >= 4 and top3 >= 1:
        return "대체로 양호"
    return "실패"


def current_failure_reason(query_id, current_rows):
    if query_id == "Q12":
        return "disciplinary_severity 모집단 안에서 proportionality/appropriateness_of_discipline보다 단순 primary match와 text overlap이 먼저 작동해 각하·구제이익·비본질 사건이 섞였다."
    if query_id == "Q10":
        return "work_ability 자체는 잡지만 employment_stage=regular 우선이 없어 probation/본채용거부 구조가 섞일 수 있었다."
    if query_id == "Q02":
        return "absence와 procedure가 동시에 필요한 질의인데, 현행 후보 랭킹은 issue_type_primary match 위주라 교차 구조를 강하게 보상하지 못했다."
    if query_id == "Q05":
        return "retaliation/unfair_treatment 직접 회수보다 workplace_harassment나 일반 징계 사건이 같이 올라오고, 신고 이후 보복 구조를 랭킹이 충분히 반영하지 못했다."
    return ""


def format_rows(rows):
    lines = []
    for idx, row in enumerate(rows[:5], start=1):
        rec = row["record"]
        lines.append(
            f"| {idx} | {rec.get('case_id','')} | {rec.get('issue_type_primary','')} | {rec.get('employment_stage','')} | {', '.join(arr(rec,'disposition_type'))} | {row['score']} | {', '.join(row.get('why', [])) or '-'} |\n"
        )
    return "".join(lines)


def main():
    merged = load_jsonl(MERGED_PATH)
    by_case = {row["case_id"]: row for row in merged}
    queries = {row["id"]: row for row in json.loads(QUERIES_PATH.read_text(encoding="utf-8"))}
    current = {item["query"]["id"]: item for item in json.loads(CURRENT_PATH.read_text(encoding="utf-8"))}

    analysis_lines = ["# Retrieval Failure Analysis\n\n"]
    tuning_lines = ["# Retrieval Tuning v1\n\n"]
    comparison_lines = ["# Retrieval Tuning Before/After Comparison\n\n"]

    tuning_lines.append("## 적용 원칙\n\n")
    tuning_lines.append("- baseline/search UI는 건드리지 않는다.\n")
    tuning_lines.append("- candidate 경로에서 query-aware reranking을 강화한다.\n")
    tuning_lines.append("- primary 단일 일치보다 stage/disposition/fact/legal/result 교차를 더 크게 본다.\n\n")

    for query_id, meta in TARGETS.items():
        query = queries[query_id]
        profile = build_profile(query["query"])
        pool = [row for row in merged if row.get("issue_type_primary") in profile["primary_pool"]]
        tuned_rows = []
        for row in pool:
            if row.get("decision_result", "") in profile["excluded_results"]:
                continue
            score, why = score_record(row, query["query"], profile)
            if score > 0:
                tuned_rows.append({"record": row, "score": score, "why": why})
        tuned_rows.sort(key=lambda item: (-item["score"], item["record"].get("case_id", "")))

        current_rows = current[query_id]["candidate"]
        before_rows = [{"record": row["record"], "score": row["score"], "why": row["why"]} for row in current_rows]

        before_status = meta["observed_before"]
        after_status = final_status(tuned_rows, meta["scenario"])

        analysis_lines.append(f"## {meta['label']}\n\n")
        analysis_lines.append(f"- query id: `{query_id}`\n")
        analysis_lines.append(f"- 현재 실패 원인: {current_failure_reason(query_id, current_rows)}\n")
        analysis_lines.append("- 현재 상위 결과 why surfaced:\n")
        for row in before_rows[:5]:
            rec = row["record"]
            analysis_lines.append(f"  - `{rec['case_id']}` `{rec['issue_type_primary']}` | {', '.join(row['why'])}\n")
        analysis_lines.append("\n")

        tuning_lines.append(f"## {meta['label']}\n\n")
        tuning_lines.append(f"- scenario: `{profile['scenario']}`\n")
        tuning_lines.append(f"- primary pool: `{', '.join(profile['primary_pool'])}`\n")
        if profile["preferred_stages"]:
            tuning_lines.append(f"- preferred stage: `{', '.join(profile['preferred_stages'])}`\n")
        if profile["penalized_stages"]:
            tuning_lines.append(f"- penalized stage: `{', '.join(profile['penalized_stages'])}`\n")
        if profile["preferred_dispositions"]:
            tuning_lines.append(f"- preferred disposition: `{', '.join(profile['preferred_dispositions'])}`\n")
        if profile["preferred_fact_markers"]:
            tuning_lines.append(f"- preferred fact markers: `{', '.join(profile['preferred_fact_markers'])}`\n")
        if profile["preferred_legal_focus"]:
            tuning_lines.append(f"- preferred legal focus: `{', '.join(profile['preferred_legal_focus'])}`\n")
        if profile["boosted_results"]:
            tuning_lines.append(f"- boosted decision_result: `{', '.join(profile['boosted_results'])}`\n")
        if profile["excluded_results"]:
            tuning_lines.append(f"- excluded decision_result: `{', '.join(profile['excluded_results'])}`\n")
        if profile["penalized_keywords"]:
            tuning_lines.append(f"- penalized keywords: `{', '.join(profile['penalized_keywords'])}`\n")
        tuning_lines.append("\n")

        comparison_lines.append(f"## {meta['label']}\n\n")
        comparison_lines.append(f"- observed before status: `{before_status}`\n")
        comparison_lines.append(f"- after retrieval status: `{after_status}`\n\n")
        comparison_lines.append("### Before Top-5\n\n")
        comparison_lines.append("| rank | case_id | primary | stage | disposition | score | why |\n")
        comparison_lines.append("|------|---------|---------|-------|-------------|-------|-----|\n")
        comparison_lines.append(format_rows(before_rows))
        comparison_lines.append("\n### After Top-5\n\n")
        comparison_lines.append("| rank | case_id | primary | stage | disposition | score | why |\n")
        comparison_lines.append("|------|---------|---------|-------|-------------|-------|-----|\n")
        comparison_lines.append(format_rows(tuned_rows))
        comparison_lines.append("\n")

    comparison_lines.append("## Next Priorities\n\n")
    comparison_lines.append("1. `retaliation/unfair_treatment` 질의에서 신고 후 보복 구조를 더 직접 표현하는 fact_markers/keywords 확장\n")
    comparison_lines.append("2. `disciplinary_severity` 질의에서 decision_result와 legal_focus 기반 노이즈 감점 추가 보정\n")
    comparison_lines.append("3. `regular work_ability` 질의에서 probation 분리와 개선기회 marker coverage 확장\n")
    comparison_lines.append("4. `absence + procedure` 질의에서 written_notice_missing 등 procedural markers 보강 여부 점검\n")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "retrieval_tuning_failure_analysis.md").write_text("".join(analysis_lines), encoding="utf-8")
    (OUT_DIR / "retrieval_tuning_v1.md").write_text("".join(tuning_lines), encoding="utf-8")
    (OUT_DIR / "retrieval_tuning_comparison.md").write_text("".join(comparison_lines), encoding="utf-8")
    print("wrote retrieval tuning docs")


if __name__ == "__main__":
    main()
