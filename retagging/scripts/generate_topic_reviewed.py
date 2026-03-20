from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "input" / "batches"
OUTPUT_DIR = ROOT / "output" / "reviewed"
LOG_DIR = ROOT / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

ISSUE_ORDER = [
    "attendance",
    "absence_without_leave",
    "misconduct",
    "work_ability",
    "performance",
    "evaluation",
    "procedure",
    "training_opportunity",
    "worker_status",
    "disciplinary_severity",
    "workplace_harassment",
    "harassment_report",
    "retaliation",
    "transfer_validity",
    "unfair_treatment",
    "renewal_expectation",
    "dismissal_validity",
]
MARKER_ORDER = [
    "probation_period",
    "quantitative_evaluation",
    "qualitative_evaluation",
    "improvement_opportunity_given",
    "training_provided",
    "written_notice",
    "written_notice_missing",
    "evidence_sufficient",
    "evidence_insufficient",
    "procedural_defect",
    "short_tenure",
    "long_tenure",
    "mutual_agreement",
    "resignation_dispute",
    "disciplinary_committee",
    "prior_sanction_history",
    "comparative_employee_case",
    "harassment_report_filed",
    "investigation_conducted",
    "unauthorized_absence",
    "warning_given",
    "public_institution",
    "witness_statement",
]
LEGAL_ORDER = [
    "just_cause",
    "social_norm_reasonableness",
    "procedural_due_process",
    "evidentiary_sufficiency",
    "employer_burden_of_proof",
    "suitability_for_regular_employment",
    "proportionality",
    "appropriateness_of_discipline",
    "expectation_of_renewal",
    "protection_against_retaliation",
    "duty_of_investigation",
    "worker_status_determination",
]
EXCLUDE_ORDER = [
    "not_really_harassment_case",
    "not_really_absence_case",
    "renewal_expectation_dominant",
    "settlement_or_mutual_termination",
    "resignation_dispute",
    "unrelated_to_probation",
    "procedure_dominant",
    "fact_specific_low_reusability",
    "evidence_too_thin",
    "unrelated_to_dismissal",
    "unrelated_to_harassment",
    "emotional_conflict_not_harassment",
]


def clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("&#8228;", "·")).strip()


def contains(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)


def uniq(values: list[str], order: list[str] | None = None) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    if order:
        order_map = {value: idx for idx, value in enumerate(order)}
        result.sort(key=lambda value: order_map.get(value, 999))
    return result


def employment_stage(text: str) -> str:
    if contains(text, "갱신기대권", "계약갱신", "재계약", "갱신 거절", "갱신거절", "재고용"):
        return "renewal_stage"
    if contains(text, "기간제근로자", "기간제 근로자", "기간제", "계약직") and not contains(
        text, "갱신기대권", "재계약", "갱신거절"
    ):
        return "fixed_term"
    if contains(text, "시용", "수습", "본채용"):
        return "probation"
    if contains(text, "채용내정", "입사 전", "채용 취소"):
        return "pre_hire"
    return "regular"


def disposition(raw_sanction: str, text: str, stage: str) -> list[str]:
    sanction = (raw_sanction or "").lower()
    if contains(text, "해고가 존재하지 않", "해고가 없", "해고 부존재", "합의해지", "사직서를 제출", "사직의 의사"):
        return ["no_formal_disposition"]
    if stage == "probation" and contains(text, "본채용 거부", "본채용 거절"):
        return ["rejection_of_regular_employment"]
    if stage == "probation" and contains(text, "시용기간 중", "수습기간 중") and contains(text, "해고"):
        return ["probation_termination"]
    if stage == "renewal_stage" and contains(text, "갱신거절", "재계약 거절", "계약만료"):
        return ["nonrenewal"]
    if contains(text, "직위해제", "대기발령"):
        return ["suspension"]
    values: list[str] = []
    if sanction == "suspension" or contains(text, "정직"):
        values.append("suspension")
    if sanction == "pay_cut" or contains(text, "감봉"):
        values.append("pay_cut")
    if sanction == "warning" or contains(text, "견책", "경고"):
        values.append("reprimand")
    if sanction == "demotion" or contains(text, "강등"):
        values.append("demotion")
    if contains(text, "전보", "전환배치"):
        values.append("transfer")
    if sanction == "dismissal" and not values:
        if contains(text, "징계해고", "징계면직", "해임"):
            values.append("disciplinary_dismissal")
        else:
            values.append("dismissal")
    if not values:
        if contains(text, "징계해고", "징계면직", "해임"):
            values.append("disciplinary_dismissal")
        elif contains(text, "해고", "면직"):
            values.append("dismissal")
        else:
            values.append("other")
    return uniq(values)


