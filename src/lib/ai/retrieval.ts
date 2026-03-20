import { createClient } from '@supabase/supabase-js';
import { ALL_TAGS } from '@/lib/tags';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_URL = 'https://api.openai.com/v1/embeddings';
const EMBEDDING_MODEL = 'text-embedding-3-small';

// 42k 판정례 분류에서 검증된 키워드 패턴
const KEYWORD_PATTERNS: [RegExp, string][] = [
  // 비위행위 (구체적→일반 순)
  [/횡령|배임|공금|유용|착복|사금고/, '징계해고'],
  [/횡령|배임|공금|유용|착복/, '해고사유'],
  [/폭언|폭행|욕설|폭력|가혹행위|모욕/, '직장내괴롭힘'],
  [/폭언|폭행|욕설|폭력|가혹/, '징계양정'],
  [/성희롱|성추행|성적.*언동|성폭력/, '성희롱'],
  [/무단결근|결근|지각|조퇴|태만|근무태만|직무유기/, '해고사유'],
  [/무단결근|결근|지각|태만/, '징계양정'],
  [/업무능력|성과.*부족|업무.*부적격|근무.*불량|업무.*미숙/, '해고사유'],
  [/기밀|유출|정보.*유출|영업비밀|보안/, '징계해고'],
  [/음주|음주운전|만취/, '징계해고'],
  [/허위|위조|변조|사문서/, '해고사유'],
  [/반말|고객.*민원|불친절|고객.*불만/, '징계양정'],
  [/개인.*용도|사적.*사용|사적.*이용|회사.*차량/, '해고사유'],
  [/겸직|이중.*취업|부업/, '해고사유'],
  [/지시.*불이행|명령.*불복|업무.*거부|업무.*지시/, '해고사유'],
  [/금품.*수수|뇌물|리베이트/, '징계해고'],

  // 사건유형
  [/해고|면직|파면|퇴직.*처리/, '부당해고'],
  [/징계|견책|경고|감봉|정직/, '부당징계'],
  [/전보|전직|배치.*전환|발령/, '전보'],
  [/정직/, '정직'],
  [/감봉/, '감봉'],
  [/수습|시용|수습.*해고/, '수습'],
  [/사직|퇴직|퇴사|합의.*퇴직|권고.*사직/, '사직'],

  // 쟁점
  [/절차.*위반|서면.*통지|해고.*통지|통보.*없이/, '절차위반'],
  [/소명.*기회|의견.*진술|변명.*기회|인사위원회/, '소명기회'],
  [/양정|징계.*수위|과중|비례/, '징계양정'],
  [/갱신.*기대|계약.*갱신|기간제/, '갱신기대권'],
  [/근로자.*지위|근로자.*여부|근로자성/, '근로자성'],

  // 산업
  [/공공기관|공단|공사|재단|진흥원|공기업|지방자치/, '공공기관'],
  [/병원|의료기관|간호|보건|의료법인/, '의료'],
  [/제조|공장|생산.*라인|생산직/, '제조업'],
  [/금융|은행|보험|증권|캐피탈/, '금융'],
  [/학교|대학|교육|학원|교사|교수/, '교육'],
  [/건설|시공|건축|토목/, '건설업'],
  [/운수|버스|택시|화물|운송/, '운수업'],
  [/호텔|음식|유통|마트|서비스/, '서비스업'],
  [/IT|소프트웨어|정보통신|시스템/, 'IT'],
];

export interface CaseCard {
  id: string;
  title: string;
  decision_result: string;
  holding_points: string;
  url: string;
  similarity?: number;
}

export interface RetrievalResult {
  tags: string[];
  cases: CaseCard[];
  allCases: Record<string, unknown>[];
  reranked: boolean;
}

interface CandidateQueryProfile {
  scenario: 'generic' | 'absence_procedure' | 'regular_work_ability' | 'retaliation' | 'severity_excessive';
  primaryPool: string[];
  primaryBoosts: Record<string, number>;
  preferredStages: string[];
  penalizedStages: string[];
  preferredSecondary: string[];
  preferredDispositions: string[];
  preferredFactMarkers: string[];
  preferredLegalFocus: string[];
  boostedDecisionResults: string[];
  excludedDecisionResults: string[];
  penalizedKeywords: string[];
}

