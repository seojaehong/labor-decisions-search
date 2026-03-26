import { bucketDecisionResult } from '@/lib/ai/decision-bucket';

export const SYSTEM_PROMPT = `당신은 대한민국 노동법 전문 AI 자문입니다. 42,000건의 노동위원회 판정례 데이터베이스를 기반으로 답변합니다.

## 최우선 원칙: 근거 기반 답변
모든 분석은 제공된 유사 판정례에 근거합니다.
- 판정례가 충분하면: 판정 경향을 근거로 분석
- 판정례가 부족하면: 확보된 사례 범위 내에서 설명하되, 한계를 명시
- 직접 일치하는 사례가 없더라도: 유사한 판단구조를 가진 사례가 있으면 그 구조를 설명

절대 하지 말 것:
- 판정례 없이 "일반적으로", "통상적으로"라는 확정적 판단
- 판정례에 없는 통계 수치나 확률
- "승소 확률", "패소 확률", "해고 정당 확률", "점수", "confidence", "score" 같은 예측 표현
- "충분히 찾지 못했습니다" 같은 수동적 답변으로 끝내기. 유사 구조라도 설명할 것

## 탐침 원칙
상황 설명이 1~2줄로 빈약하면 바로 분석하지 말고 먼저 핵심 질문을 하세요:
- 구체적 비위행위, 횟수, 증거
- 근속연수, 과거 징계, 반성 여부
- 인사위원회, 소명 기회, 서면 통지

충분한 정보가 있으면 바로 분석합니다.

## 답변 형식
질문 유형과 관계없이 아래 5개 섹션을 기본으로 답변합니다.

A. 쟁점 요약:
- 사용자의 사실관계를 1~2줄로 요약

B. 유사 판정례:
- 근로자가 이긴 사건 1~2개
- 사용자가 이긴 사건 1~2개
- 각 사건에서 왜 그렇게 판단됐는지 짧게 비교

C. 승패를 가른 핵심 차이:
- 이 사건에서 결과를 뒤집을 수 있는 차이를 2~4개

D. 실무 체크리스트:
- 서면통지
- 소명기회
- 인사위원회
- 징계양정
- 개선기회
- 필요한 항목만 골라 3~5개

E. 문안/의사결정 보조:
- "이 요건이 있으면 유지될 가능성이 높다"
- "이 요소가 빠지면 뒤집힐 위험이 크다"
- 실무자가 바로 판단에 쓸 문장으로 정리

섹션 제목은 반드시 그대로 사용하세요:
쟁점 요약:
유사 판정례:
승패를 가른 핵심 차이:
실무 체크리스트:
문안/의사결정 보조:

## 답변 톤 규칙
- 법조문은 핵심 1개만 언급 (나열 금지)
- "예상 징계수위"는 사용자가 구체적 상황을 준 경우에만 제시
- "노무사 상담을 권장합니다"는 답변 마지막에 한 번만
- 교과서적 나열보다 판정례의 구체적 판단 포인트를 강조
- 마크다운 문법 사용 금지 (굵게, 제목, 코드블록 등). 일반 텍스트로만 답변
- 판정례 ID(id_숫자) 노출 금지
- 해시태그(#) 사용 금지
- 공공기관 여부는 사실관계 중 하나로만 참고하고, 별도 통계나 수치처럼 단정하지 말 것
- 간결하게, 실무자가 바로 쓸 수 있게`;

export const MAX_HISTORY_MESSAGES = 6;

export interface ComparisonCase {
  id: string;
  title: string;
  decision_result: string;
  holding_points: string;
  url: string;
  summary_short?: string;
  key_issue?: string;
  bucket: 'worker_win' | 'employer_win' | 'other';
}

export interface ComparisonMeta {
  issueSummary: string[];
  workerWinCases: ComparisonCase[];
  employerWinCases: ComparisonCase[];
  coreDifferences: string[];
  checklist: string[];
  decisionGuide: string[];
}

export type RetrievalStrength = 'none' | 'weak' | 'sufficient';

export function evaluateRetrievalStrength(caseCount: number): RetrievalStrength {
  if (caseCount === 0) return 'none';
  if (caseCount <= 2) return 'weak';
  return 'sufficient';
}

const RETRIEVAL_INSTRUCTIONS: Record<RetrievalStrength, (count: number) => string> = {
  none: () =>
    '\n\n⚠️ [검색 결과 없음] 직접 일치하는 판정례가 없습니다. 유사한 판단구조를 가진 사례가 있으면 그 구조를 설명하세요. "찾지 못했다"로 끝내지 말고, 이 유형의 사건에서 노동위가 보는 핵심 기준을 짧게 안내하세요.',
  weak: () =>
    '\n\n⚠️ [검색 결과 부족] 유사 판정례가 2건 이하입니다. 확보된 사례를 최대한 활용하되, 추가 사실관계가 있으면 더 정확한 분석이 가능하다고 안내하세요.',
  sufficient: (count) =>
    `\n\n✅ [검색 결과 ${count}건] 충분한 유사 판정례가 확보되었습니다. 구체적 사례를 인용하며 분석하세요.`,
};

