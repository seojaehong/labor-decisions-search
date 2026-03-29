import { createClient } from '@supabase/supabase-js';
import { extractTags, searchCases } from '@/lib/ai/retrieval';
import { normalizeQuery } from '@/lib/search/normalize-query';
import { parseCandidateQuery } from '@/lib/search/query-parser';
import type {
  SearchBucket,
  SearchCard,
  SearchDebugBucket,
  SearchDebugCandidateBucket,
  SearchRequestOptions,
  SearchResponsePayload,
} from '@/lib/search/types';
import type { ReasonCategory } from '@/lib/types';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type CandidateMetaRow = Record<string, unknown>;
const IS_DEV = process.env.NODE_ENV === 'development';

const COMPARE_BUCKET_SIZE = 5;
const BASELINE_PAGE_SIZE = 20;
const CANDIDATE_PAGE_SIZE = 5;
const COMBINED_QUERY_FETCH_SIZE = 80;

const REASON_TO_QUERY: Record<string, string> = {
  sexual_harassment: '성희롱',
  workplace_bullying: '직장내괴롭힘',
  violence: '폭행 폭언',
  absence: '무단결근',
  embezzlement: '횡령 배임',
  incompetence: '업무능력 부족',
  misconduct: '비위행위',
  redundancy: '경영상 해고',
  probation: '수습 본채용',
  transfer: '전보 인사발령',
  contract_expiry: '갱신기대권 계약만료',
  no_dismissal: '해고부존재 사직',
  union_activity: '부당노동행위',
  worker_status: '근로자성',
  discrimination: '차별시정',
};

const REASON_TO_LAWGO_KEYWORDS: Record<string, string[]> = {
  absence: ['부당해고', '취업규칙', '해고부존재'],
  workplace_bullying: ['직장내괴롭힘', '성희롱', '폭언/폭행'],
  sexual_harassment: ['성희롱', '직장내괴롭힘'],
  violence: ['폭언/폭행', '비위행위'],
  embezzlement: ['횡령/배임', '비위행위'],
  incompetence: ['부당해고', '전보/인사이동'],
  misconduct: ['비위행위', '부당해고', '취업규칙'],
  redundancy: ['경영상해고', '부당해고'],
  probation: ['수습', '본채용거부', '부당해고'],
  transfer: ['전보/인사이동', '취업규칙'],
  contract_expiry: ['갱신기대권', '기간제', '부당해고'],
  no_dismissal: ['해고부존재', '부당해고'],
  union_activity: ['노동조합', '부당노동행위', '단체교섭', '단체협약', '조합활동', '쟁의행위'],
  worker_status: ['근로자성', '파견', '도급'],
  discrimination: ['남녀고용평등', '근로조건'],
};

function matchesReason(reasonCategory: string[] | null | undefined, reason: ReasonCategory | ''): boolean {
  if (!reason) return true;
  return (reasonCategory || []).includes(reason);
}

function escapeIlike(value: string): string {
  return value.replace(/[%_,]/g, ' ').trim();
}

function tokenizeQuery(query: string): string[] {
  const normalized = normalizeQuery(query);
  const baseTokens = normalized.keywords.length > 0 ? normalized.keywords : query.split(/\s+/);
  return Array.from(new Set(baseTokens.map((token) => token.trim()).filter((token) => token.length > 0)));
}

function normalizeDateValue(value: string | null | undefined): number {
  if (!value) return 0;
  const digits = String(value).replace(/\D/g, '');
  if (!digits) return 0;
  const numeric = Number(digits);
  return Number.isFinite(numeric) ? numeric : 0;
}

function computeFieldScore(field: string | null | undefined, tokens: string[], weight: number): number {
  const haystack = String(field || '').toLowerCase();
  if (!haystack) return 0;
  let score = 0;
  for (const token of tokens) {
    const needle = token.toLowerCase();
    if (!needle) continue;
    if (haystack.includes(needle)) {
      score += weight;
    }
  }
  return score;
}

function computeKeywordArrayScore(keywords: string[] | null | undefined, query: string): number {
  if (!keywords || keywords.length === 0) return 0;
  const tokens = tokenizeQuery(query).map((token) => token.toLowerCase());
  const normalizedKeywords = keywords.map((keyword) => keyword.toLowerCase());
  let score = 0;

  for (const token of tokens) {
    if (normalizedKeywords.some((keyword) => keyword.includes(token) || token.includes(keyword))) {
      score += 4;
    }
  }

  return score;
}