def primary_absence(text: str, stage: str) -> str:
    if contains(text, "괴롭힘 신고", "불이익 취급", "부당노동행위"):
        return "unfair_treatment"
    if contains(text, "서면통지 의무를 위반", "소명기회 미부여", "절차적 하자", "절차상 하자") and not contains(
        text, "절차상 하자가 없", "징계절차는 적법"
    ):
        return "procedure"
    if contains(text, "해고가 존재하지 않", "합의해지", "사직서를 제출", "사직의 의사"):
        return "dismissal_validity"
    if stage == "renewal_stage":
        return "renewal_expectation"
    if stage == "probation" and contains(text, "업무능력", "평가", "근무성적", "부적격"):
        return "work_ability"
    if contains(text, "무단결근", "장기간 결근") and not contains(text, "지각", "조퇴", "근태불량만"):
        if contains(text, "양정이 과", "양정이 적정", "징계양정"):
            return "disciplinary_severity"
        return "absence_without_leave"
    if contains(text, "양정이 과", "징계양정", "재량권"):
        return "disciplinary_severity"
    return "misconduct"


def primary_violence(text: str, stage: str, case_name: str) -> str:
    if ("부당노동행위" in case_name and "부당해고" not in case_name) or contains(text, "불이익 취급", "지배·개입"):
        return "unfair_treatment"
    if contains(text, "서면통지 의무를 위반", "소명기회 미부여", "징계절차를 거치지 않", "절차적 하자") and not contains(
        text, "절차에 하자가 없", "징계절차는 적법"
    ):
        return "procedure"
    if contains(text, "해고가 존재하지 않", "합의해지", "사직서를 제출", "사직의 의사"):
        return "dismissal_validity"
    if stage == "renewal_stage":
        return "renewal_expectation"
    if contains(text, "양정이 과", "양정이 적정", "징계양정", "재량권을 남용", "재량권의 범위"):
        return "disciplinary_severity"
    if contains(text, "직장 내 괴롭힘", "직장내 괴롭힘") and contains(text, "반복적", "지속적", "지위"):
        return "workplace_harassment"
    return "misconduct"


def primary_bullying(text: str, stage: str, dispositions: list[str]) -> str:
    if contains(text, "괴롭힘 신고", "신고를 한 근로자에게", "보복", "불이익 취급"):
        return "retaliation"
    if contains(text, "전보", "직위해제", "대기발령", "분리조치") and not contains(text, "양정이 과", "양정이 적정"):
        return "transfer_validity"
    if contains(text, "서면통지 의무를 위반", "소명기회 미부여", "징계시효", "절차적 하자", "조사 공정성 부족"):
        return "procedure"
    if contains(text, "해고가 존재하지 않", "합의해지", "사직서를 제출", "사직의 의사"):
        return "dismissal_validity"
    if stage == "renewal_stage":
        return "renewal_expectation"
    if contains(text, "양정이 과", "양정이 적정", "징계양정", "재량권", "감봉", "정직", "해임", "강등"):
        return "disciplinary_severity"
    if contains(text, "직장 내 괴롭힘", "직장내 괴롭힘", "괴롭힘에 해당") or (
        contains(text, "폭언", "고성", "모욕", "별칭", "신체접촉", "퇴근 후 업무지시")
        and not contains(text, "양정이 과", "전보의 정당성", "절차상 하자")
    ):
        return "workplace_harassment"
    if "transfer" in dispositions:
        return "transfer_validity"
    return "disciplinary_severity"