export function extractTags(text: string): string[] {
  const tags = new Set<string>();
  for (const [pattern, tag] of KEYWORD_PATTERNS) {
    if (pattern.test(text)) {
      tags.add(tag);
    }
  }
  if (tags.size < 2) {
    tags.add('부당해고');
    tags.add('징계양정');
  }
  return [...tags].filter((t) => (ALL_TAGS as readonly string[]).includes(t));
}

// 키워드 → 신규 8축 태그 매핑
const KEYWORD_TO_PRIMARY: [RegExp, string][] = [
  [/횡령|배임|공금|유용|착복/, 'misconduct'],
  [/폭언|폭행|욕설|폭력|가혹|모욕/, 'disciplinary_severity'],
  [/성희롱|성추행|성적.*언동/, 'misconduct'],
  [/무단결근|결근|지각|조퇴|태만|근무태만|직무유기/, 'absence_without_leave'],
  [/업무능력|성과.*부족|업무.*부적격|근무.*불량/, 'work_ability'],
  [/직장.*내.*괴롭힘|따돌림/, 'workplace_harassment'],
  [/경영.*해고|정리해고|구조조정|경영.*악화/, 'redundancy'],
  [/수습|시용/, 'dismissal_validity'],
  [/전보|전직|배치.*전환|인사.*발령/, 'transfer_validity'],
  [/갱신.*기대|계약.*만료|기간제/, 'renewal_expectation'],
  [/사직|권고.*사직|합의.*퇴직/, 'dismissal_validity'],
  [/부당노동행위|노조|지배.*개입/, 'unfair_treatment'],
  [/근로자.*지위|근로자성/, 'worker_status'],
  [/차별.*시정|차별적.*처우/, 'discrimination'],
  [/겸직|허위|위조|음주|기밀|유출|지시.*불이행|금품/, 'misconduct'],
  [/징계.*양정|양정.*과다|처분.*과중|비례/, 'disciplinary_severity'],
  [/절차.*위반|서면.*통지|소명.*기회/, 'procedure'],
  [/괴롭힘.*신고.*불이익|보복/, 'retaliation'],
];

const KEYWORD_TO_STAGE: [RegExp, string][] = [
  [/정규직|상용직|기간의\s*정함이\s*없는/, 'regular'],
  [/수습|시용|본채용/, 'probation'],
  [/기간제|계약직|계약기간\s*만료|갱신/, 'fixed_term'],
  [/채용내정|채용\s*전|입사\s*전/, 'pre_hire'],
];

// 키워드 → reason_category (fallback용)
const KEYWORD_TO_REASON: [RegExp, string][] = [
  [/횡령|배임|공금|유용|착복/, 'embezzlement'],
  [/폭언|폭행|욕설|폭력|가혹|모욕/, 'violence'],
  [/성희롱|성추행|성적.*언동/, 'sexual_harassment'],
  [/무단결근|결근|지각|조퇴|태만|근무태만|직무유기/, 'absence'],
  [/업무능력|성과.*부족|업무.*부적격|근무.*불량/, 'incompetence'],
  [/직장.*내.*괴롭힘|따돌림/, 'workplace_bullying'],
  [/경영.*해고|정리해고|구조조정|경영.*악화/, 'redundancy'],
  [/수습|시용/, 'probation'],
  [/전보|전직|배치.*전환|인사.*발령/, 'transfer'],
  [/갱신.*기대|계약.*만료|기간제/, 'contract_expiry'],
  [/사직|권고.*사직|합의.*퇴직/, 'no_dismissal'],
  [/부당노동행위|노조|지배.*개입/, 'union_activity'],
  [/근로자.*지위|근로자성/, 'worker_status'],
  [/차별.*시정|차별적.*처우/, 'discrimination'],
  [/겸직|허위|위조|음주|기밀|유출|지시.*불이행|금품/, 'misconduct'],
];

function extractPrimaryTypes(text: string): string[] {
  const types = new Set<string>();
  for (const [pattern, primary] of KEYWORD_TO_PRIMARY) {
    if (pattern.test(text)) types.add(primary);
  }
  return [...types];
}

