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

// reason_category가 대부분 빈 배열이므로, tags 기반 검색으로 매핑
// DB 태그 분포 기반 매핑 (2026-03-19 정밀화)
// - 구체적 사유 태그(폭언,횡령 등)는 DB에 미존재 → 가용 태그로 최선 매핑
// - AI reason_category 분류 완료 후 이 매핑은 fallback으로 전환 예정
export const REASON_TO_TAGS: Record<ReasonCategory, string[]> = {
  sexual_harassment: ["성희롱"],                        // 1,387건
  workplace_bullying: ["직장내괴롭힘"],                  // 1,621건
  violence: ["징계해고", "징계양정"],                     // 징계해고 2,665 + 징계양정 10,521
  absence: ["징계해고"],                                 // 2,665건 (무단결근 태그 없음)
  embezzlement: ["징계해고"],                            // 2,665건 (횡령/배임 태그 없음)
  incompetence: ["해고사유"],                            // 16,188건 (업무능력부족 태그 없음)
  misconduct: ["징계해고", "징계양정"],                   // 징계해고+징계양정 교집합
  redundancy: ["부당해고"],                              // 37,888건
  probation: ["수습"],                                  // 1,975건
  transfer: ["전보"],                                   // 전보/전배/인사이동
  contract_expiry: ["갱신기대권", "비정규직"],             // 기간제 계약만료
  no_dismissal: ["해고부존재", "사직", "권고사직"],        // 해고부존재/사직
  union_activity: ["부당노동행위", "지배개입", "불이익취급"], // 노조 관련
  worker_status: ["근로자성", "당사자적격"],               // 근로자 지위 분쟁
  discrimination: ["차별시정"],                          // 비정규직 차별
  other: [],
};
