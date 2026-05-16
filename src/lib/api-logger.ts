import { createHash } from 'crypto';
import { supabaseServer } from '@/lib/supabase-server';

const MAX_QUERY_SHORT = 40;
const MAX_TITLE_LEN = 80;
const MAX_IDS = 10;
const MAX_TITLES = 5;

function redactSensitive(text: string): string {
  return text
    .replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi, '[email]')
    .replace(/01[016789]-?\d{3,4}-?\d{4}/g, '[phone]')
    .replace(/\d{3}-?\d{2}-?\d{5}/g, '[bizno]')
    .replace(/\d{6}-?\d{7}/g, '[rrn]');
}

export function shortText(text?: string | null, max = MAX_QUERY_SHORT): string | null {
  if (!text) return null;
  const clean = redactSensitive(text).trim().replace(/\s+/g, ' ');
  return clean ? clean.slice(0, max) : null;
}

export function hashText(text?: string | null): string | null {
  if (!text) return null;
  return createHash('sha256').update(text).digest('hex');
}

export function safeTitles(items: Array<{ title?: unknown }> | undefined, limit = MAX_TITLES): string[] {
  return (items || [])
    .slice(0, limit)
    .map((item) => String(item?.title ?? '').slice(0, MAX_TITLE_LEN))
    .filter(Boolean);
}

export function safeIds(items: Array<{ id?: unknown }> | undefined, limit = MAX_IDS): string[] {
  return (items || [])
    .slice(0, limit)
    .map((item) => String(item?.id ?? ''))
    .filter(Boolean);
}

export async function logApiEvent(payload: Record<string, unknown>): Promise<void> {
  try {
    const { error } = await supabaseServer.from('api_logs').insert(payload);
    if (error && process.env.NODE_ENV === 'development') {
      console.warn('[api_logs] insert failed', error.message);
    }
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      console.warn('[api_logs] unexpected failure', error);
    }
  }
}
