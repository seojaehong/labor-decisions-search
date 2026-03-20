import argparse
import json
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Generate override entries from merge collisions.")
    p.add_argument("--root", default=r"C:\dev\labor-decisions-search\retagging")
    p.add_argument(
        "--overrides",
        default=r"C:\dev\labor-decisions-search\retagging\output\reviewed\manual_merge_overrides_v1.json",
    )
    p.add_argument(
        "--collisions",
        default=r"C:\dev\labor-decisions-search\retagging\logs\merge_collisions_report.md",
    )
    p.add_argument(
        "--proposal-report",
        default=r"C:\dev\labor-decisions-search\retagging\logs\collision_override_proposals.md",
    )
    p.add_argument("--write", action="store_true")
    return p.parse_args()


def contains(text, *tokens):
    return any(token in text for token in tokens)


def listify(value):
    return value if isinstance(value, list) else [value]


def load_reviewed_records(reviewed_dir: Path):
    records = {}
    for path in reviewed_dir.glob("*.jsonl"):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                records[(path.name, record["case_id"])] = record
    return records


def parse_collisions(collision_md: Path):
    text = collision_md.read_text(encoding="utf-8")
    entries = []
    cur = None
    for line in text.splitlines():
        if line.startswith("## "):
            if cur:
                entries.append(cur)
            cur = {"case_id": line.split(". ", 1)[1].strip(), "conflicts": []}
        elif line.startswith("소스 A: "):
            cur["a"] = line.split(": ", 1)[1].strip()
        elif line.startswith("소스 B: "):
            cur["b"] = line.split(": ", 1)[1].strip()
        elif line.startswith("충돌 필드: "):
            cur["_field"] = line.split(": ", 1)[1].strip()
        elif line.startswith("  A: "):
            cur["_a"] = json.loads(line.split(": ", 1)[1].strip())
        elif line.startswith("  B: "):
            cur["conflicts"].append(
                (cur.pop("_field"), cur.pop("_a"), json.loads(line.split(": ", 1)[1].strip()))
            )
    if cur:
        entries.append(cur)
    return entries


def choose_primary(summary, notes, conflict_values, record_a, record_b):
    text = f"{summary} {notes}"
    stages = {record_a.get("employment_stage"), record_b.get("employment_stage")}
    dispositions = set(listify(record_a.get("disposition_type", []))) | set(
        listify(record_b.get("disposition_type", []))
    )

    if contains(text, "수습", "시용", "본채용", "채용거부", "본채용 거부") or stages == {"probation"}:
        return "dismissal_validity", "probation_case"
    if contains(text, "직장 내 괴롭힘", "괴롭힘") and contains(text, "성립", "해당", "인정", "사실로 확인"):
        return "workplace_harassment", "harassment_established"
    if contains(text, "양정이 과도", "양정 과다", "양정이 적정", "양정 적정", "징계양정", "비위의 정도", "재량권"):
        return "disciplinary_severity", "severity_case"
    if contains(text, "전보", "전직", "배치전환", "인사발령") and "transfer_validity" in conflict_values:
        return "transfer_validity", "transfer_case"
    if contains(text, "부당노동행위", "불이익", "보복") and "unfair_treatment" in conflict_values:
        return "unfair_treatment", "unfair_treatment_case"
    if contains(text, "무단결근") and not contains(text, "양정") and "absence_without_leave" in conflict_values:
        return "absence_without_leave", "absence_core"
    if contains(text, "폭행", "폭언", "비위", "징계사유가 인정") and not contains(text, "양정"):
        if "misconduct" in conflict_values:
            return "misconduct", "misconduct_core"
    if contains(text, "업무능력", "평가 결과", "평점", "처리지연", "능력 부족", "실수") and "work_ability" in conflict_values:
        return "work_ability", "ability_core"

    pair = tuple(sorted(conflict_values))
    pair_defaults = {
        tuple(sorted(["work_ability", "dismissal_validity"])): "dismissal_validity",
        tuple(sorted(["misconduct", "dismissal_validity"])): "dismissal_validity",
        tuple(sorted(["procedure", "dismissal_validity"])): "dismissal_validity",
        tuple(sorted(["procedure", "unfair_treatment"])): "unfair_treatment",
        tuple(sorted(["misconduct", "transfer_validity"])): "transfer_validity",
    }
    if pair in pair_defaults:
        return pair_defaults[pair], "pair_default"
    if pair == tuple(sorted(["absence_without_leave", "disciplinary_severity"])):
        return ("disciplinary_severity" if contains(text, "양정") else "absence_without_leave"), "pair_absence_severity"
    if pair == tuple(sorted(["disciplinary_severity", "workplace_harassment"])):
        return ("workplace_harassment" if contains(text, "괴롭힘") else "disciplinary_severity"), "pair_harassment_severity"
    if pair == tuple(sorted(["misconduct", "disciplinary_severity"])):
        return ("disciplinary_severity" if contains(text, "양정") else "misconduct"), "pair_misconduct_severity"

    return conflict_values[0], "fallback_first"


