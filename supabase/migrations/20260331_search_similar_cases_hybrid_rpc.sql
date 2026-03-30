create extension if not exists pg_trgm;
create extension if not exists vector;

create index if not exists idx_nlrc_decisions_embedding
  on nlrc_decisions
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

create or replace function public.compute_search_trigram_score(
  query text,
  title text,
  holding_summary text,
  key_issue text,
  summary_short text
)
returns real
language sql
immutable
as $$
  select greatest(
    similarity(coalesce(title, ''), query),
    word_similarity(query, coalesce(title, '')),
    similarity(coalesce(holding_summary, ''), query),
    word_similarity(query, coalesce(holding_summary, '')),
    similarity(coalesce(key_issue, ''), query),
    word_similarity(query, coalesce(key_issue, '')),
    similarity(coalesce(summary_short, ''), query),
    word_similarity(query, coalesce(summary_short, ''))
  )::real;
$$;

create or replace function public.compute_search_metadata_boost(
  query text,
  sanction_type text,
  reason_category text[],
  holding_summary text,
  title text
)
returns real
language sql
immutable
as $$
  select (
    case
      when query ~ '감봉' and coalesce(sanction_type, '') = 'pay_cut' then 0.15
      else 0
    end
    + case
      when query ~ '정직' and coalesce(sanction_type, '') = 'suspension' then 0.12
      else 0
    end
    + case
      when query ~ '(여러|함께|복합|복수).*(비위|사유)|비위.*(여러|함께|복합|복수)|정당성 전체'
        and coalesce(array_length(reason_category, 1), 0) >= 3 then 0.10
      else 0
    end
    + case
      when query ~ '(여러|함께|복합|복수|정당성|양정|과하|정당)'
        and coalesce(holding_summary, '') ~ '징계사유'
        and coalesce(holding_summary, '') ~ '(양정|과하|정당)' then 0.08
      else 0
    end
    + case
      when query ~ '(택시|버스|기사|운전|운수)'
        and (coalesce(title, '') || ' ' || coalesce(holding_summary, '')) ~ '(택시|버스|기사|운전|운수)' then 0.12
      else 0
    end
    + case
      when query ~ '(개선|시정|경고|교육|기회|주고도|부여|업무능력|저성과)'
        and coalesce(holding_summary, '') ~ '(개선|시정|경고|교육|기회|주고도|부여)' then 0.10
      else 0
    end
  )::real;
$$;

drop function if exists public.search_similar_cases(text, text, integer);

create or replace function public.search_similar_cases(
  query text,
  category text default '',
  "limit" integer default 5
)
returns table (
  id text,
  title text,
  decision_result text,
  holding_summary text,
  summary_short text,
  key_issue text,
  reason_category text[],
  sanction_type text,
  decision_date date,
  url text,
  relevance real
)
language sql
stable
as $$
  with params as (
    select
      trim(query) as q,
      nullif(trim(category), '') as c
  ),
  candidate_pool as (
    select
      n.id,
      n.title,
      n.decision_result,
      n.holding_summary,
      n.summary_short,
      n.key_issue,
      n.reason_category,
      n.sanction_type,
      n.decision_date,
      n.url,
      public.compute_search_trigram_score(p.q, n.title, n.holding_summary, n.key_issue, n.summary_short) as trigram_score
    from nlrc_decisions n
    cross join params p
    where (
      (p.c is not null and n.reason_category @> array[p.c]::text[])
      or (
        n.title % p.q
        or coalesce(n.holding_summary, '') % p.q
        or coalesce(n.key_issue, '') % p.q
        or coalesce(n.summary_short, '') % p.q
        or n.title ilike '%' || p.q || '%'
        or coalesce(n.holding_summary, '') ilike '%' || p.q || '%'
        or coalesce(n.key_issue, '') ilike '%' || p.q || '%'
        or coalesce(n.summary_short, '') ilike '%' || p.q || '%'
      )
    )
    order by
      case when p.c is not null and n.reason_category @> array[p.c]::text[] then 1 else 0 end desc,
      public.compute_search_trigram_score(p.q, n.title, n.holding_summary, n.key_issue, n.summary_short) desc,
      n.decision_date desc nulls last
    limit 500
  ),
  scored as (
    select
      c.id,
      c.title,
      c.decision_result,
      c.holding_summary,
      c.summary_short,
      c.key_issue,
      c.reason_category,
      c.sanction_type,
      c.decision_date,
      c.url,
      (
        c.trigram_score
        + case when p.c is not null and c.reason_category @> array[p.c]::text[] then 0.08 else 0 end
        + public.compute_search_metadata_boost(p.q, c.sanction_type, c.reason_category, c.holding_summary, c.title)
      )::real as relevance
    from candidate_pool c
    cross join params p
  )
  select
    s.id,
    s.title,
    s.decision_result,
    s.holding_summary,
    s.summary_short,
    s.key_issue,
    s.reason_category,
    s.sanction_type,
    s.decision_date,
    s.url,
    s.relevance
  from scored s
  order by s.relevance desc, s.decision_date desc nulls last
  limit greatest("limit", 1);