function extractReasonCategories(text: string): string[] {
  const reasons = new Set<string>();
  for (const [pattern, reason] of KEYWORD_TO_REASON) {
    if (pattern.test(text)) reasons.add(reason);
  }
  return [...reasons];
}

function extractEmploymentStages(text: string): string[] {
  const stages = new Set<string>();
  for (const [pattern, stage] of KEYWORD_TO_STAGE) {
    if (pattern.test(text)) stages.add(stage);
  }
  return [...stages];
}

const DB_CANDIDATE_LIMIT = 60;
const CANDIDATE_LIMIT = 20;
const RESULT_LIMIT = 5;

function uniq(values: string[]): string[] {
  return [...new Set(values.filter(Boolean))];
}

function includesAny(text: string, needles: string[]): boolean {
  return needles.some((needle) => text.includes(needle));
}

function asStringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((v): v is string => typeof v === 'string') : [];
}

function buildCandidateQueryProfile(query: string): CandidateQueryProfile {
  const lowered = query.toLowerCase();
  const primaryPool = extractPrimaryTypes(query);
  const stageHints = extractEmploymentStages(query);
  const base: CandidateQueryProfile = {
    scenario: 'generic',
    primaryPool: uniq(primaryPool),
    primaryBoosts: Object.fromEntries(primaryPool.map((primary) => [primary, 10])),
    preferredStages: stageHints,
    penalizedStages: [],
    preferredSecondary: [],
    preferredDispositions: [],
    preferredFactMarkers: [],
    preferredLegalFocus: [],
    boostedDecisionResults: [],
    excludedDecisionResults: [],
    penalizedKeywords: [],
  };

  const hasAbsence = includesAny(lowered, ['무단결근', '결근', '근무태만', '근무지 이탈']);
  const hasProcedure = includesAny(lowered, ['절차', '서면통지', '서면 통지', '소명', '인사위원회']);
  const hasRegular = includesAny(lowered, ['정규직']);
  const hasWorkAbility = includesAny(lowered, ['업무능력', '저성과', '성과 부족', '성과부족']);
  const hasRetaliation = includesAny(lowered, ['보복', '불이익', '신고 이후', '신고자']);
  const hasHarassment = includesAny(lowered, ['직장내괴롭힘', '괴롭힘']);
  const hasSeverity = includesAny(lowered, ['양정', '과하다', '과도', '너무 과', '수위']);
  const hasDismissal = includesAny(lowered, ['해고']);

  if (hasAbsence && hasProcedure) {
    return {
      ...base,
      scenario: 'absence_procedure',
      primaryPool: uniq(['procedure', 'dismissal_validity', 'absence_without_leave']),
      primaryBoosts: {
        procedure: 16,
        dismissal_validity: 10,
        absence_without_leave: 4,
      },
      preferredSecondary: ['procedure', 'absence_without_leave'],
      preferredFactMarkers: ['unauthorized_absence', 'written_notice_missing'],
      preferredLegalFocus: ['procedural_due_process'],
      excludedDecisionResults: ['dismissed', 'settled'],
      penalizedKeywords: ['구제이익', '복직명령', '상시근로자 수', '채용내정'],
    };
  }

  if (hasRegular && hasWorkAbility) {
    return {
      ...base,
      scenario: 'regular_work_ability',
      primaryPool: uniq(['work_ability', 'dismissal_validity']),
      primaryBoosts: {
        work_ability: 15,
        dismissal_validity: 7,
      },
      preferredStages: stageHints.includes('regular') ? ['regular'] : ['regular'],
      penalizedStages: stageHints.includes('regular') ? ['probation'] : [],
      preferredFactMarkers: ['qualitative_evaluation', 'quantitative_evaluation', 'warning_given', 'improvement_opportunity_given', 'training_provided'],
      preferredLegalFocus: ['just_cause', 'social_norm_reasonableness'],
      penalizedKeywords: ['수습', '본채용', '시용'],
    };
  }

  if (hasHarassment && hasRetaliation) {
    return {
      ...base,
      scenario: 'retaliation',
      primaryPool: uniq(['retaliation', 'unfair_treatment', 'workplace_harassment']),
      primaryBoosts: {
        retaliation: 16,
        unfair_treatment: 13,
        workplace_harassment: 3,
      },
      preferredDispositions: ['dismissal', 'disciplinary_dismissal', 'transfer', 'suspension', 'pay_cut', 'reprimand'],
      preferredFactMarkers: ['harassment_report_filed'],
      preferredLegalFocus: ['protection_against_retaliation'],
      preferredSecondary: ['workplace_harassment', 'unfair_treatment'],
      preferredStages: stageHints,
      penalizedStages: stageHints.includes('regular') ? ['probation'] : [],
      penalizedKeywords: ['2차 가해', '성희롱'],
    };
  }

  if (hasSeverity && hasDismissal) {
    return {
      ...base,
      scenario: 'severity_excessive',
      primaryPool: uniq(['disciplinary_severity', 'misconduct']),
      primaryBoosts: {
        disciplinary_severity: 16,
        misconduct: 5,
      },
      preferredDispositions: ['dismissal', 'disciplinary_dismissal', 'suspension', 'pay_cut'],
      preferredLegalFocus: ['proportionality', 'appropriateness_of_discipline'],
      preferredSecondary: ['misconduct'],
      boostedDecisionResults: ['granted', 'partial', 'overturned'],
      excludedDecisionResults: ['dismissed', 'settled'],
      penalizedKeywords: ['구제이익', '채용내정', '상시근로자 수', '복직명령', '계약기간 만료'],
    };
  }

  return base;
}

