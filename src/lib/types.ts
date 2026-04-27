export type ReasonCategory =
  | "sexual_harassment"
  | "workplace_bullying"
  | "violence"
  | "absence"
  | "embezzlement"
  | "incompetence"
  | "misconduct"
  | "redundancy"
  | "probation"
  | "transfer"
  | "contract_expiry"
  | "no_dismissal"
  | "union_activity"
  | "worker_status"
  | "discrimination"
  | "other";

export type DecisionResult =
  | "granted"
  | "dismissed"
  | "rejected"
  | "upheld"
  | "overturned"
  | "partial"
  | "settled";

export type SanctionType =
  | "dismissal"
  | "suspension"
  | "pay_cut"
  | "warning"
  | "demotion"
  | "other";

export interface NlrcDecision {
  id: string;
  title: string;
  case_number: string;
  department: string;
  decision_date: string;
  case_type: string;
  reason_category: ReasonCategory[];
  reason_detail: string;
  procedure_committee: boolean;
  procedure_defense: boolean;
  procedure_written_notice: boolean;
  procedure_advance_notice: boolean;
  procedure_note: string;
  sanction_type: SanctionType;
  decision_result: DecisionResult;
  key_issue: string;
  holding_points: string;
  holding_summary: string;
  url: string;
  tags: string[];
}

export const REASON_LABELS: Record<ReasonCategory, string> = {
  sexual_harassment: "성희롱",
  workplace_bullying: "직장내괴롭힘",
  violence: "폭언/폭행",
  absence: "무단결근/태만",
  embezzlement: "횡령/배임",
  incompetence: "업무능력부족",
  misconduct: "비위행위",
  redundancy: "경영상해고",
  probation: "수습해고",
  transfer: "전보/인사이동",
  contract_expiry: "갱신기대권/계약만료",
  no_dismissal: "해고부존재/사직",
  union_activity: "부당노동행위",
  worker_status: "근로자성 분쟁",
  discrimination: "차별시정",
  other: "기타",
};

export const RESULT_LABELS: Record<DecisionResult, string> = {
  granted: "인정 (구제)",
  dismissed: "기각",
  rejected: "각하",
  upheld: "초심유지",
  overturned: "초심취소",
  partial: "일부인정",
  settled: "화해/취하",
};

export const SANCTION_LABELS: Record<SanctionType, string> = {
  dismissal: "해고",
  suspension: "정직",
  pay_cut: "감봉",
  warning: "경고/견책",
  demotion: "강등",
  other: "기타",
};

// reason_category 분류 완료 (42,105건) — reason_category 컬럼으로 직접 검색
// REASON_TO_TAGS는 태그 기반 fallback용으로만 유지
export const REASON_TO_TAGS: Record<ReasonCategory, string[]> = {
  sexual_harassment: ["성희롱"],
  workplace_bullying: ["직장내괴롭힘"],
  violence: ["징계해고", "징계양정"],
  absence: ["징계해고"],
  embezzlement: ["징계해고"],
  incompetence: ["해고사유"],
  misconduct: ["징계해고", "징계양정"],
  redundancy: ["부당해고"],
  probation: ["수습"],
  transfer: ["전보"],
  contract_expiry: ["갱신기대권", "비정규직"],
  no_dismissal: ["해고부존재", "사직", "권고사직"],
  union_activity: ["부당노동행위", "지배개입", "불이익취급"],
  worker_status: ["근로자성", "당사자적격"],
  discrimination: ["차별시정"],
  other: [],
};

// ─── 사용자 노출용 한글 라벨 (영문 컬럼값 → 한글) ──────────────────────────────
// DB 키는 영문 그대로 두되, 화면 렌더 시 매핑. 미매핑은 fallback으로 원문 노출.