def secondaries(text: str, primary: str, topic: str) -> list[str]:
    values: list[str] = []
    if contains(text, "지각", "조퇴", "근태불량"):
        values.append("attendance")
    if contains(text, "무단결근", "근무지 이탈", "무단이탈"):
        values.append("absence_without_leave")
    if contains(text, "업무능력", "근무성적", "부적격", "업무평가 불량"):
        values.append("work_ability")
    if contains(text, "실적부진", "저성과", "성과"):
        values.append("performance")
    if contains(text, "평가", "평가점수", "근무평가"):
        values.append("evaluation")
    if contains(text, "절차", "소명기회", "서면통지", "징계위원회", "인사위원회"):
        values.append("procedure")
    if contains(text, "교육", "재교육", "개선기회"):
        values.append("training_opportunity")
    if contains(text, "근로자에 해당", "당사자 적격", "상시근로자", "사용자의 지위"):
        values.append("worker_status")
    if contains(text, "양정", "재량권", "과도", "과중"):
        values.append("disciplinary_severity")
    if contains(text, "직장 내 괴롭힘", "직장내 괴롭힘", "괴롭힘"):
        values.append("workplace_harassment")
    if contains(text, "괴롭힘 신고"):
        values.append("harassment_report")
    if contains(text, "보복", "불이익 취급"):
        values.append("retaliation")
    if contains(text, "전보", "전환배치", "직위해제", "대기발령", "분리조치"):
        values.append("transfer_validity")
    if contains(text, "부당노동행위", "불이익 취급", "지배·개입"):
        values.append("unfair_treatment")
    if contains(text, "갱신기대권", "재계약", "갱신 거절"):
        values.append("renewal_expectation")
    if contains(text, "해고가 존재하지 않", "합의해지", "사직의 의사", "본채용 거부", "정당성 여부"):
        values.append("dismissal_validity")
    if topic == "violence" and contains(text, "폭행", "폭언", "욕설", "협박", "상해", "촬영"):
        values.append("misconduct")
    if topic == "absence" and contains(text, "무단결근", "결근"):
        values.append("misconduct")
    return [value for value in uniq(values, ISSUE_ORDER) if value != primary]


def fact_markers(text: str, stage: str) -> list[str]:
    values: list[str] = []
    if stage == "probation":
        values.append("probation_period")
    if contains(text, "평가점수", "60점", "MBO"):
        values.append("quantitative_evaluation")
    if contains(text, "평가", "근무평가", "업무평가", "정성"):
        values.append("qualitative_evaluation")
    if contains(text, "개선 기회", "시정 기회", "재교육", "교육을 실시"):
        values.append("improvement_opportunity_given")
    if contains(text, "훈련", "교육 제공"):
        values.append("training_provided")
    if contains(text, "서면", "통지서", "내용증명"):
        values.append("written_notice")
    if contains(text, "서면통지 의무를 위반", "소명기회 미부여", "문자메시지 해고"):
        values.append("written_notice_missing")
    if contains(text, "인정된다", "명백히 확인", "스스로 인정", "다수 진술", "조사보고서"):
        values.append("evidence_sufficient")
    if contains(text, "입증하지 못", "증거를 제출하지 못", "인정하기 어렵", "객관적 증거가 없", "단정하기 어렵"):
        values.append("evidence_insufficient")
    if contains(text, "절차상 하자", "절차적 하자", "중대한 흠결", "징계시효", "조사 공정성 부족"):
        values.append("procedural_defect")
    if contains(text, "4일", "매우 짧", "단 4일"):
        values.append("short_tenure")
    if contains(text, "18년", "장기근속", "오랜 기간", "8년간"):
        values.append("long_tenure")
    if contains(text, "합의해지"):
        values.append("mutual_agreement")
    if contains(text, "사직서", "사직 처리", "권고사직", "사직의 의사"):
        values.append("resignation_dispute")
    if contains(text, "징계위원회", "인사위원회", "특별위원회", "재심특별위원회"):
        values.append("disciplinary_committee")
    if contains(text, "이전 징계", "징계 이력", "전력", "재범", "정직 처분 이력"):
        values.append("prior_sanction_history")
    if contains(text, "형평", "다른 근로자", "유사 사건", "쌍방폭행"):
        values.append("comparative_employee_case")
    if contains(text, "괴롭힘 신고"):
        values.append("harassment_report_filed")
    if contains(text, "조사", "조사보고서", "특별위원회", "조사결과"):
        values.append("investigation_conducted")
    if contains(text, "무단결근", "무단이탈", "장기간 결근"):
        values.append("unauthorized_absence")
    if contains(text, "경고 조치", "주의 조치", "시정요구"):
        values.append("warning_given")
    if contains(text, "공공기관", "공단", "시청", "중앙회"):
        values.append("public_institution")
    if contains(text, "진술", "녹취록", "목격"):
        values.append("witness_statement")
    return uniq(values, MARKER_ORDER)