$$;

drop function if exists public.search_similar_cases_hybrid(text, vector, text, integer, real, real);

create or replace function public.search_similar_cases_hybrid(
  query text,
  query_embedding vector,
  category text default '',
  "limit" integer default 5,
  trigram_weight real default 0.4,
  semantic_weight real default 0.6
)
returns table (
  id text,
  title text,
  decision_result text,
  holding_summary text,
  summary_short text,
  key_issue text,
  reason_category text[],
  sanction_type text,
  decision_date date,
  url text,
  relevance real
)
language sql
stable
as $$
  with params as (
    select
      trim(query) as q,
      nullif(trim(category), '') as c
  ),
  vector_candidates as (
    select
      n.id,
      n.title,
      n.decision_result,
      n.holding_summary,
      n.summary_short,
      n.key_issue,
      n.reason_category,
      n.sanction_type,
      n.decision_date,
      n.url,
      public.compute_search_trigram_score(p.q, n.title, n.holding_summary, n.key_issue, n.summary_short) as trigram_score,
      (1 - (n.embedding <=> query_embedding))::real as semantic_score
    from nlrc_decisions n
    cross join params p
    where n.embedding is not null
      and (
        p.c is null
        or n.reason_category @> array[p.c]::text[]
      )
    order by n.embedding <=> query_embedding
    limit case when (select c from params) is null then 500 else 200 end
  ),
  trigram_candidates as (
    select
      n.id,
      n.title,
      n.decision_result,
      n.holding_summary,
      n.summary_short,
      n.key_issue,
      n.reason_category,
      n.sanction_type,
      n.decision_date,
      n.url,
      public.compute_search_trigram_score(p.q, n.title, n.holding_summary, n.key_issue, n.summary_short) as trigram_score,
      (1 - (n.embedding <=> query_embedding))::real as semantic_score
    from nlrc_decisions n
    cross join params p
    where p.c is not null
      and (
        n.reason_category @> array[p.c]::text[]
        or n.title % p.q
        or coalesce(n.holding_summary, '') % p.q
        or coalesce(n.key_issue, '') % p.q
        or coalesce(n.summary_short, '') % p.q
        or n.title ilike '%' || p.q || '%'
        or coalesce(n.holding_summary, '') ilike '%' || p.q || '%'
        or coalesce(n.key_issue, '') ilike '%' || p.q || '%'
        or coalesce(n.summary_short, '') ilike '%' || p.q || '%'
      )
    order by public.compute_search_trigram_score(p.q, n.title, n.holding_summary, n.key_issue, n.summary_short) desc
    limit 200
  ),
  candidate_pool as (
    select distinct on (merged.id)
      merged.id,
      merged.title,
      merged.decision_result,
      merged.holding_summary,
      merged.summary_short,
      merged.key_issue,
      merged.reason_category,
      merged.sanction_type,
      merged.decision_date,
      merged.url,
      merged.trigram_score,
      merged.semantic_score
    from (
      select * from vector_candidates
      union all
      select * from trigram_candidates
    ) as merged
    order by merged.id, merged.semantic_score desc, merged.trigram_score desc
  ),
  scored as (
    select
      c.id,
      c.title,
      c.decision_result,
      c.holding_summary,
      c.summary_short,
      c.key_issue,
      c.reason_category,
      c.sanction_type,
      c.decision_date,
      c.url,
      (
        (trigram_weight * c.trigram_score)
        + (semantic_weight * c.semantic_score)
        + case when p.c is not null and c.reason_category @> array[p.c]::text[] then 0.08 else 0 end
        + public.compute_search_metadata_boost(p.q, c.sanction_type, c.reason_category, c.holding_summary, c.title)
      )::real as relevance
    from candidate_pool c
    cross join params p
  )
  select
    s.id,
    s.title,
    s.decision_result,
    s.holding_summary,
    s.summary_short,
    s.key_issue,
    s.reason_category,
    s.sanction_type,
    s.decision_date,
    s.url,
    s.relevance
  from scored s
  order by s.relevance desc, s.decision_date desc nulls last
  limit greatest("limit", 1);
$$;
