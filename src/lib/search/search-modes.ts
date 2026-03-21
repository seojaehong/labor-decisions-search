import { createClient } from '@supabase/supabase-js';
import { extractTags, searchCases } from '@/lib/ai/retrieval';
import type { DecisionResult, ReasonCategory } from '@/lib/types';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export type SearchMode = 'baseline' | 'candidate' | 'compare';

export interface SearchCard {
  id: string;
  title: string;
  department: string | null;
  decision_date: string | null;
  decision_result: string;
  key_issue: string | null;
  url: string | null;
  reason_category: string[];
  case_id?: string;
  employment_stage?: string | null;
  issue_type_primary?: string | null;
  issue_type_secondary?: string[];
  disposition_type?: string[];
  fact_markers?: string[];
  legal_focus?: string[];
  exclusion_flags?: string[];
  why_surfaced?: string[];
  score?: number | null;
}

export interface SearchBucket {
  items: SearchCard[];
  total: number;
  page: number;
  pageSize: number;
}

export interface SearchResponsePayload {
  mode: SearchMode;
  query: string;
  reason: ReasonCategory | '';
  result: DecisionResult | '';
  baseline?: SearchBucket;
  candidate?: SearchBucket;
}

export interface SearchRequestOptions {
  query: string;
  reason?: ReasonCategory | '';
  result?: DecisionResult | '';
  page?: number;
  pageSize?: number;
  mode: SearchMode;
}

type CandidateMetaRow = Record<string, unknown>;

function toStringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === 'string') : [];
}

function matchesReason(reasonCategory: string[] | null | undefined, reason: ReasonCategory | ''): boolean {
  if (!reason) return true;
  return (reasonCategory || []).includes(reason);
}

function toBaselineWhy(query: string, reason: ReasonCategory | '', result: DecisionResult | ''): string[] {
  const why: string[] = [];
  if (reason) why.push(`reason:${reason}`);
  if (result) why.push(`result:${result}`);
  if (query) why.push(`text:${query}`);
  return why;
}

async function runBaselineSearch({
  query,
  reason = '',
  result = '',
  page = 0,
  pageSize = 20,
}: SearchRequestOptions): Promise<SearchBucket> {
  let q = supabase
    .from('nlrc_decisions')
    .select('id, title, department, decision_date, decision_result, key_issue, url, reason_category', { count: 'exact' })
    .range(page * pageSize, (page + 1) * pageSize - 1)
    .order('decision_date', { ascending: false });

  if (reason) q = q.contains('reason_category', [reason]);
  if (result) q = q.eq('decision_result', result);
  if (query) q = q.textSearch('search_vector', query.split(' ').join(' & '));

  const { data, count, error } = await q;
  if (error) throw error;

  const items: SearchCard[] = (data || []).map((row) => ({
    id: row.id,
    title: row.title,
    department: row.department,
    decision_date: row.decision_date,
    decision_result: row.decision_result,
    key_issue: row.key_issue,
    url: row.url,
    reason_category: row.reason_category || [],
    why_surfaced: toBaselineWhy(query, reason, result),
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
    .select('id, title, department, decision_date, decision_result, key_issue, url, reason_category')
    .in('id', ids);

  if (error) throw error;

  const baseById = new Map((data || []).map((row) => [row.id, row]));

  return rows.map((row) => {
    const base = baseById.get(String(row.id));
    return {
      id: String(row.id),
      title: base?.title || String(row.title || ''),
      department: base?.department || null,
      decision_date: base?.decision_date || null,
      decision_result: base?.decision_result || String(row.decision_result || ''),
      key_issue: base?.key_issue || null,
      url: base?.url || null,
      reason_category: base?.reason_category || [],
      case_id: typeof row.id === 'string' ? row.id : String(row.id),
      employment_stage: typeof row.employment_stage === 'string' ? row.employment_stage : null,
      issue_type_primary: typeof row.issue_type_primary === 'string' ? row.issue_type_primary : null,
      issue_type_secondary: toStringArray(row.issue_type_secondary),
      disposition_type: toStringArray(row.disposition_type),
      fact_markers: toStringArray(row.fact_markers),
      legal_focus: toStringArray(row.legal_focus),
      exclusion_flags: toStringArray(row.exclusion_flags),
      why_surfaced: toStringArray(row._score_reasons),
      score: typeof row._score === 'number' ? row._score : null,
    };
  });
}

async function runCandidateSearch({
  query,
  reason = '',
  result = '',
  page = 0,
  pageSize = 5,
}: SearchRequestOptions): Promise<SearchBucket> {
  if (!query.trim()) {
    return { items: [], total: 0, page, pageSize };
  }

  const tags = extractTags(query);
  const retrieval = await searchCases(tags, query);
  let items = await hydrateCandidateRows(retrieval.allCases);

  items = items.filter((item) => {
    if (result && item.decision_result !== result) return false;
    if (!matchesReason(item.reason_category, reason)) return false;
    return true;
  });

  const total = items.length;
  const paged = items.slice(page * pageSize, (page + 1) * pageSize);

  return {
    items: paged,
    total,
    page,
    pageSize,
  };
}

export async function runSearch(options: SearchRequestOptions): Promise<SearchResponsePayload> {
  const page = options.page ?? 0;
  const pageSize = options.pageSize ?? (options.mode === 'baseline' ? 20 : 5);

  const payload: SearchResponsePayload = {
    mode: options.mode,
    query: options.query,
    reason: options.reason || '',
    result: options.result || '',
  };

  if (options.mode === 'baseline' || options.mode === 'compare') {
    payload.baseline = await runBaselineSearch({ ...options, page, pageSize: options.mode === 'compare' ? 5 : pageSize });
  }

  if (options.mode === 'candidate' || options.mode === 'compare') {
    payload.candidate = await runCandidateSearch({ ...options, page: 0, pageSize: 5 });
  }

  return payload;
}