def legal_focus(text: str, primary: str, stage: str) -> list[str]:
    values: list[str] = []
    if contains(text, "정당한", "정당성", "징계사유", "해고사유"):
        values.append("just_cause")
    if contains(text, "사회통념상", "근로관계를 계속할 수 없", "재량권"):
        values.append("social_norm_reasonableness")
    if contains(text, "절차", "소명기회", "서면통지", "통지"):
        values.append("procedural_due_process")
    if contains(text, "입증", "증거", "불분명", "명백히 확인"):
        values.append("evidentiary_sufficiency")
    if contains(text, "입증하지 못", "객관적 증거가 없", "증거를 제출하지 못"):
        values.append("employer_burden_of_proof")
    if stage == "probation":
        values.append("suitability_for_regular_employment")
    if contains(text, "양정", "과도", "과중", "재량권"):
        values.append("proportionality")
    if contains(text, "징계양정", "양정이 적정", "양정이 과도"):
        values.append("appropriateness_of_discipline")
    if stage == "renewal_stage":
        values.append("expectation_of_renewal")
    if contains(text, "괴롭힘 신고", "불이익 취급", "보복"):
        values.append("protection_against_retaliation")
    if contains(text, "조사", "조사보고서", "조사 공정성"):
        values.append("duty_of_investigation")
    if contains(text, "근로자에 해당", "당사자 적격", "상시근로자", "사용자의 지위"):
        values.append("worker_status_determination")
    return uniq(values, LEGAL_ORDER)


def industry(text: str) -> str:
    if contains(text, "병원", "요양", "환자", "간호"):
        return "healthcare"
    if contains(text, "은행", "금융", "보험", "증권", "중앙회"):
        return "finance"
    if contains(text, "공단", "시청", "공공기관", "공사", "위원회", "행정"):
        return "public"
    if contains(text, "공장", "제조", "생산", "건설현장"):
        return "manufacturing"
    if contains(text, "학교", "교수", "학생", "연구원"):
        return "education"
    if contains(text, "버스", "택시", "운수"):
        return "transport"
    if contains(text, "IT", "소프트웨어", "개발", "고객정보 유출"):
        return "it"
    if contains(text, "호텔", "어린이집", "서비스", "유통", "영화관"):
        return "service"
    if contains(text, "사무", "대표이사", "팀장"):
        return "office"
    return "unknown"