function scoreTaggedCandidate(candidate: Record<string, unknown>, query: string, profile: CandidateQueryProfile): { score: number; reasons: string[] } {
  const reasons: string[] = [];
  let score = 0;

  const primary = (candidate.issue_type_primary as string) || '';
  const secondary = asStringArray(candidate.issue_type_secondary);
  const dispositions = asStringArray(candidate.disposition_type);
  const factMarkers = asStringArray(candidate.fact_markers);
  const legalFocus = asStringArray(candidate.legal_focus);
  const exclusions = asStringArray(candidate.exclusion_flags);
  const stage = (candidate.employment_stage as string) || '';
  const decisionResult = (candidate.decision_result as string) || '';
  const haystack = [
    candidate.title,
    candidate.summary_short,
    candidate.holding_points,
    candidate.retrieval_note,
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();

  const primaryBoost = profile.primaryBoosts[primary];
  if (primaryBoost) {
    score += primaryBoost;
    reasons.push(`primary:${primary}`);
  }

  const secondaryHits = profile.preferredSecondary.filter((item) => secondary.includes(item));
  if (secondaryHits.length > 0) {
    score += secondaryHits.length * 4;
    reasons.push(`secondary:${secondaryHits.join(',')}`);
  }

  const dispositionHits = profile.preferredDispositions.filter((item) => dispositions.includes(item));
  if (dispositionHits.length > 0) {
    score += dispositionHits.length * 4;
    reasons.push(`disposition:${dispositionHits.join(',')}`);
  }

  const factHits = profile.preferredFactMarkers.filter((item) => factMarkers.includes(item));
  if (factHits.length > 0) {
    score += factHits.length * 5;
    reasons.push(`fact:${factHits.join(',')}`);
  }

  const focusHits = profile.preferredLegalFocus.filter((item) => legalFocus.includes(item));
  if (focusHits.length > 0) {
    score += focusHits.length * 6;
    reasons.push(`focus:${focusHits.join(',')}`);
  }

  if (profile.preferredStages.includes(stage)) {
    score += 7;
    reasons.push(`stage:${stage}`);
  }

  if (profile.penalizedStages.includes(stage)) {
    score -= 9;
    reasons.push(`stage_penalty:${stage}`);
  }

  if (profile.boostedDecisionResults.includes(decisionResult)) {
    score += 4;
    reasons.push(`result_boost:${decisionResult}`);
  }

  if (query.includes('결근') && exclusions.includes('not_really_absence_case')) {
    score -= 10;
    reasons.push('exclude:not_really_absence_case');
  }
  if (query.includes('괴롭힘') && exclusions.includes('not_really_harassment_case')) {
    score -= 10;
    reasons.push('exclude:not_really_harassment_case');
  }

  for (const keyword of profile.penalizedKeywords) {
    if (haystack.includes(keyword.toLowerCase())) {
      score -= 6;
      reasons.push(`keyword_penalty:${keyword}`);
    }
  }

  const queryTokens = query.split(/\s+/).filter((token) => token.length >= 2);
  const textHits = queryTokens.filter((token) => haystack.includes(token.toLowerCase())).length;
  if (textHits > 0) {
    score += Math.min(textHits, 4);
    reasons.push(`text:${textHits}`);
  }

  if (profile.scenario === 'absence_procedure') {
    const hasProcedureEvidence = primary === 'procedure' || secondary.includes('procedure') || legalFocus.includes('procedural_due_process');
    const hasAbsenceEvidence = primary === 'absence_without_leave' || secondary.includes('absence_without_leave') || factMarkers.includes('unauthorized_absence');
    if (hasProcedureEvidence && hasAbsenceEvidence) {
      score += 7;
      reasons.push('cross:absence+procedure');
    } else if (primary === 'absence_without_leave') {
      score -= 6;
      reasons.push('cross_penalty:absence_only');
    }
  }

  if (profile.scenario === 'regular_work_ability') {
    if (primary === 'work_ability' && stage === 'regular') {
      score += 7;
      reasons.push('cross:regular_work_ability');
    }
    if (stage === 'probation') {
      score -= 6;
      reasons.push('cross_penalty:probation_mix');
    }
  }

  if (profile.scenario === 'retaliation') {
    const hasRetaliationStructure =
      primary === 'retaliation' ||
      primary === 'unfair_treatment' ||
      legalFocus.includes('protection_against_retaliation') ||
      factMarkers.includes('harassment_report_filed');
    if (hasRetaliationStructure) {
      score += 7;
      reasons.push('cross:retaliation_structure');
    }
    if (primary === 'workplace_harassment' && !hasRetaliationStructure) {
      score -= 7;
      reasons.push('cross_penalty:harassment_only');
    }
  }

  if (profile.scenario === 'severity_excessive') {
    const hasSeverityStructure =
      primary === 'disciplinary_severity' &&
      (legalFocus.includes('proportionality') || legalFocus.includes('appropriateness_of_discipline'));
    if (hasSeverityStructure) {
      score += 8;
      reasons.push('cross:severity_proportionality');
    }
    if (decisionResult === 'dismissed' || decisionResult === 'rejected') {
      score -= 4;
      reasons.push('cross_penalty:non_excessive_outcome');
    }
  }

  return { score, reasons };
}

function rankTaggedCandidates(query: string, taggedCases: Record<string, unknown>[]): Record<string, unknown>[] {
  const profile = buildCandidateQueryProfile(query);

  const filtered = taggedCases.filter((candidate) => {
    const exclusions = asStringArray(candidate.exclusion_flags);
    const decisionResult = (candidate.decision_result as string) || '';
    if (query.includes('결근') && exclusions.includes('not_really_absence_case')) return false;
    if (query.includes('괴롭힘') && exclusions.includes('not_really_harassment_case') && profile.scenario !== 'retaliation') return false;
    if (query.includes('수습') && exclusions.includes('unrelated_to_probation')) return false;
    if (profile.excludedDecisionResults.includes(decisionResult)) return false;
    return true;
  });

  const scored = filtered.map((candidate) => {
    const { score, reasons } = scoreTaggedCandidate(candidate, query, profile);
    return { ...candidate, _score: score, _score_reasons: reasons };
  });

  scored.sort((a, b) => {
    const scoreDiff = ((b as Record<string, unknown>)._score as number || 0) - ((a as Record<string, unknown>)._score as number || 0);
    if (scoreDiff !== 0) return scoreDiff;
    const aDecision = ((a as Record<string, unknown>).decision_result as string) || '';
    const bDecision = ((b as Record<string, unknown>).decision_result as string) || '';
    if (aDecision !== bDecision) return aDecision.localeCompare(bDecision);
    return (((a as Record<string, unknown>).id as string) || '').localeCompare(((b as Record<string, unknown>).id as string) || '');
  });

  return scored;
}

export async function searchCases(tags: string[], query?: string): Promise<RetrievalResult> {
  let candidates: Record<string, unknown>[] = [];

  // Stage 1A: 신규 8축 태그 기반 검색 (우선 — 3,839건 태깅 완료)
  const profile = query ? buildCandidateQueryProfile(query) : null;
  const primaryTypes = profile?.primaryPool || [];
  if (primaryTypes.length > 0) {
    const { data: taggedCases } = await supabase
      .from('nlrc_decisions')
      .select('id, title, decision_result, holding_points, summary_short, retrieval_note, tags, url, employment_stage, issue_type_primary, issue_type_secondary, disposition_type, fact_markers, legal_focus, industry_context, exclusion_flags')
      .in('issue_type_primary', primaryTypes)
      .not('holding_points', 'is', null)
      .limit(DB_CANDIDATE_LIMIT);

    if (taggedCases && taggedCases.length > 0) {
      candidates = query ? rankTaggedCandidates(query, taggedCases) : taggedCases;
    }
  }

  // Stage 1B: 신규 태그 부족하면 기존 reason_category fallback
  if (candidates.length < 3) {
    const reasons = query ? extractReasonCategories(query) : [];
    if (reasons.length > 0) {
      const { data: reasonCases } = await supabase
        .from('nlrc_decisions')
        .select('id, title, decision_result, holding_points, tags, url')
        .overlaps('reason_category', reasons)
        .not('holding_points', 'is', null)
        .limit(CANDIDATE_LIMIT);
      candidates = reasonCases || [];
    }
  }

  // Stage 1C: 둘 다 부족하면 태그 기반 fallback
  if (candidates.length < 3) {
    const { data: tagCases } = await supabase
      .from('nlrc_decisions')
      .select('id, title, decision_result, holding_points, tags, url')
      .overlaps('tags', tags)
      .not('holding_points', 'is', null)
      .limit(CANDIDATE_LIMIT);
    candidates = tagCases || [];
  }

  const reranked = false;

  const results = candidates.slice(0, RESULT_LIMIT);

  return {
    tags,
    cases: results.map((c) => ({
      id: c.id as string,
      title: c.title as string,
      decision_result: c.decision_result as string,
      holding_points: ((c.holding_points as string) || '').slice(0, 150),
      url: c.url as string,
      similarity: (c._score as number | undefined) ?? (c._similarity as number | undefined),
    })),
    allCases: candidates,
    reranked,
  };
}

// --- hybrid-lite rerank ---

async function getQueryEmbedding(text: string): Promise<number[]> {
  const resp = await fetch(OPENAI_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${OPENAI_API_KEY}`,
    },
    body: JSON.stringify({ model: EMBEDDING_MODEL, input: text }),
  });

  if (!resp.ok) throw new Error(`Embedding API ${resp.status}`);
  const data = await resp.json();
  return data.data[0].embedding;
}

function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function rerankByEmbedding(
  query: string,
  candidates: Record<string, unknown>[],
): Promise<Record<string, unknown>[]> {
  // 쿼리 임베딩 생성 (~100ms)
  const queryEmbedding = await getQueryEmbedding(query);

  // 후보 ID로 임베딩만 별도 조회 (메타데이터 select에서 제외했으므로)
  const ids = candidates.map((c) => c.id as string);
  const { data: embeddingRows } = await supabase
    .from('nlrc_decisions')
    .select('id, embedding')
    .in('id', ids);

  const embeddingMap = new Map<string, number[]>();
  for (const row of embeddingRows || []) {
    if (row.embedding) embeddingMap.set(row.id, row.embedding);
  }

  // 유사도 계산
  const scored = candidates.map((c) => {
    const embedding = embeddingMap.get(c.id as string);
    const similarity = embedding ? cosineSimilarity(queryEmbedding, embedding) : -1;
    return { ...c, _similarity: similarity };
  });

  // 유사도 내림차순 정렬
  scored.sort((a, b) => (b._similarity as number) - (a._similarity as number));

  return scored;
}
