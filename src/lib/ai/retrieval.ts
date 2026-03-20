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

// 키워드 → reason_category 매핑 (분류 완료된 42k건 활용)
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

function extractReasonCategories(text: string): string[] {
  const reasons = new Set<string>();
  for (const [pattern, reason] of KEYWORD_TO_REASON) {
    if (pattern.test(text)) reasons.add(reason);
  }
  return [...reasons];
}

const CANDIDATE_LIMIT = 20;
const RESULT_LIMIT = 5;

export async function searchCases(tags: string[], query?: string): Promise<RetrievalResult> {
  let candidates: Record<string, unknown>[] = [];

  // Stage 1A: reason_category 기반 검색 (우선)
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

  // Stage 1B: reason_category로 부족하면 태그 기반 fallback
  if (candidates.length < 3) {
    const topTags = tags.slice(0, 3);
    const { data: tagCases } = await supabase
      .from('nlrc_decisions')
      .select('id, title, decision_result, holding_points, tags, url')
      .overlaps('tags', tags)
      .not('holding_points', 'is', null)
      .limit(CANDIDATE_LIMIT);
    candidates = tagCases || [];
  }

  // Stage 2: hybrid-lite rerank — 현재 비활성화 (Vercel 서버리스 타임아웃 이슈)
  // 임베딩 조회 + OpenAI 쿼리 임베딩이 Vercel 10초 제한을 초과할 수 있어 일시 비활성화
  // TODO: Vercel Pro 전환 또는 Edge Runtime 전환 시 재활성화
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
      similarity: c._similarity as number | undefined,
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