function deriveReasonKeywordHints(query: string): string[] {
  const lowered = query.toLowerCase();
  return Array.from(
    new Set(
      Object.entries(REASON_TO_LAWGO_KEYWORDS)
        .filter(([reason, keywords]) => lowered.includes(reason) || keywords.some((keyword) => lowered.includes(keyword.toLowerCase())))
        .flatMap(([, keywords]) => keywords)
    )
  );
}

function scoreSearchCard(item: SearchCard, tokens: string[], keywordHints: string[]): number {
  const query = tokens.join(' ');
  return (
    computeFieldScore(item.title, tokens, 5) +
    computeFieldScore(item.holding_summary, tokens, 3) +
    computeFieldScore(item.key_issue, tokens, 3) +
    computeFieldScore(item.holding_points, tokens, 2) +
    computeKeywordArrayScore(item.reason_category, query) +
    computeKeywordArrayScore(item.reason_category, keywordHints.join(' '))
  );
}

function mergeAndRankSearchCards(items: SearchCard[], query: string, page: number, pageSize: number): SearchBucket {
  const tokens = tokenizeQuery(query);
  const keywordHints = deriveReasonKeywordHints(query);
  const ranked = items
    .map((item) => ({
      item,
      relevance: scoreSearchCard(item, tokens, keywordHints),
      dateValue: normalizeDateValue(item.decision_date),
    }))
    .sort((a, b) => {
      if (b.relevance !== a.relevance) return b.relevance - a.relevance;
      if (b.dateValue !== a.dateValue) return b.dateValue - a.dateValue;
      return a.item.id.localeCompare(b.item.id);
    });

  const deduped: SearchCard[] = [];
  const seen = new Set<string>();
  const seenDuplicateGroups = new Set<string>();
  for (const entry of ranked) {
    if (seen.has(entry.item.id)) continue;
    if (entry.item.duplicate_group_id && seenDuplicateGroups.has(entry.item.duplicate_group_id)) {
      continue;
    }
    seen.add(entry.item.id);
    if (entry.item.duplicate_group_id) {
      seenDuplicateGroups.add(entry.item.duplicate_group_id);
    }
    deduped.push(entry.item);
  }

  return {
    items: deduped.slice(page * pageSize, (page + 1) * pageSize),
    total: deduped.length,
    page,
    pageSize,
  };
}

function buildBaselineSelect(page: number, pageSize: number) {
  return supabase
    .from('nlrc_decisions')
    .select(
      'id, title, case_number, department, decision_date, decision_result, key_issue, holding_summary, holding_points, url, reason_category',
      { count: 'exact' }
    )
    .range(page * pageSize, (page + 1) * pageSize - 1)
    .order('decision_date', { ascending: false });
}

function buildLawgoSelect(limit: number) {
  return supabase
    .from('lawgo_precedents')
    .select(
      'id, api_id, title, reference_number, decision_date, court, judgment_type, issue_text, summary_text, reference_statutes, reference_cases, source_url, keywords_matched, bigcase_case_id',
      { count: 'exact' }
    )
    .limit(limit)
    .order('decision_date', { ascending: false, nullsFirst: false });
}

function buildBigcaseSelect(limit: number) {
  return supabase
    .from('cases')
    .select(
      'id, title, case_number, court, decision_date, verdict_type, summary, holding_points, keywords_matched, url',
      { count: 'exact' }
    )
    .limit(limit)
    .order('decision_date', { ascending: false, nullsFirst: false });
}

async function runLawgoSearch(query: string, limit = 8): Promise<SearchBucket> {
  let q = buildLawgoSelect(limit);
  if (query) {
    const escaped = escapeIlike(query);
    q = q.or(
      [
        `title.ilike.%${escaped}%`,
        `issue_text.ilike.%${escaped}%`,
        `summary_text.ilike.%${escaped}%`,
        `reference_statutes.ilike.%${escaped}%`,
        `reference_cases.ilike.%${escaped}%`,
        `reference_number.ilike.%${escaped}%`,
      ].join(',')
    );
  }

  const { data, count, error } = await q;
  if (error) throw error;

  const items: SearchCard[] = (data || []).map((row) => ({
    id: row.id,
    title: row.title,
    case_number: row.reference_number || '',
    department: row.court || null,
    decision_date: row.decision_date || null,
      decision_result: row.judgment_type || '판례',
      key_issue: row.issue_text || null,
      holding_summary: row.summary_text || null,
      holding_points: row.summary_text || null,
      url: row.source_url || null,
      reason_category: row.keywords_matched || [],
      source_provider: 'lawgo',
      duplicate_group_id: row.bigcase_case_id || null,
    }));

  return {
    items,
    total: count || 0,
    page: 0,
    pageSize: limit,
  };
}