def choose_disposition(summary, notes, record_a, record_b, chosen_primary):
    text = f"{summary} {notes}"
    a = listify(record_a.get("disposition_type", []))
    b = listify(record_b.get("disposition_type", []))
    combined = sorted(set(a) | set(b))

    if "rejection_of_regular_employment" in combined or "probation_termination" in combined:
        if contains(text, "본채용", "채용 거부", "채용거부", "정식채용을 거부"):
            return ["rejection_of_regular_employment"], "probation_rejection"
        if contains(text, "시용기간 중 해고", "수습기간 중 해고", "해약권"):
            return ["probation_termination"], "probation_termination"
        if chosen_primary == "dismissal_validity":
            return (
                ["rejection_of_regular_employment"] if contains(text, "본채용") else ["probation_termination"],
                "probation_primary",
            )
    if "dismissal" in combined and "disciplinary_dismissal" in combined:
        if contains(text, "징계해고", "징계처분", "정직", "감봉", "해임", "징계사유") or chosen_primary in {"misconduct", "disciplinary_severity"}:
            return ["disciplinary_dismissal"], "disciplinary_dismissal"
        return ["dismissal"], "general_dismissal"
    if "contract_termination" in combined:
        return ["contract_termination"], "contract_termination"
    if "nonrenewal" in combined:
        return ["nonrenewal"], "nonrenewal"
    if chosen_primary == "transfer_validity" and "transfer" in combined:
        return ["transfer"], "transfer_only"

    if len(combined) > 1:
        return combined, "union_preserve"
    return combined, "single"


def choose_industry(summary, notes, value_a, value_b):
    if value_a == "unknown" and value_b != "unknown":
        return value_b, "specific_over_unknown"
    if value_b == "unknown" and value_a != "unknown":
        return value_a, "specific_over_unknown"
    if value_a == value_b:
        return value_a, "same"

    text = f"{summary} {notes}"
    if contains(text, "학교", "교수", "강사", "학원"):
        return "education", "education_keyword"
    if contains(text, "병원", "의료", "간호", "환자", "조리원"):
        return "healthcare", "healthcare_keyword"
    if contains(text, "택시", "버스", "운전", "운수", "교통"):
        return "transport", "transport_keyword"
    if contains(text, "건설", "현장", "원청"):
        return "construction", "construction_keyword"
    if contains(text, "여수시", "공단", "시청", "지자체", "공공", "공사"):
        return "public", "public_keyword"
    if contains(text, "은행", "증권", "보험"):
        return "finance", "finance_keyword"
    if contains(text, "사무", "총무", "회계", "행정"):
        return "office", "office_keyword"
    if contains(text, "매장", "판매", "서비스", "콜센터", "경비", "미화", "편의점"):
        return "service", "service_keyword"
    return (value_a if value_a != "unknown" else value_b), "fallback_specific"


def choose_stage(summary, notes, value_a, value_b, chosen_disposition):
    text = f"{summary} {notes}"
    if contains(text, "수습", "시용", "본채용"):
        return "probation", "probation_keyword"
    if contains(text, "갱신기대권", "재계약", "계약갱신", "갱신 거절"):
        return "renewal_stage", "renewal_keyword"
    if contains(text, "기간제", "계약기간 만료"):
        return "fixed_term", "fixed_term_keyword"
    if "rejection_of_regular_employment" in chosen_disposition or "probation_termination" in chosen_disposition:
        return "probation", "disposition_probation"
    return value_a, "fallback_first"