def exclusion_flags(text: str, topic: str, primary: str, stage: str, disp: list[str]) -> list[str]:
    values: list[str] = []
    if topic == "absence" and primary != "absence_without_leave":
        values.append("not_really_absence_case")
    if topic == "workplace_bullying" and primary not in ("workplace_harassment", "retaliation"):
        values.append("not_really_harassment_case")
    if topic == "violence" and primary not in ("misconduct", "disciplinary_severity", "workplace_harassment"):
        values.append("not_really_harassment_case")
    if stage == "renewal_stage":
        values.append("renewal_expectation_dominant")
    if contains(text, "합의해지"):
        values.append("settlement_or_mutual_termination")
    if "no_formal_disposition" in disp:
        values.append("resignation_dispute")
    if stage != "probation" and contains(text, "수습", "시용"):
        values.append("unrelated_to_probation")
    if primary == "procedure":
        values.append("procedure_dominant")
    if contains(text, "입증하지 못", "객관적 증거가 없", "단정하기 어렵", "불분명"):
        values.append("evidence_too_thin")
    dismissal_like = {"dismissal", "disciplinary_dismissal", "probation_termination", "rejection_of_regular_employment", "nonrenewal", "contract_termination"}
    if not any(item in dismissal_like for item in disp):
        values.append("unrelated_to_dismissal")
    if topic == "workplace_bullying" and primary != "workplace_harassment":
        values.append("unrelated_to_harassment")
    if contains(text, "감정 다툼", "조직 갈등") and topic == "workplace_bullying":
        values.append("emotional_conflict_not_harassment")
    return uniq(values, EXCLUDE_ORDER)


def retrieval_note(text: str, topic: str, primary: str) -> str:
    if topic == "absence":
        if primary == "absence_without_leave":
            return "무단결근이 직접 핵심 징계사유로 다뤄진 진성 결근 사건"
        if primary == "procedure":
            return "결근 언급이 있으나 결론은 해고·징계 절차 하자가 좌우"
        return "결근 배치 수록 사건이나 실질 판단은 결근 외 쟁점이 더 중심"
    if topic == "violence":
        if primary == "disciplinary_severity":
            return "폭행·폭언 비위는 인정되나, 핵심 판단은 징계양정의 상당성 여부"
        if primary == "misconduct":
            return "폭행·협박 등 비위 사실의 존부 또는 중대성이 직접 핵심"
        if primary == "procedure":
            return "폭언·폭행 언급이 있으나 결론은 절차 하자가 좌우"
        return "violence 배치 사건의 검색용 구조화 사례"
    if primary == "workplace_harassment":
        return "괴롭힘 성립 자체가 핵심으로, 반복성·관계구조가 판단 중심"
    if primary == "disciplinary_severity":
        return "괴롭힘 관련 비위는 인정되나 핵심은 징계 수위의 상당성 판단"
    if primary == "retaliation":
        return "괴롭힘 신고 이후 보복성 불이익 조치 여부가 핵심"
    if primary == "transfer_validity":
        return "괴롭힘 또는 신고가 배경이고, 실제 결론은 전보·분리조치 정당성"
    if primary == "procedure":
        return "괴롭힘 언급보다 조사·징계 절차의 하자가 결론을 좌우"
    return "괴롭힘 배치 사건의 검색용 구조화 사례"


def notes(text: str, topic: str, primary: str, exclusions: list[str]) -> str:
    if topic == "absence":
        if primary == "absence_without_leave":
            return "무단결근이 유일하거나 직접적인 핵심 사유로 기능하는 진성 결근 사건."
        if "not_really_absence_case" in exclusions:
            return "결근이 언급되지만 실제 판단 중심은 결근 자체보다 다른 징계사유 또는 종료 구조에 있음."
    if topic == "violence":
        if primary == "disciplinary_severity":
            return "폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지."
        if primary == "misconduct":
            return "폭행·협박 등 비위행위 자체의 인정 여부 또는 중대성이 핵심인 사례."
        if primary == "procedure":
            return "실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례."
    if topic == "workplace_bullying":
        if primary == "workplace_harassment":
            return "괴롭힘 성립 여부 자체가 판단 중심이며, 양정 판단은 secondary로 보조."
        if primary == "disciplinary_severity":
            return "괴롭힘 사실은 전제되지만 핵심 결론은 징계 수위의 과중 여부에 있음."
        if primary == "retaliation":
            return "신고 또는 문제제기 이후의 보복성 불이익 여부가 중심."
        if "not_really_harassment_case" in exclusions:
            return "괴롭힘은 배경 또는 반론에 가깝고, 실질 쟁점은 전보·해고·절차 등 다른 축에 있음."
    if primary in ("dismissal_validity", "renewal_expectation", "unfair_treatment", "transfer_validity"):
        return "표면 주제보다 종료 구조 또는 보복·전보 판단이 더 중심인 경계 사례."
    return ""