async function runBigcaseSearch(query: string, limit = 8): Promise<SearchBucket> {
  let q = buildBigcaseSelect(limit);
  if (query) {
    const escaped = escapeIlike(query);
    q = q.or(
      [
        `title.ilike.%${escaped}%`,
        `summary.ilike.%${escaped}%`,
        `holding_points.ilike.%${escaped}%`,
        `case_number.ilike.%${escaped}%`,
      ].join(',')
    );
  }

  const { data, count, error } = await q;
  if (error) throw error;

  const items: SearchCard[] = (data || []).map((row) => ({
    id: row.id,
    title: row.title,
    case_number: row.case_number || '',
    department: row.court || null,
    decision_date: row.decision_date || null,
    decision_result: row.verdict_type || '판결',
    key_issue: row.summary || null,
    holding_summary: row.summary || null,
    holding_points: row.holding_points || null,
    url: row.url || null,
    reason_category: row.keywords_matched || [],
    source_provider: 'bigcase',
    duplicate_group_id: row.id,
  }));

  return {
    items,
    total: count || 0,
    page: 0,
    pageSize: limit,
  };
}

async function runBaselineSearch({
  query,
  reason = '',
  result = '',
  page = 0,
  pageSize = BASELINE_PAGE_SIZE,
}: SearchRequestOptions): Promise<SearchBucket> {
  if (query && !reason && !result) {
    const escaped = escapeIlike(query);
    const normalized = normalizeQuery(query);
    const searchTerms =
      normalized.keywords.length > 0 ? normalized.keywords.slice(0, 4).join(' & ') : query.split(' ').join(' & ');

    let nlrcQuery = supabase
      .from('nlrc_decisions')
      .select(
        'id, title, case_number, department, decision_date, decision_result, key_issue, holding_summary, holding_points, url, reason_category',
        { count: 'exact' }
      )
      .limit(COMBINED_QUERY_FETCH_SIZE)
      .order('decision_date', { ascending: false });

    nlrcQuery = nlrcQuery.textSearch('search_vector', searchTerms);
    let nlrcResp = await nlrcQuery;

    if (nlrcResp.error || (nlrcResp.count || 0) === 0) {
      nlrcResp = await supabase
        .from('nlrc_decisions')
        .select(
          'id, title, case_number, department, decision_date, decision_result, key_issue, holding_summary, holding_points, url, reason_category',
          { count: 'exact' }
        )
        .or(`title.ilike.%${escaped}%,key_issue.ilike.%${escaped}%,holding_points.ilike.%${escaped}%,holding_summary.ilike.%${escaped}%`)
        .limit(COMBINED_QUERY_FETCH_SIZE)
        .order('decision_date', { ascending: false });
    }

    if (nlrcResp.error) throw nlrcResp.error;

    const nlrcItems: SearchCard[] = (nlrcResp.data || []).map((row) => ({
      id: row.id,
      title: row.title,
      case_number: row.case_number || '',
      department: row.department,
      decision_date: row.decision_date,
      decision_result: row.decision_result,
      key_issue: row.key_issue,
      holding_summary: row.holding_summary || null,
      holding_points: row.holding_points || null,
      url: row.url,
      reason_category: row.reason_category || [],
      source_provider: 'nlrc',
    }));

    const bigcaseBucket = await runBigcaseSearch(query, COMBINED_QUERY_FETCH_SIZE);
    const lawgoBucket = await runLawgoSearch(query, COMBINED_QUERY_FETCH_SIZE);
    const merged = mergeAndRankSearchCards([...nlrcItems, ...bigcaseBucket.items, ...lawgoBucket.items], query, page, pageSize);

    return {
      ...merged,
      total: Math.max(merged.total, (nlrcResp.count || 0) + (bigcaseBucket.total || 0) + (lawgoBucket.total || 0)),
    };
  }

  let q = buildBaselineSelect(page, pageSize);
  if (reason) q = q.contains('reason_category', [reason]);
  if (result) q = q.eq('decision_result', result);
  if (query) {
    const normalized = normalizeQuery(query);
    const searchTerms =
      normalized.keywords.length > 0 ? normalized.keywords.slice(0, 4).join(' & ') : query.split(' ').join(' & ');
    q = q.textSearch('search_vector', searchTerms);
  }

  let { data, count, error } = await q;

  if (error || (query && (count || 0) === 0)) {
    let fallback = buildBaselineSelect(page, pageSize);
    if (reason) fallback = fallback.contains('reason_category', [reason]);
    if (result) fallback = fallback.eq('decision_result', result);
    if (query) {
      fallback = fallback.or(`title.ilike.%${query}%,key_issue.ilike.%${query}%,holding_points.ilike.%${query}%`);
    }
    const fallbackResp = await fallback;
    data = fallbackResp.data;
    count = fallbackResp.count;
    error = fallbackResp.error;
  }

  if (error) throw error;

  const items: SearchCard[] = (data || []).map((row) => ({
    id: row.id,
    title: row.title,
    case_number: row.case_number || '',
    department: row.department,
    decision_date: row.decision_date,
    decision_result: row.decision_result,
    key_issue: row.key_issue,
    holding_summary: row.holding_summary || null,
    holding_points: row.holding_points || null,
    url: row.url,
    reason_category: row.reason_category || [],
    source_provider: 'nlrc',
  }));

  return {
    items,
    total: count || 0,
    page,
    pageSize,
  };
}

