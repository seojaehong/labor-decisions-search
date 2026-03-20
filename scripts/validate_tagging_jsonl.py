"""
판정례 재태깅 JSONL 검증 스크립트

사용법:
    python3 scripts/validate_tagging_jsonl.py retagging/output/draft/*.jsonl
    python3 scripts/validate_tagging_jsonl.py retagging/output/draft/absence_sample_output.jsonl --report
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import argparse
from pathlib import Path
from collections import Counter

# ── 태그 사전 v1 (docs/tagging-schema-v1.json 기준) ──

EMPLOYMENT_STAGE = {
    "probation", "regular", "fixed_term", "renewal_stage", "pre_hire", "unknown"
}

ISSUE_TYPE_PRIMARY = {
    "performance", "low_sales", "work_ability", "attendance", "absence_without_leave",
    "disciplinary_severity", "workplace_harassment", "harassment_report",
    "harassment_investigation", "retaliation", "misconduct", "procedure",
    "renewal_expectation", "dismissal_validity", "unfair_treatment",
    "redundancy", "transfer_validity", "worker_status", "discrimination",
    "wage_dispute", "other",
}

ISSUE_TYPE_SECONDARY = ISSUE_TYPE_PRIMARY | {
    "warning", "training_opportunity", "evaluation", "comparative_fairness",
}

DISPOSITION_TYPE = {
    "dismissal", "disciplinary_dismissal", "probation_termination",
    "rejection_of_regular_employment", "suspension", "reprimand", "pay_cut",
    "demotion", "transfer", "contract_termination", "nonrenewal",
    "corrective_order_related", "no_formal_disposition", "other",
}

FACT_MARKERS = {
    "sales_target_not_met", "quantitative_evaluation", "qualitative_evaluation",
    "probation_period", "short_tenure", "six_month_tenure", "long_tenure",
    "warning_given", "improvement_opportunity_given", "training_provided",
    "repeated_absence", "unauthorized_absence", "investigation_conducted",
    "harassment_report_filed", "victim_claim", "witness_statement",
    "disciplinary_committee", "procedural_defect", "written_notice",
    "written_notice_missing", "comparative_employee_case", "prior_sanction_history",
    "emotional_conflict_only", "evidence_insufficient", "evidence_sufficient",
    "public_institution", "mutual_agreement", "resignation_dispute",
}

LEGAL_FOCUS = {
    "just_cause", "social_norm_reasonableness", "proportionality",
    "procedural_due_process", "evidentiary_sufficiency", "employer_burden_of_proof",
    "expectation_of_renewal", "duty_of_investigation", "protection_against_retaliation",
    "appropriateness_of_discipline", "suitability_for_regular_employment",
    "worker_status_determination", "discrimination_prohibition",
}

INDUSTRY_CONTEXT = {
    "sales", "retail", "office", "manufacturing", "service", "education",
    "healthcare", "public", "construction", "transport", "finance", "it", "unknown",
}

EXCLUSION_FLAGS = {
    "not_really_performance_case", "not_really_harassment_case",
    "not_really_absence_case", "renewal_expectation_dominant",
    "settlement_or_mutual_termination", "resignation_dispute",
    "procedure_dominant", "evidence_too_thin", "fact_specific_low_reusability",
    "unrelated_to_probation", "unrelated_to_dismissal", "unrelated_to_harassment",
    "emotional_conflict_not_harassment",
}

CONFIDENCE = {"high", "medium", "low"}

# TODO: review_status 확장 시 여기에 추가
REVIEW_STATUS = {"pending", "reviewed", "final", "needs_revision", "approved"}

# ── 필수 필드 ──

REQUIRED_FIELDS = [
    "case_id", "case_name", "summary_short", "holding_summary", "retrieval_note",
    "employment_stage", "issue_type_primary", "issue_type_secondary",
    "disposition_type", "fact_markers", "legal_focus", "industry_context",
    "exclusion_flags", "include_for_queries", "exclude_for_queries",
    "confidence", "notes", "review_status", "tag_version",
]

# 배열이어야 하는 필드
ARRAY_FIELDS = {
    "issue_type_secondary", "disposition_type", "fact_markers", "legal_focus",
    "exclusion_flags", "include_for_queries", "exclude_for_queries",
}

# enum 검증 매핑
ENUM_FIELDS = {
    "employment_stage": EMPLOYMENT_STAGE,
    "issue_type_primary": ISSUE_TYPE_PRIMARY,
    "confidence": CONFIDENCE,
    "review_status": REVIEW_STATUS,
    "industry_context": INDUSTRY_CONTEXT,
}

ARRAY_ENUM_FIELDS = {
    "issue_type_secondary": ISSUE_TYPE_SECONDARY,
    "disposition_type": DISPOSITION_TYPE,
    "fact_markers": FACT_MARKERS,
    "legal_focus": LEGAL_FOCUS,
    "exclusion_flags": EXCLUSION_FLAGS,
}


def validate_record(record, line_num, file_path):
    """단일 레코드 검증. (errors, warnings) 리스트 반환."""
    errors = []
    warnings = []
    case_id = record.get("case_id", f"UNKNOWN@line{line_num}")

    def err(msg):
        errors.append(f"[ERROR] {file_path}:{line_num} ({case_id}) — {msg}")

    def warn(msg):
        warnings.append(f"[WARN]  {file_path}:{line_num} ({case_id}) — {msg}")

    # 필수 필드 존재
    for field in REQUIRED_FIELDS:
        if field not in record:
            err(f"필수 필드 누락: {field}")

    # 문자열 필드 비어있는지
    for field in ["case_id", "summary_short", "holding_summary", "tag_version"]:
        val = record.get(field)
        if val is not None and isinstance(val, str) and val.strip() == "":
            err(f"빈 문자열: {field}")

    # issue_type_primary: 단일 문자열
    primary = record.get("issue_type_primary")
    if primary is not None:
        if not isinstance(primary, str):
            err(f"issue_type_primary가 문자열이 아님: {type(primary).__name__}")
        elif primary not in ISSUE_TYPE_PRIMARY:
            warn(f"issue_type_primary 허용값 밖: '{primary}'")

    # enum 필드 검증
    for field, allowed in ENUM_FIELDS.items():
        val = record.get(field)
        if val is not None and isinstance(val, str) and val not in allowed:
            warn(f"{field} 허용값 밖: '{val}'")

    # 배열 필드 검증
    for field in ARRAY_FIELDS:
        val = record.get(field)
        if val is not None and not isinstance(val, list):
            err(f"{field}가 배열이 아님: {type(val).__name__}")

    # 배열 내 enum 검증
    for field, allowed in ARRAY_ENUM_FIELDS.items():
        val = record.get(field)
        if isinstance(val, list):
            for item in val:
                if item not in allowed:
                    warn(f"{field} 내 허용값 밖: '{item}'")

    # retrieval_note, notes 비어있으면 경고
    for field in ["retrieval_note", "notes"]:
        val = record.get(field)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            warn(f"{field}가 비어있음 — 검색 품질 개선에 유용한 정보가 누락될 수 있음")

    # tag_version 확인
    tv = record.get("tag_version")
    if tv is not None and tv != "v1":
        warn(f"tag_version이 'v1'이 아님: '{tv}'")

    return errors, warnings


def validate_file(file_path):
    """JSONL 파일 전체 검증."""
    path = Path(file_path)
    if not path.exists():
        print(f"[ERROR] 파일 없음: {file_path}")
        return [], [], [], 0

    all_errors = []
    all_warnings = []
    case_ids = []
    valid_count = 0

    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            # JSON 파싱
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                all_errors.append(f"[ERROR] {file_path}:{line_num} — JSON 파싱 실패: {e}")
                continue

            if not isinstance(record, dict):
                all_errors.append(f"[ERROR] {file_path}:{line_num} — 최상위가 dict가 아님")
                continue

            errors, warnings = validate_record(record, line_num, path.name)
            all_errors.extend(errors)
            all_warnings.extend(warnings)

            case_id = record.get("case_id")
            if case_id:
                case_ids.append(case_id)

            if not errors:
                valid_count += 1

    # 중복 case_id 검사
    id_counts = Counter(case_ids)
    for cid, count in id_counts.items():
        if count > 1:
            all_warnings.append(f"[WARN]  {path.name} — case_id 중복: '{cid}' ({count}회)")

    return all_errors, all_warnings, case_ids, valid_count


def main():
    parser = argparse.ArgumentParser(description="판정례 재태깅 JSONL 검증")
    parser.add_argument("files", nargs="+", help="검증할 JSONL 파일 경로")
    parser.add_argument("--report", action="store_true", help="logs/validation_report.md 저장")
    args = parser.parse_args()

    total_errors = []
    total_warnings = []
    total_records = 0
    total_valid = 0
    file_summaries = []
    all_case_ids = []
    primary_counter = Counter()
    confidence_counter = Counter()

    for file_path in args.files:
        errors, warnings, case_ids, valid_count = validate_file(file_path)
        total_errors.extend(errors)
        total_warnings.extend(warnings)
        total_records += len(case_ids)
        total_valid += valid_count
        all_case_ids.extend(case_ids)

        # primary 분포 수집
        path = Path(file_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                        p = r.get("issue_type_primary", "?")
                        primary_counter[p] += 1
                        c = r.get("confidence", "?")
                        confidence_counter[c] += 1
                    except json.JSONDecodeError:
                        pass

        file_summaries.append({
            "file": Path(file_path).name,
            "records": len(case_ids),
            "valid": valid_count,
            "errors": len(errors),
            "warnings": len(warnings),
        })

    # 전체 중복 검사
    global_id_counts = Counter(all_case_ids)
    global_dupes = {k: v for k, v in global_id_counts.items() if v > 1}
    if global_dupes:
        for cid, count in global_dupes.items():
            total_warnings.append(f"[WARN]  전체 — case_id 중복: '{cid}' ({count}회)")

    # ── 리포트 출력 ──
    print("=" * 60)
    print("  판정례 재태깅 JSONL 검증 리포트")
    print("=" * 60)

    print(f"\n검증 파일: {len(args.files)}개")
    for s in file_summaries:
        status = "OK" if s["errors"] == 0 else "ERROR"
        print(f"  {s['file']}: {s['records']}건, 유효 {s['valid']}, 에러 {s['errors']}, 경고 {s['warnings']} [{status}]")

    print(f"\n합계: {total_records}건, 유효 {total_valid}, 에러 {len(total_errors)}, 경고 {len(total_warnings)}")

    if global_dupes:
        print(f"\n전체 중복 case_id: {len(global_dupes)}건")

    print(f"\n[issue_type_primary 분포]")
    for k, v in primary_counter.most_common():
        print(f"  {k}: {v}")

    print(f"\n[confidence 분포]")
    for k, v in confidence_counter.most_common():
        print(f"  {k}: {v}")

    if total_errors:
        print(f"\n{'─' * 60}")
        print(f"에러 상세 ({len(total_errors)}건):")
        for e in total_errors:
            print(f"  {e}")

    if total_warnings:
        print(f"\n{'─' * 60}")
        print(f"경고 상세 ({len(total_warnings)}건):")
        for w in total_warnings[:50]:  # 최대 50건
            print(f"  {w}")
        if len(total_warnings) > 50:
            print(f"  ... 외 {len(total_warnings) - 50}건")

    # ── 리포트 파일 저장 ──
    if args.report:
        report_dir = Path("retagging/logs")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "validation_report.md"

        lines = [
            "# 재태깅 JSONL 검증 리포트\n",
            f"검증 파일: {len(args.files)}개\n",
        ]
        for s in file_summaries:
            lines.append(f"- {s['file']}: {s['records']}건, 유효 {s['valid']}, 에러 {s['errors']}, 경고 {s['warnings']}\n")
        lines.append(f"\n합계: {total_records}건, 유효 {total_valid}, 에러 {len(total_errors)}, 경고 {len(total_warnings)}\n")

        lines.append("\n## issue_type_primary 분포\n")
        for k, v in primary_counter.most_common():
            lines.append(f"- {k}: {v}\n")

        lines.append("\n## confidence 분포\n")
        for k, v in confidence_counter.most_common():
            lines.append(f"- {k}: {v}\n")

        if total_errors:
            lines.append("\n## 에러\n")
            for e in total_errors:
                lines.append(f"- {e}\n")

        if total_warnings:
            lines.append("\n## 경고\n")
            for w in total_warnings:
                lines.append(f"- {w}\n")

        report_path.write_text("".join(lines), encoding="utf-8")
        print(f"\n리포트 저장: {report_path}")

    # 종료 코드
    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()