export const LEGAL_FOCUS_LABELS: Record<string, string> = {
  anti_union_domination: "지배·개입",
  anti_union_intent: "반조합 의도",
  appropriateness_of_discipline: "징계 양정 적정성",
  automatic_termination: "당연퇴직",
  business_necessity: "업무상 필요성",
  business_necessity_test: "업무상 필요성 판단",
  collective_agreement: "단체협약",
  consultation_procedure: "협의 절차",
  consultation_requirement_source: "협의 의무 근거",
  disciplinary_action_definition: "징계 처분 해당 여부",
  disciplinary_proportionality: "징계 비례성",
  discrimination_prohibition: "차별 금지",
  dismissal_existence: "해고 존재 여부",
  double_jeopardy_denial: "이중 처벌 금지",
  duty_of_investigation: "조사 의무",
  employer_burden_of_proof: "사용자 입증책임",
  employment_condition_violation: "근로조건 위반",
  evidentiary_sufficiency: "증거의 충분성",
  expectation_of_renewal: "갱신기대권",
  fair_representation_duty: "공정대표의무",
  financial_compensation_order: "금전보상명령",
  just_cause: "정당한 이유",
  labor_commission_jurisdiction: "노동위 관할",
  party_standing: "당사자적격",
  procedural_due_process: "절차적 정당성",
  procedural_requirements: "절차 요건",
  proportionality: "비례원칙",
  protection_against_retaliation: "보복조치 금지",
  refusal_to_bargain: "교섭 거부",
  relief_interest: "구제이익",
  social_norm_reasonableness: "사회통념상 상당성",
  statute_of_limitations: "제척기간",
  strike_action_legality: "쟁의행위 정당성",
  suitability_for_regular_employment: "본채용 적격성",
  supervisory_responsibility: "감독자 책임",
  time_off_for_union_work: "노조 활동 면제시간",
  transfer_3prong_test: "전보 3요건 심사",
  transfer_validity_3prong: "전보 정당성 3요건",
  unfair_labor_practice: "부당노동행위",
  unfair_labor_practice_transfer: "부당노동행위(전보)",
  worker_classification: "근로자 분류",
  worker_status_determination: "근로자성 판단",
  written_notice_requirement: "서면통지 요건",
};

export const DISPOSITION_TYPE_LABELS: Record<string, string> = {
  contract_termination: "근로계약 종료",
  demotion: "강등",
  discipline_invalid: "부당징계",
  disciplinary_dismissal: "징계해고",
  dismissal: "해고",
  dismissed: "기각",
  granted: "인용",
  no_formal_disposition: "처분 없음",
  nonrenewal: "갱신 거절",
  other: "기타",
  overturned: "초심취소",
  pay_cut: "감봉",
  probation_termination: "수습해지",
  rejected: "기각",
  rejection_of_regular_employment: "본채용 거부",
  reprimand: "견책",
  strike_action: "쟁의행위",
  suspension: "정직",
  transfer: "전보",
  transfer_invalid: "부당전보",
  transfer_order: "전보 명령",
  transfer_valid: "정당한 전보",
  upheld: "초심유지",
  warning: "경고",
};