async function hydrateCandidateRows(rows: CandidateMetaRow[]): Promise<SearchCard[]> {
  const ids = rows.map((row) => String(row.id));
  if (ids.length === 0) return [];

  const { data, error } = await supabase
    .from('nlrc_decisions')
    .select('id, title, case_number, department, decision_date, decision_result, key_issue, holding_summary, holding_points, url, reason_category')
    .in('id', ids);

  if (error) throw error;

  const baseById = new Map((data || []).map((row) => [row.id, row]));

  return rows.map((row) => {
    const base = baseById.get(String(row.id));
    return {
      id: String(row.id),
      title: base?.title || String(row.title || ''),
      case_number: base?.case_number || '',
      department: base?.department || null,
      decision_date: base?.decision_date || null,
      decision_result: base?.decision_result || String(row.decision_result || ''),
      key_issue: base?.key_issue || null,
      holding_summary: base?.holding_summary || null,
      holding_points: base?.holding_points || null,
      url: base?.url || null,
      reason_category: base?.reason_category || [],
    };
  });
}

async function runCandidateRecall(query: string, reason: ReasonCategory | ''): Promise<CandidateMetaRow[]> {
  const effectiveQuery = query.trim() || (reason ? REASON_TO_QUERY[reason] || reason : '');
  const parsed = await parseCandidateQuery(effectiveQuery);
  const tags = extractTags(parsed.normalized_query || effectiveQuery);
  const retrieval = await searchCases(tags, effectiveQuery);
  return retrieval.allCases;
}

function toDebugBucket(items: SearchCard[]): SearchDebugBucket {
  return {
    top_ids: items.slice(0, 5).map((item) => item.id),
  };
}

function toCandidateDebugBucket(
  items: SearchCard[],
  parsed: Awaited<ReturnType<typeof parseCandidateQuery>>,
  rows: CandidateMetaRow[]
): SearchDebugCandidateBucket {
  return {
    ...toDebugBucket(items),
    normalized_query: parsed.normalized_query,
    scenario: parsed.query_scenario,
    intended_primary: parsed.intended_primary,
    intended_stage: parsed.intended_stage,
    intended_disposition: parsed.intended_disposition,
    top_score_reasons: rows
      .slice(0, 3)
      .flatMap((row) => (Array.isArray(row._score_reasons) ? row._score_reasons.slice(0, 2) : []))
      .map((value) => String(value)),
  };
}

function runCandidatePrecision(
  rows: SearchCard[],
  {
    result = '',
    reason = '',
    page = 0,
    pageSize = CANDIDATE_PAGE_SIZE,
  }: Pick<SearchRequestOptions, 'reason' | 'result' | 'page' | 'pageSize'>
): SearchBucket {
  const filtered = rows.filter((item) => {
    if (result && item.decision_result !== result) return false;
    if (!matchesReason(item.reason_category, reason)) return false;
    return true;
  });

  const total = filtered.length;
  const paged = filtered.slice(page * pageSize, (page + 1) * pageSize);

  return {
    items: paged,
    total,
    page,
    pageSize,
  };
}

async function runCandidateSearch({
  query,
  reason = '',
  result = '',
  page = 0,
  pageSize = CANDIDATE_PAGE_SIZE,
}: SearchRequestOptions): Promise<SearchBucket> {
  if (!query.trim() && !reason && !result) {
    return { items: [], total: 0, page, pageSize };
  }

  const recalled = await runCandidateRecall(query, reason);
  const hydrated = await hydrateCandidateRows(recalled);
  return runCandidatePrecision(hydrated, { reason, result, page, pageSize });
}

