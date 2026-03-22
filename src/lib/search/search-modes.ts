import { createClient } from '@supabase/supabase-js';
import { extractTags, searchCases } from '@/lib/ai/retrieval';
import { normalizeQuery } from '@/lib/search/normalize-query';
import { parseCandidateQuery } from '@/lib/search/query-parser';
import type {
  SearchBucket,
  SearchCard,
  SearchRequestOptions,
  SearchResponsePayload,
} from '@/lib/search/types';
import type { DecisionResult, ReasonCategory } from '@/lib/types';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type CandidateMetaRow = Record<string, unknown>;

const COMPARE_BUCKET_SIZE = 5;
const BASELINE_PAGE_SIZE = 20;
const CANDIDATE_PAGE_SIZE = 5;

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

function matchesReason(reasonCategory: string[] | null | undefined, reason: ReasonCategory | ''): boolean {
  if (!reason) return true;
  return (reasonCategory || []).includes(reason);
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

async function runBaselineSearch({
  query,
  reason = '',
  result = '',
  page = 0,
  pageSize = BASELINE_PAGE_SIZE,
}: SearchRequestOptions): Promise<SearchBucket> {
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
    } catch (error) {
      payload.baselineError = error instanceof Error ? error.message : 'baseline search failed';
    }
    return payload;
  }

  if (options.mode === 'candidate') {
    try {
      payload.candidate = await runCandidateSearch({ ...options, page: 0, pageSize: CANDIDATE_PAGE_SIZE });
    } catch (error) {
      payload.candidateError = error instanceof Error ? error.message : 'candidate search failed';
    }
    return payload;
  }

  const compareState = await runCompareSearch(options);
  return {
    ...payload,
    ...compareState,
  };
}