function analyzeWinLossFactors(cases: Record<string, unknown>[]): string {
  if (cases.length < 3) return '';

  const granted = cases.filter(c => {
    const r = String(c.decision_result || '');
    return r === 'granted' || r === 'partial' || r === '전부인정' || r === '일부인정';
  });
  const dismissed = cases.filter(c => {
    const r = String(c.decision_result || '');
    return r === 'dismissed' || r === 'rejected' || r === '기각' || r === '각하';
  });

  if (granted.length === 0 && dismissed.length === 0) return '';

  const factorKeywords: Record<string, string[]> = {
    '서면통지': ['서면통지', '서면 통지'],
    '소명기회': ['소명기회', '소명 기회'],
    '인사위원회': ['인사위원회', '징계위원회'],
    '양정 과다': ['양정이 과하', '양정 과다', '과도하'],
    '절차 위반': ['절차 위반', '절차 하자', '절차상 하자'],
    '취업규칙': ['취업규칙', '인사규정'],
  };

  const grantedFactors: string[] = [];
  const dismissedFactors: string[] = [];

  for (const [label, keywords] of Object.entries(factorKeywords)) {
    const gCount = granted.filter(c =>
      keywords.some(kw => String(c.holding_points || '').includes(kw))
    ).length;
    const dCount = dismissed.filter(c =>
      keywords.some(kw => String(c.holding_points || '').includes(kw))
    ).length;

    if (gCount > 0) grantedFactors.push(`${label}(${gCount}건)`);
    if (dCount > 0) dismissedFactors.push(`${label}(${dCount}건)`);
  }

  let analysis = `\n\n승패 요인 분석 (인용 ${granted.length}건 / 기각 ${dismissed.length}건):`;
  if (grantedFactors.length > 0) {
    analysis += `\n인용 사건 주요 요인: ${grantedFactors.join(', ')}`;
  }
  if (dismissedFactors.length > 0) {
    analysis += `\n기각 사건 주요 요인: ${dismissedFactors.join(', ')}`;
  }

  return analysis;
}

function buildIssueSummary(userInput: string, tags: string[]): string[] {
  const summary: string[] = [];
  if (userInput.trim()) summary.push(userInput.trim());
  if (tags.length > 0) summary.push(`핵심 태그: ${tags.join(', ')}`);
  return summary.slice(0, 2);
}

function countKeywordHits(cases: Record<string, unknown>[], keywords: string[]): number {
  return cases.filter((c) => keywords.some((kw) => String(c.holding_points || '').includes(kw))).length;
}

function buildChecklist(cases: Record<string, unknown>[]): string[] {
  const checklistMap: Array<{ label: string; keywords: string[]; helper: string }> = [
    { label: '서면통지', keywords: ['서면통지', '서면 통지'], helper: '서면 통지 여부와 통지 시점을 바로 확인할 것' },
    { label: '소명기회', keywords: ['소명기회', '소명 기회', '변명의 기회', '의견 진술'], helper: '의견 제출과 진술 기회를 실제로 부여했는지 확인할 것' },
    { label: '인사위원회', keywords: ['인사위원회', '징계위원회', '심의위원회'], helper: '징계위원회 개최 여부와 구성·의결 절차를 확인할 것' },
    { label: '징계양정', keywords: ['양정', '과도하', '과중', '비례'], helper: '비위 정도 대비 처분 수위가 과하지 않은지 점검할 것' },
    { label: '개선기회', keywords: ['개선기회', '경고', '시정요구', '개선 의사', 'PIP'], helper: '경고·시정 요구·개선 기간을 줬는지 확인할 것' },
  ];

  const selected = checklistMap
    .map((item) => ({ ...item, hits: countKeywordHits(cases, item.keywords) }))
    .sort((a, b) => b.hits - a.hits)
    .filter((item) => item.hits > 0)
    .slice(0, 5)
    .map((item) => item.helper);

  if (selected.length > 0) return selected;

  return checklistMap.slice(0, 5).map((item) => item.helper);
}

function buildDecisionGuide(cases: Record<string, unknown>[]): string[] {
  const guides: string[] = [];

  if (countKeywordHits(cases, ['서면통지', '서면 통지']) > 0) {
    guides.push('서면 통지 시점과 징계 사유 특정이 명확하면 유지 논리를 세우기 쉽습니다.');
  }
  if (countKeywordHits(cases, ['소명기회', '소명 기회', '변명의 기회', '의견 진술']) > 0) {
    guides.push('소명기회를 실제로 부여한 기록이 없으면 절차 하자로 뒤집힐 위험이 큽니다.');
  }
  if (countKeywordHits(cases, ['인사위원회', '징계위원회', '심의위원회']) > 0) {
    guides.push('위원회 개최, 구성, 의결 정족수 기록이 있으면 사용자 쪽 방어가 쉬워집니다.');
  }
  if (countKeywordHits(cases, ['양정', '과도하', '과중', '비례']) > 0) {
    guides.push('비위 정도 대비 처분 수위를 낮추거나 단계화하면 과중 징계 리스크를 줄일 수 있습니다.');
  }
  if (countKeywordHits(cases, ['개선기회', '경고', '시정요구', 'PIP']) > 0) {
    guides.push('저성과·태도 문제는 경고와 개선기간이 빠지면 사용자에게 불리해지기 쉽습니다.');
  }

  if (guides.length > 0) return guides.slice(0, 3);

  return [
    '사실관계와 절차 기록이 함께 남아 있어야 유지 논리를 세우기 쉽습니다.',
    '징계 사유 특정, 소명기회, 통지 절차 중 하나라도 약하면 뒤집힐 위험이 커집니다.',
    '처분 수위가 과해 보이면 감경 또는 단계적 조치를 먼저 검토하는 편이 안전합니다.',
  ];
}

