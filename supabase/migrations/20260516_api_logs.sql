-- api_logs — /api/search, /api/sanction, /api/log-event 행동 집계용
-- 원칙: PII 미저장 (query_short 최대 40자 + 마스킹, 원문 사건내용/AI 응답 전문 X)
-- 30일 보존: pg_cron 미가용 → Hermes 서버2의 외부 cron이 매일 03:00 cleanup 실행
--   delete from public.api_logs where created_at < now() - interval '30 days';

create extension if not exists pgcrypto;

create table if not exists public.api_logs (
  id uuid primary key default gen_random_uuid(),

  created_at timestamptz not null default now(),
  route text not null,
  event_type text not null,

  -- request context
  method text,
  mode text,
  reason text,
  result_filter text,
  query_short text,
  query_hash text,

  -- response summary
  status text not null default 'ok',
  status_code integer,
  latency_ms integer,

  result_count integer,
  baseline_count integer,
  candidate_count integer,
  returned_case_ids text[],
  returned_case_titles text[],

  -- AI-specific summary
  stream boolean,
  tag_count integer,
  retrieved_case_count integer,
  comparison_worker_case_count integer,
  comparison_employer_case_count integer,
  ai_model text,
  error_class text,

  -- click-specific summary
  clicked_case_id text,
  clicked_case_title text,
  clicked_source text,
  source_provider text,

  -- safe extensibility only
  metadata jsonb not null default '{}'::jsonb
);

create index if not exists api_logs_created_at_idx
  on public.api_logs (created_at desc);

create index if not exists api_logs_route_created_at_idx
  on public.api_logs (route, created_at desc);

create index if not exists api_logs_event_type_created_at_idx
  on public.api_logs (event_type, created_at desc);

create index if not exists api_logs_mode_created_at_idx
  on public.api_logs (mode, created_at desc);
