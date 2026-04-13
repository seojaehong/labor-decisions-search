-- Fix: no-category 쿼리에서 전체 문자열 ILIKE 대신 키워드 분리 매칭
-- 문제: "정직 처분 양정이 적정한지 본 사건" 전체를 ILIKE로 찾으면 0건
-- 해결: 쿼리를 공백으로 분리하여 2글자 이상 키워드 중 2개 이상 매칭

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
language plpgsql
stable
as $$
declare
  q text := trim(query);
  c text := nullif(trim(category), '');
  keywords text[];
  kw1 text;
  kw2 text;
  kw3 text;
begin
  -- 쿼리에서 2글자 이상 키워드 추출 (최대 3개)
  select array_agg(w order by length(w) desc)
  into keywords
  from unnest(regexp_split_to_array(q, '\s+')) as w
  where length(w) >= 2;

  kw1 := coalesce(keywords[1], q);
  kw2 := coalesce(keywords[2], '');
  kw3 := coalesce(keywords[3], '');

  return query
  with candidate_pool as (
    select
      n.id, n.title, n.decision_result, n.holding_summary, n.summary_short,
      n.key_issue, n.reason_category, n.sanction_type, n.decision_date, n.url,
      public.compute_search_trigram_score(q, n.title, n.holding_summary, n.key_issue, n.summary_short) as trigram_score
    from nlrc_decisions n
    where
      case
        -- 카테고리가 있으면: 카테고리 필터 + trigram/ILIKE
        when c is not null then (
          n.reason_category @> array[c]::text[]
          or n.title % q
          or coalesce(n.holding_summary, '') % q
          or coalesce(n.key_issue, '') % q
          or coalesce(n.summary_short, '') % q
          or n.title ilike '%' || q || '%'
          or coalesce(n.holding_summary, '') ilike '%' || q || '%'
          or coalesce(n.key_issue, '') ilike '%' || q || '%'
          or coalesce(n.summary_short, '') ilike '%' || q || '%'
        )
        -- 카테고리 없으면: 키워드 분리 매칭 (2개 이상 키워드 동시 포함)
        else (
          -- trigram 매칭 (인덱스 활용)
          n.title % q
          or coalesce(n.holding_summary, '') % q
          or coalesce(n.key_issue, '') % q
          -- 키워드1 ILIKE (가장 긴 키워드)
          or (
            (n.title ilike '%' || kw1 || '%'
             or coalesce(n.holding_summary, '') ilike '%' || kw1 || '%'
             or coalesce(n.key_issue, '') ilike '%' || kw1 || '%')
            and (
              kw2 = ''
              or n.title ilike '%' || kw2 || '%'
              or coalesce(n.holding_summary, '') ilike '%' || kw2 || '%'
              or coalesce(n.key_issue, '') ilike '%' || kw2 || '%'
            )
          )
        )
      end
    order by
      case when c is not null and n.reason_category @> array[c]::text[] then 1 else 0 end desc,
      public.compute_search_trigram_score(q, n.title, n.holding_summary, n.key_issue, n.summary_short) desc,
      n.decision_date desc nulls last
    limit 500
  ),
  scored as (
    select
      cp.id, cp.title, cp.decision_result, cp.holding_summary, cp.summary_short,
      cp.key_issue, cp.reason_category, cp.sanction_type, cp.decision_date, cp.url,
      (
        cp.trigram_score
        + case when c is not null and cp.reason_category @> array[c]::text[] then 0.08 else 0 end
        + public.compute_search_metadata_boost(q, cp.sanction_type, cp.reason_category, cp.holding_summary, cp.title)
      )::real as relevance
    from candidate_pool cp
  )
  select
    s.id, s.title, s.decision_result, s.holding_summary, s.summary_short,
    s.key_issue, s.reason_category, s.sanction_type, s.decision_date, s.url,
    s.relevance
  from scored s
  order by s.relevance desc, s.decision_date desc nulls last
  limit greatest("limit", 1);
end;
$$;
