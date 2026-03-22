import type { DecisionResult, ReasonCategory } from '@/lib/types';

export type SearchMode = 'baseline' | 'candidate' | 'compare';

export interface SearchCard {
  id: string;
  title: string;
  case_number?: string | null;
  department: string | null;
  decision_date: string | null;
  decision_result: string;
  key_issue: string | null;
  holding_summary?: string | null;
  holding_points?: string | null;
  url: string | null;
  reason_category: string[];
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
  baselineError?: string;
  candidateError?: string;
}

export interface SearchRequestOptions {
  query: string;
  reason?: ReasonCategory | '';
  result?: DecisionResult | '';
  page?: number;
  pageSize?: number;
  mode: SearchMode;
}

export type QueryScenario =
  | 'generic'
  | 'absence_procedure'
  | 'regular_work_ability'
  | 'retaliation'
  | 'severity_excessive';

export interface ParsedCandidateQuery {
  raw_query: string;
  normalized_query: string;
  keywords: string[];
  intended_primary: string[];
  intended_stage: string[];
  intended_disposition: string[];
  must_have_markers: string[];
  penalized_markers: string[];
  query_scenario: QueryScenario;
  explanation: string;
}