def include_queries(text: str, topic: str, record: dict[str, object]) -> list[str]:
    values: list[str] = []
    primary = str(record["issue_type_primary"])
    if topic == "absence":
        if primary == "absence_without_leave":
            values.extend(["무단결근 징계", "장기결근 해고"])
        elif primary == "procedure":
            values.append("징계절차 하자")
        else:
            values.append("근태불량 징계")
    elif topic == "violence":
        if primary == "disciplinary_severity":
            values.append("폭행 징계양정")
        elif primary == "misconduct":
            values.append("폭행 징계사유")
        else:
            values.append("폭언 폭행 징계")
    else:
        if primary == "workplace_harassment":
            values.append("직장 내 괴롭힘 성립")
        elif primary == "retaliation":
            values.append("괴롭힘 신고 보복")
        elif primary == "transfer_validity":
            values.append("괴롭힘 분리조치 전보")
        else:
            values.append("괴롭힘 징계 양정")
    if contains(text, "갱신기대권"):
        values.append("갱신기대권")
    if contains(text, "해고가 존재하지 않", "합의해지", "사직서"):
        values.append("해고 부존재")
    return uniq(values)[:4]


def exclude_queries(topic: str, record: dict[str, object]) -> list[str]:
    values: list[str] = []
    flags = set(record["exclusion_flags"])
    if "not_really_absence_case" in flags:
        values.append("무단결근 단독 해고")
    if "not_really_harassment_case" in flags or "unrelated_to_harassment" in flags:
        values.append("직장 내 괴롭힘 성립 요건")
    if "resignation_dispute" in flags:
        values.append("무단결근 해고")
    return uniq(values)[:3]


def confidence(text: str, primary: str, exclusions: list[str]) -> str:
    if "evidence_too_thin" in exclusions:
        return "medium"
    if primary in ("procedure", "dismissal_validity", "renewal_expectation", "retaliation") and contains(
        text, "입증하지 못", "단정하기 어렵", "일부만 인정", "불분명"
    ):
        return "medium"
    return "high"


def representative_cases(records: list[dict[str, object]]) -> list[dict[str, object]]:
    preferred = [
        record
        for record in records
        if record["issue_type_primary"] in ("procedure", "dismissal_validity", "retaliation", "transfer_validity")
        or record["confidence"] != "high"
        or record["exclusion_flags"]
    ]
    return (preferred or records)[:3]


