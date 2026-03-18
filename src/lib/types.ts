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
  other: "기타",
};