async function runCandidateSearchWithDebug(
  options: SearchRequestOptions,
  parsedCandidateQuery: Awaited<ReturnType<typeof parseCandidateQuery>> | null
): Promise<{ bucket: SearchBucket; debug?: SearchDebugCandidateBucket }> {
  const recalled = await runCandidateRecall(options.query, options.reason || '');
  const hydrated = await hydrateCandidateRows(recalled);
  const bucket = runCandidatePrecision(hydrated, {
    reason: options.reason || '',
    result: options.result || '',
    page: options.page ?? 0,
    pageSize: options.pageSize ?? CANDIDATE_PAGE_SIZE,
  });

  if (!IS_DEV || !parsedCandidateQuery) {
    return { bucket };
  }

  return {
    bucket,
    debug: toCandidateDebugBucket(bucket.items, parsedCandidateQuery, recalled),
  };
}

async function runCompareSearch(options: SearchRequestOptions): Promise<Pick<SearchResponsePayload, 'baseline' | 'candidate' | 'baselineError' | 'candidateError'>> {
  const compareState: Pick<SearchResponsePayload, 'baseline' | 'candidate' | 'baselineError' | 'candidateError'> = {};

  try {
    compareState.baseline = await runBaselineSearch({ ...options, page: options.page ?? 0, pageSize: COMPARE_BUCKET_SIZE });
  } catch (error) {
    compareState.baseline = { items: [], total: 0, page: options.page ?? 0, pageSize: COMPARE_BUCKET_SIZE };
    compareState.baselineError = error instanceof Error ? error.message : 'baseline search failed';
  }

  try {
    compareState.candidate = await runCandidateSearch({ ...options, page: 0, pageSize: COMPARE_BUCKET_SIZE });
  } catch (error) {
    compareState.candidate = { items: [], total: 0, page: 0, pageSize: COMPARE_BUCKET_SIZE };
    compareState.candidateError = error instanceof Error ? error.message : 'candidate search failed';
  }

  return compareState;
}

export async function runSearch(options: SearchRequestOptions): Promise<SearchResponsePayload> {
  const page = options.page ?? 0;
  const effectiveQuery = options.query.trim() || (options.reason ? REASON_TO_QUERY[options.reason] || options.reason : '');
  const parsedCandidateQuery = options.mode !== 'baseline' && effectiveQuery
    ? await parseCandidateQuery(effectiveQuery)
    : null;

  const payload: SearchResponsePayload = {
    mode: options.mode,
    query: options.query,
    reason: options.reason || '',
    result: options.result || '',
    baseline: options.mode === 'candidate' ? undefined : { items: [], total: 0, page, pageSize: options.mode === 'compare' ? COMPARE_BUCKET_SIZE : BASELINE_PAGE_SIZE },
    candidate: options.mode === 'baseline' ? undefined : { items: [], total: 0, page: 0, pageSize: CANDIDATE_PAGE_SIZE },
  };

  if (options.mode === 'baseline') {
    try {
      payload.baseline = await runBaselineSearch({ ...options, page, pageSize: BASELINE_PAGE_SIZE });
      if (IS_DEV && payload.baseline) {
        payload.debug = {
          baseline: toDebugBucket(payload.baseline.items),
        };
      }
    } catch (error) {
      payload.baselineError = error instanceof Error ? error.message : 'baseline search failed';
    }
    return payload;
  }

  if (options.mode === 'candidate') {
    try {
      const candidateState = await runCandidateSearchWithDebug(
        { ...options, page: 0, pageSize: CANDIDATE_PAGE_SIZE },
        parsedCandidateQuery
      );
      payload.candidate = candidateState.bucket;
      if (IS_DEV && payload.candidate && parsedCandidateQuery) {
        payload.debug = {
          candidate: candidateState.debug,
        };
      }
    } catch (error) {
      payload.candidateError = error instanceof Error ? error.message : 'candidate search failed';
    }
    return payload;
  }

  const compareState = await runCompareSearch(options);
  const compareCandidateDebug =
    IS_DEV && parsedCandidateQuery && compareState.candidate
      ? toCandidateDebugBucket(compareState.candidate.items, parsedCandidateQuery, await runCandidateRecall(options.query, options.reason || ''))
      : undefined;
  const debug = IS_DEV
    ? {
        baseline: compareState.baseline ? toDebugBucket(compareState.baseline.items) : undefined,
        candidate: compareCandidateDebug,
      }
    : undefined;
  return {
    ...payload,
    ...compareState,
    debug,
  };
}