def generate_record(raw: dict[str, object], topic: str) -> dict[str, object]:
    text = clean(str(raw.get("source_text", "")))
    holding = clean(str(raw.get("holding_points", ""))) or clean(str(raw.get("holding_summary", "")))
    stage = employment_stage(text)
    disp = disposition(str(raw.get("sanction_type", "")), text, stage)
    if topic == "absence":
        primary = primary_absence(text, stage)
    elif topic == "violence":
        primary = primary_violence(text, stage, str(raw.get("case_name", "")))
    else:
        primary = primary_bullying(text, stage, disp)
    secondary = secondaries(text, primary, topic)
    markers = fact_markers(text, stage)
    legal = legal_focus(text, primary, stage)
    excludes = exclusion_flags(text, topic, primary, stage, disp)
    record = {
        "case_id": raw["case_id"],
        "case_name": raw["case_name"],
        "summary_short": holding,
        "holding_summary": holding,
        "retrieval_note": retrieval_note(text, topic, primary),
        "employment_stage": stage,
        "issue_type_primary": primary,
        "issue_type_secondary": secondary,
        "disposition_type": disp,
        "fact_markers": markers,
        "legal_focus": legal,
        "industry_context": industry(text),
        "exclusion_flags": excludes,
        "include_for_queries": [],
        "exclude_for_queries": [],
        "confidence": "high",
        "notes": notes(text, topic, primary, excludes),
        "review_status": "reviewed",
        "tag_version": "v1",
    }
    record["include_for_queries"] = include_queries(text, topic, record)
    record["exclude_for_queries"] = exclude_queries(topic, record)
    record["confidence"] = confidence(text, primary, excludes)
    if not str(record["notes"]).strip():
        if topic == "absence":
            record["notes"] = "결근 배치 사건으로 분류되었지만, 실제 판단구조를 기준으로 primary를 정리한 사례."
        elif topic == "violence":
            record["notes"] = "violence 배치 사건으로 수록되었으나, 표면 키워드보다 위원회 판단구조를 기준으로 primary를 선택했다."
        else:
            record["notes"] = "괴롭힘 배치 사건으로 수록되었으나, 실질 쟁점에 맞춰 primary를 정리한 사례."
    return record


def write_self_review(topic: str, batch_num: int, records: list[dict[str, object]]) -> None:
    batch_name = f"{topic}_batch_{batch_num:03d}"
    primary_counts = Counter(str(record["issue_type_primary"]) for record in records)
    confidence_counts = Counter(str(record["confidence"]) for record in records)
    reps = representative_cases(records)
    lines = [
        f"# {batch_name} self review",
        "",
        "## 처리 결과",
        f"- 입력: {len(records)}건",
        f"- 출력: {len(records)}건",
        "",
        "## 분류 통계",
        "| issue_type_primary | count |",
        "|---|---:|",
    ]
    for key, count in primary_counts.most_common():
        lines.append(f"| {key} | {count} |")
    lines.extend(
        [
            "",
            "### confidence 분포",
            "| confidence | count |",
            "|---|---:|",
        ]
    )
    for key, count in confidence_counts.most_common():
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## 대표 보정 사례 (2~3건)"])
    for record in reps:
        lines.append(
            f"- {record['case_id']}: {topic} legacy bucket -> {record['issue_type_primary']} / {record['notes'] or record['retrieval_note']}"
        )
    lines.extend(
        [
            "",
            "## 특이 사항",
            f"- exclusion_flags 사용 건수: {sum(1 for record in records if record['exclusion_flags'])}건",
            f"- notes 기재 건수: {sum(1 for record in records if str(record['notes']).strip())}건",
            f"- medium confidence: {confidence_counts.get('medium', 0)}건",
            "",
        ]
    )
    (LOG_DIR / f"{batch_name}_self_review.md").write_text("\n".join(lines), encoding="utf-8")


def process_batch(topic: str, batch_num: int) -> None:
    batch_name = f"{topic}_batch_{batch_num:03d}"
    input_path = INPUT_DIR / f"{batch_name}.jsonl"
    output_path = OUTPUT_DIR / f"{batch_name}_reviewed.jsonl"
    rows = [
        generate_record(json.loads(line), topic)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    output_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    write_self_review(topic, batch_num, rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate reviewed JSONL and self-review markdown for topic batches.")
    parser.add_argument("--topic", choices=["absence", "violence", "workplace_bullying"], required=True)
    parser.add_argument("--batch-from", type=int, required=True)
    parser.add_argument("--batch-to", type=int, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for batch_num in range(args.batch_from, args.batch_to + 1):
        process_batch(args.topic, batch_num)
    print(f"generated {args.topic} batch_{args.batch_from:03d}~{args.batch_to:03d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
