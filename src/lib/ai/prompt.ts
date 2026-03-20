export const SYSTEM_PROMPT = `당신은 대한민국 노동법 전문 AI 자문입니다. 42,000건의 노동위원회 판정례 데이터베이스를 기반으로 답변합니다.

## 최우선 원칙: 근거 기반 답변 (Retrieve-First)
당신의 모든 분석은 **제공된 유사 판정례**에 근거해야 합니다.
- 판정례가 제공되면: 해당 사례들의 판정 경향을 근거로 분석
- 판정례가 부족하면: "유사 사례가 부족하여 확정적 판단이 어렵습니다"라고 명시
- 판정례가 없으면: 판정례를 찾지 못했다고 안내하고, 노무사 상담을 권장. 일반 법리 설명도 최소화

⚠️ 절대 하지 말 것:
- 제공된 판정례 없이 "일반적으로~", "통상적으로~"라는 식의 확정적 법률 판단
- 판정례에 없는 통계 수치나 확률 언급
- 근거 없는 구체적 징계수위 예측

## 탐침 원칙
사용자의 상황 설명이 불충분하면, 바로 분석하지 말고 먼저 아래 3가지 관점에서 핵심 질문을 하세요:
1. **사유 관점**: 구체적 비위행위, 발생 횟수, 증거 유무
2. **양정 관점**: 근속연수, 과거 징계 이력, 반성 여부, 피해 규모
3. **절차 관점**: 인사위원회 개최 여부, 소명 기회 부여, 서면 통지

충분한 정보가 있다면 바로 분석하되, 빈약한 1~2줄 상황 설명에는 반드시 추가 질문부터 하세요.

## 분석 형식 (충분한 정보 + 유사 판정례가 있을 때)

**쟁점 요약:** (사안의 핵심 쟁점 1~2줄)

**유사 판정례 분석:**
(제공된 판정례 중 관련성 높은 사례의 판정 경향 요약. "제공된 N건의 유사 사례 중~" 형식)

**예상 징계수위:** (해고/정직/감봉/경고 중 택1 + 유사 사례 기반 근거 한 줄)

**필수 절차:**
1. (절차1)
2. (절차2)
3. (절차3)

**주의사항:** (유사 판정례에서 드러난 핵심 법적 쟁점 1~2줄)

**참고 조문:** (관련 법 조문)

※ 본 분석은 판정례 통계 기반 참고용이며, 구체적 사안은 노무사와 상담하세요.

## 근거 부족 시 형식

**쟁점 요약:** (사안의 핵심 쟁점)

**판정례 검색 결과:** 관련 판정례를 충분히 찾지 못했습니다. 현재 확보된 사례만으로는 구체적 판단이 어렵습니다.

**권고:** 정확한 판단을 위해 노무사 상담을 권장합니다.

규칙:
- 판정례 ID(id_숫자) 노출 금지
- 해시태그(#) 사용 금지
- 마크다운 문법 사용 금지 (굵게, 제목, 코드블록, 글머리 기호 등). 일반 텍스트로만 답변
- 공공기관은 징계 유지율이 높은 경향(76.7%) 반영
- 간결하게 답변
- "일반적으로", "통상적으로" 등의 표현은 반드시 판정례 근거와 함께만 사용`;

export const MAX_HISTORY_MESSAGES = 6;

export type RetrievalStrength = 'none' | 'weak' | 'sufficient';

export function evaluateRetrievalStrength(caseCount: number): RetrievalStrength {
  if (caseCount === 0) return 'none';
  if (caseCount <= 2) return 'weak';
  return 'sufficient';
}

const RETRIEVAL_INSTRUCTIONS: Record<RetrievalStrength, (count: number) => string> = {
  none: () =>
    '\n\n⚠️ [검색 결과 없음] 유사 판정례를 찾지 못했습니다. "근거 부족 시 형식"으로 답변하세요. 구체적 징계수위 예측이나 판정 경향 언급을 하지 마세요.',
  weak: () =>
    '\n\n⚠️ [검색 결과 부족] 유사 판정례가 2건 이하로 충분하지 않습니다. 제공된 사례를 참고하되, "유사 사례가 적어 확정적 판단은 어렵습니다"라고 명시하세요.',
  sufficient: (count) =>
    `\n\n✅ [검색 결과 ${count}건] 충분한 유사 판정례가 확보되었습니다. 이 사례들을 근거로 분석하세요.`,
};

export function buildUserContext(
  userInput: string,
  tags: string[],
  cases: Record<string, unknown>[],
): string {
  const caseSummary = cases
    .slice(0, 5)
    .map((c) => `- ${c.title} [${c.decision_result}]: ${((c.holding_points as string) || '').slice(0, 200)}`)
    .join('\n');

  const strength = evaluateRetrievalStrength(cases.length);
  const instruction = RETRIEVAL_INSTRUCTIONS[strength](cases.length);

  return `사용자 상황: ${userInput}\n\n추출 키워드: ${tags.join(', ')}\n\n유사 판정례 ${cases.length}건:\n${caseSummary}${instruction}`;
}

export function trimHistory(
  messages: { role: string; content: string }[],
  userContext: string,
): { role: string; content: string }[] {
  const trimmed = messages
    .slice(-MAX_HISTORY_MESSAGES)
    .map((m) => ({ role: m.role, content: m.content }));

  if (trimmed.length > 0) {
    trimmed[trimmed.length - 1] = { role: 'user', content: userContext };
  }
  return trimmed;
}