def adjudicate_entry(entry, records):
    record_a = records[(entry["a"], entry["case_id"])]
    record_b = records[(entry["b"], entry["case_id"])]
    summary = record_a.get("holding_summary", "")
    notes = f"{record_a.get('notes', '')} {record_b.get('notes', '')}".strip()

    chosen = {}
    reason_parts = []

    primary_conflict = next((c for c in entry["conflicts"] if c[0] == "issue_type_primary"), None)
    if primary_conflict:
        chosen_primary, why = choose_primary(summary, notes, [primary_conflict[1], primary_conflict[2]], record_a, record_b)
        chosen["issue_type_primary"] = chosen_primary
        reason_parts.append(f"primary={why}")
    else:
        chosen_primary = record_a.get("issue_type_primary")

    disposition_conflict = next((c for c in entry["conflicts"] if c[0] == "disposition_type"), None)
    if disposition_conflict:
        disposition, why = choose_disposition(summary, notes, {"disposition_type": disposition_conflict[1]}, {"disposition_type": disposition_conflict[2]}, chosen_primary)
        chosen["disposition_type"] = disposition
        reason_parts.append(f"disposition={why}")
    else:
        disposition = listify(record_a.get("disposition_type", []))

    industry_conflict = next((c for c in entry["conflicts"] if c[0] == "industry_context"), None)
    if industry_conflict:
        industry, why = choose_industry(summary, notes, industry_conflict[1], industry_conflict[2])
        chosen["industry_context"] = industry
        reason_parts.append(f"industry={why}")

    stage_conflict = next((c for c in entry["conflicts"] if c[0] == "employment_stage"), None)
    if stage_conflict:
        stage, why = choose_stage(summary, notes, stage_conflict[1], stage_conflict[2], disposition)
        chosen["employment_stage"] = stage
        reason_parts.append(f"employment_stage={why}")

    reason = (
        f"2026-03-21 collision adjudication: {'; '.join(reason_parts)}. "
        f"Summary basis: {summary}"
    )
    return {"case_id": entry["case_id"], "fields": chosen, "reason": reason}


def write_proposal_report(path: Path, proposals, records, entries):
    entry_map = {e["case_id"]: e for e in entries}
    lines = ["# Collision Override Proposals\n\n"]
    for proposal in proposals:
        case_id = proposal["case_id"]
        entry = entry_map[case_id]
        record_a = records[(entry["a"], case_id)]
        lines.append(f"## {case_id}\n\n")
        lines.append(f"- source_a: `{entry['a']}`\n")
        lines.append(f"- source_b: `{entry['b']}`\n")
        lines.append(f"- override: `{json.dumps(proposal['fields'], ensure_ascii=False)}`\n")
        lines.append(f"- reason: {proposal['reason']}\n")
        lines.append(f"- summary: {record_a.get('holding_summary', '')}\n\n")
    path.write_text("".join(lines), encoding="utf-8")


def main():
    args = parse_args()
    root = Path(args.root)
    records = load_reviewed_records(root / "output" / "reviewed")
    entries = parse_collisions(Path(args.collisions))

    overrides_path = Path(args.overrides)
    data = json.loads(overrides_path.read_text(encoding="utf-8"))
    existing = {item["case_id"] for item in data.get("overrides", [])}

    proposals = []
    for entry in entries:
        if entry["case_id"] in existing:
            continue
        proposals.append(adjudicate_entry(entry, records))

    write_proposal_report(Path(args.proposal_report), proposals, records, entries)
    print(f"generated proposals: {len(proposals)}")

    if args.write:
        data["overrides"].extend(proposals)
        if "_source" in data:
            data["_source"] = data["_source"] + " + 2026-03-21 collision adjudication"
        overrides_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"updated overrides: {overrides_path}")


if __name__ == "__main__":
    main()