export const FACT_MARKER_LABELS: Record<string, string> = {
  back_pay_paid: "임금상당액 지급",
  bargaining_refusal: "교섭 거부",
  business_necessity_proven: "업무상 필요성 입증",
  business_necessity_recognized: "업무상 필요성 인정",
  cba_clause: "단체협약 조항",
  comparative_employee_case: "유사 사례 비교",
  conflicting_authority: "권한 충돌",
  consent_not_required: "동의 불요",
  consultation_conducted: "협의 진행",
  consultation_held: "협의 실시",
  consultation_not_conducted: "협의 미실시",
  continuous_absence: "연속 결근",
  contract_terms_changed: "근로조건 변경",
  contractual_transfer_clause: "전보 약정 조항",
  coworker_conflict: "동료 갈등",
  daily_hardship_within_normal_range: "통상범위 내 생활 불편",
  disciplinary_committee: "징계위원회 개최",
  disciplinary_grounds_found: "징계사유 인정",
  disciplinary_grounds_rejected: "징계사유 부인",
  disciplinary_grounds_rejected_partial: "징계사유 일부 부인",
  disguised_forced_resignation: "위장 권고사직",
  dismissal_exists: "해고 존재",
  dismissal_found_unfair: "해고 부당 인정",
  dismissal_found_unilateral: "일방적 해고 인정",
  emotional_conflict_only: "감정적 갈등에 그침",
  employer_identity_confirmed: "사용자 확정",
  employment_ended: "근로관계 종료",
  evidence_insufficient: "증거 부족",
  evidence_sufficient: "증거 충분",
  exclusion_period: "제척기간",
  filing_period_expired: "제소기간 도과",
  five_or_more_employees: "상시 5인 이상",
  harassment_report_filed: "괴롭힘 신고 접수",
  historical_practice: "관행",
  improvement_opportunity_given: "개선 기회 부여",
  inadequate_business_necessity: "업무상 필요성 부족",
  industry_specific_long_distance_transfer: "업종 특성 장거리 전보",
  initial_finding_overturned: "초심 취소",
  insufficient_evidence: "증거 불충분",
  inter_company_transfer: "관계회사 전보",
  investigation_conducted: "조사 실시",
  job_function_inability: "업무수행 불가",
  labor_board_filing_retaliation: "노동위 제소 보복",
  legitimate_rights_exercise_punished: "정당한 권리행사 징계",
  license_revocation: "자격 취소",
  living_disadvantage_within_normal_range: "통상범위 내 생활상 불이익",
  long_tenure: "장기 근속",
  management_failure: "경영 실패",
  minimal_life_disruption: "생활 영향 미미",
  minor_commute_increase: "출퇴근 가중 경미",
  minority_union: "소수 노조",
  monetary_compensation_incidental: "금전보상 부수",
  monitoring_order: "감독 명령",
  moonlighting_misconduct: "겸직 비위",
  multiple_transfer_attempts: "반복 전보 시도",
  mutual_agreement: "합의",
  mutual_agreement_termination: "합의 해지",
  new_transfer_order_issued: "재전보 명령",
  no_anti_union_intent: "반조합 의도 없음",
  no_business_necessity: "업무상 필요성 없음",
  no_consent: "동의 없음",
  no_disciplinary_grounds: "징계사유 없음",
  no_dismissal_found: "해고 부존재",
  no_equity_issue: "형평성 문제 없음",
  no_procedural_defect: "절차 하자 없음",
  no_significant_hardship: "현저한 불이익 없음",
  no_unfair_labor_practice: "부당노동행위 부인",
  no_written_notice: "서면통지 없음",
  ordinary_wage_dispute: "통상임금 분쟁",
  outside_jurisdiction: "관할 외",
  partial_relief_interest_extinguished: "구제이익 일부 소멸",
  prior_sanction_history: "징계 전력",
  pro_union_statement: "친조합 발언",
  probation_period: "수습기간",
  probation_refusal_is_dismissal: "본채용 거부=해고",
  procedural_defect: "절차상 하자",
  procedure_followed: "절차 준수",
  proportionate_sanction: "비례적 징계",
  proportionality_violated: "비례원칙 위반",
  public_institution: "공공기관",
  qualitative_evaluation: "정성 평가",
  quantitative_evaluation: "정량 평가",
  reinstatement_order_genuine: "원직복직명령 진정",
  relief_interest_extinguished: "구제이익 소멸",
  relief_interest_lapsed: "구제이익 상실",
  repeated_absence: "반복 결근",
  resignation_dispute: "사직 분쟁",
  retaliatory_transfer: "보복성 전보",
  severe_life_disruption: "현저한 생활 곤란",
  short_tenure: "단기 근속",
  six_month_tenure: "6개월 근속",
  suspension_without_cause: "이유 없는 정직",
  time_off_violation: "면제시간 위반",
  training_provided: "교육 제공",
  transfer_after_refused_resignation: "사직 거부 후 전보",
  transfer_order: "전보 명령",
  transfer_upheld: "전보 정당",
  travel_expense_customary: "출장비 관행",
  unauthorized_absence: "무단 결근",
  unfavorable_working_conditions: "불리한 근로조건",
  victim_claim: "피해자 주장",
  warning_given: "경고 부여",
  witness_statement: "증언",
  written_notice: "서면통지",
  written_notice_missing: "서면통지 누락",
};

// 미매핑 키 fallback: 원문 그대로 출력 (감지/추가용)
export function labelize(value: string, dict: Record<string, string>): string {
  return dict[value] ?? value;
}