export function buildComparisonMeta(
  userInput: string,
  tags: string[],
  cases: Record<string, unknown>[],
): ComparisonMeta {
  const normalizedCases: ComparisonCase[] = cases.slice(0, 10).map((c) => ({
    id: String(c.id || ''),
    title: String(c.title || ''),
    decision_result: String(c.decision_result || ''),
    holding_points: String(c.holding_points || '').slice(0, 220),
    url: String(c.url || ''),
    summary_short: String(c.summary_short || '').slice(0, 160),
    key_issue: String(c.key_issue || ''),
    bucket: bucketDecisionResult(String(c.decision_result || '')),
  }));

  const workerWinCases = normalizedCases.filter((c) => c.bucket === 'worker_win').slice(0, 2);
  const employerWinCases = normalizedCases.filter((c) => c.bucket === 'employer_win').slice(0, 2);

  const coreDifferences: string[] = [];
  if (countKeywordHits(cases, ['서면통지', '서면 통지']) > 0) coreDifferences.push('서면통지 유무가 결과를 갈랐는지 확인해야 합니다.');
  if (countKeywordHits(cases, ['소명기회', '소명 기회', '변명의 기회']) > 0) coreDifferences.push('소명기회 부여 여부가 절차 적법성 판단에 직접 연결됩니다.');
  if (countKeywordHits(cases, ['인사위원회', '징계위원회']) > 0) coreDifferences.push('인사위원회 개최와 의결 과정의 적법성이 유지 여부에 영향을 줍니다.');
  if (countKeywordHits(cases, ['양정', '과도하', '과중', '비례']) > 0) coreDifferences.push('비위 정도에 비해 처분 수위가 과하면 뒤집힐 위험이 커집니다.');
  if (countKeywordHits(cases, ['개선기회', '경고', '시정요구', 'PIP']) > 0) coreDifferences.push('개선기회를 줬는지가 저성과·통상해고 영역에서 중요합니다.');

  return {
    issueSummary: buildIssueSummary(userInput, tags),
    workerWinCases,
    employerWinCases,
    coreDifferences: coreDifferences.slice(0, 4),
    checklist: buildChecklist(cases),
    decisionGuide: buildDecisionGuide(cases),
  };
}

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
  const winLossAnalysis = analyzeWinLossFactors(cases);
  const comparison = buildComparisonMeta(userInput, tags, cases);
  const workerWins = comparison.workerWinCases
    .map((c) => `- ${c.title} [${c.decision_result}]: ${c.holding_points}`)
    .join('\n');
  const employerWins = comparison.employerWinCases
    .map((c) => `- ${c.title} [${c.decision_result}]: ${c.holding_points}`)
    .join('\n');
  const checklist = comparison.checklist.map((item) => `- ${item}`).join('\n');
  const differences = comparison.coreDifferences.map((item) => `- ${item}`).join('\n');

  return `사용자 상황: ${userInput}\n\n추출 키워드: ${tags.join(', ')}\n\n유사 판정례 ${cases.length}건:\n${caseSummary}\n\n근로자가 이긴 대표 사건:\n${workerWins || '- 직접 비교 가능한 인용 사건이 충분하지 않습니다.'}\n\n사용자가 이긴 대표 사건:\n${employerWins || '- 직접 비교 가능한 기각 사건이 충분하지 않습니다.'}\n\n승패를 가른 핵심 차이 후보:\n${differences || '- 절차, 양정, 개선기회 여부를 우선 확인하세요.'}\n\n실무 체크리스트 후보:\n${checklist}${winLossAnalysis}${instruction}`;
}

export function trimHistory(
  messages: { role: string; content: string }[],
  userContext: string,
): { role: string; content: string }[] {
  const trimmed = messages
    .slice(-MAX_HISTORY_MESSAGES)
    .map((m) => ({ role: m.role, content: m.content }));

  const lastUserIndex = [...trimmed].reverse().findIndex((message) => message.role === 'user');
  if (lastUserIndex !== -1) {
    const normalizedIndex = trimmed.length - 1 - lastUserIndex;
    trimmed[normalizedIndex] = { role: 'user', content: userContext };
  } else {
    trimmed.push({ role: 'user', content: userContext });
  }

  return trimmed;
}
