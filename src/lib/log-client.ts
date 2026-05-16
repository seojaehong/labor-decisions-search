// Client-side click event reporter — fires-and-forgets to /api/log-event.
// Uses navigator.sendBeacon when available so the request survives navigation.

type ClickEvent =
  | 'search_result_click'
  | 'ai_comparison_case_click'
  | 'decision_detail_open';

type ClickPayload = {
  event_type: ClickEvent;
  clicked_case_id?: string | null;
  clicked_case_title?: string | null;
  clicked_source?: 'baseline' | 'candidate' | 'compare' | 'ai' | 'detail' | null;
  source_provider?: 'nlrc' | 'bigcase' | 'lawgo' | 'court' | null;
};

export function reportClick(payload: ClickPayload): void {
  if (typeof window === 'undefined') return;

  const body = JSON.stringify(payload);

  try {
    if (typeof navigator !== 'undefined' && typeof navigator.sendBeacon === 'function') {
      const blob = new Blob([body], { type: 'application/json' });
      const ok = navigator.sendBeacon('/api/log-event', blob);
      if (ok) return;
    }
  } catch {
    /* sendBeacon failed → fallback to fetch */
  }

  try {
    fetch('/api/log-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true,
    }).catch(() => {});
  } catch {
    /* fail open */
  }
}
