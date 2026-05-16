import { NextRequest, NextResponse } from 'next/server';
import type { DecisionResult, ReasonCategory } from '@/lib/types';
import { runSearch } from '@/lib/search/search-modes';
import type { SearchMode } from '@/lib/search/types';
import { hashText, logApiEvent, safeIds, safeTitles, shortText } from '@/lib/api-logger';

function asMode(value: string | null): SearchMode {
  if (value === 'candidate' || value === 'compare') return value;
  return 'baseline';
}

export async function GET(req: NextRequest) {
  const startedAt = Date.now();
  const { searchParams } = new URL(req.url);
  const mode = asMode(searchParams.get('mode'));
  const query = searchParams.get('q') || '';
  const reason = ((searchParams.get('reason') as ReasonCategory | null) || '') as ReasonCategory | '';
  const result = ((searchParams.get('result') as DecisionResult | null) || '') as DecisionResult | '';
  const page = Number(searchParams.get('page') || '0');

  try {
    const payload = await runSearch({
      mode,
      query,
      reason,
      result,
      page: Number.isFinite(page) ? page : 0,
    });

    const baselineCount = payload.baseline?.total ?? 0;
    const candidateCount = payload.candidate?.total ?? 0;
    const items = [
      ...(payload.baseline?.items ?? []),
      ...(payload.candidate?.items ?? []),
    ];

    void logApiEvent({
      route: '/api/search',
      event_type: 'search_performed',
      method: 'GET',
      mode,
      reason: reason || null,
      result_filter: result || null,
      query_short: shortText(query),
      query_hash: hashText(query),
      status: 'ok',
      status_code: 200,
      latency_ms: Date.now() - startedAt,
      result_count:
        mode === 'candidate'
          ? candidateCount
          : mode === 'compare'
            ? baselineCount + candidateCount
            : baselineCount,
      baseline_count: baselineCount,
      candidate_count: candidateCount,
      returned_case_ids: safeIds(items),
      returned_case_titles: safeTitles(items),
    });

    return NextResponse.json(payload);
  } catch (error) {
    void logApiEvent({
      route: '/api/search',
      event_type: 'search_performed',
      method: 'GET',
      mode,
      reason: reason || null,
      result_filter: result || null,
      query_short: shortText(query),
      query_hash: hashText(query),
      status: 'error',
      status_code: 500,
      latency_ms: Date.now() - startedAt,
      error_class: error instanceof Error ? error.name : 'UnknownError',
    });

    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'Unknown search error',
      },
      { status: 500 }
    );
  }
}
