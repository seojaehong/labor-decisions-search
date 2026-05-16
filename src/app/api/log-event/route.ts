import { NextRequest, NextResponse } from 'next/server';
import { logApiEvent, shortText } from '@/lib/api-logger';

const ALLOWED_EVENTS = new Set([
  'search_result_click',
  'ai_comparison_case_click',
  'decision_detail_open',
]);

const ALLOWED_SOURCES = new Set([
  'baseline',
  'candidate',
  'compare',
  'ai',
  'detail',
]);

const ALLOWED_PROVIDERS = new Set([
  'nlrc',
  'bigcase',
  'lawgo',
  'court',
]);

function clampStr(value: unknown, max: number): string | null {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  if (!trimmed) return null;
  return trimmed.slice(0, max);
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => null);
    if (!body || typeof body !== 'object') {
      return NextResponse.json({ ok: false, error: 'invalid body' }, { status: 400 });
    }

    const eventType = typeof body.event_type === 'string' ? body.event_type : '';
    if (!ALLOWED_EVENTS.has(eventType)) {
      return NextResponse.json({ ok: false, error: 'event_type not allowed' }, { status: 400 });
    }

    const clickedSourceRaw = clampStr(body.clicked_source, 24);
    const sourceProviderRaw = clampStr(body.source_provider, 24);

    void logApiEvent({
      route: '/api/log-event',
      event_type: eventType,
      method: 'POST',
      status: 'ok',
      status_code: 200,
      clicked_case_id: clampStr(body.clicked_case_id, 64),
      clicked_case_title: shortText(typeof body.clicked_case_title === 'string' ? body.clicked_case_title : null, 80),
      clicked_source: clickedSourceRaw && ALLOWED_SOURCES.has(clickedSourceRaw) ? clickedSourceRaw : null,
      source_provider: sourceProviderRaw && ALLOWED_PROVIDERS.has(sourceProviderRaw) ? sourceProviderRaw : null,
    });

    return NextResponse.json({ ok: true });
  } catch (error) {
    return NextResponse.json(
      { ok: false, error: error instanceof Error ? error.name : 'UnknownError' },
      { status: 500 },
    );
  }
}
