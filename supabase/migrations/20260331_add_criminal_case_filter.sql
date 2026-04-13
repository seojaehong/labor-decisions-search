-- 형사/비노동법 사건 필터 추가
-- 문제: 형사사건(형법, 사기죄 등)이 노동 판정례 검색 결과에 혼입
-- 해결: WHERE절에 형사 키워드 제외 필터 추가 (단, 부당해고/부당징계 등 노동위 사건은 보존)

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
begin
  -- 2글자 어간 추출 (한국어 조사/어미 제거 효과)
  select array_agg(distinct left(w, 2) order by left(w, 2))
  into keywords
  from unnest(regexp_split_to_array(q, '\s+')) as w
  where length(w) >= 2
    and w not in ('있는', '있었', '없는', '되는', '하는', '에서', '으로', '대한', '같은', '이다', '않는', '않은', '때문');

  kw1 := coalesce(keywords[1], left(q, 2));
  kw2 := coalesce(keywords[2], '');

  return query
  with candidate_pool as (
    select
      n.id, n.title, n.decision_result, n.holding_summary, n.summary_short,
      n.key_issue, n.reason_category, n.sanction_type, n.decision_date, n.url,
      public.compute_search_trigram_score(q, n.title, n.holding_summary, n.key_issue, n.summary_short) as trigram_score
    from nlrc_decisions n
    where
      -- 형사/비노동법 사건 제외 (노동위 사건은 보존)
      not (
        coalesce(n.title, '') ~* '(형사|형법|특수협박|특수폭행|특수상해|군인사법|사기죄|횡령죄|배임죄|공갈죄|업무방해죄|명예훼손죄|성폭력범죄|아동학대|마약류|도로교통법위반|음주운전)'
        and not coalesce(n.title, '') ~* '(부당해고|부당징계|부당전보|부당노동행위|구제신청|중노위|지노위|노동위원회)'
      )
      and case
        when c is not null then (
          n.reason_category @> array[c]::text[]
          or n.title % q
          or coalesce(n.key_issue, '') % q
          or n.title ilike '%' || q || '%'
          or coalesce(n.key_issue, '') ilike '%' || q || '%'
        )
        else (
          (n.title ilike '%' || kw1 || '%' or coalesce(n.key_issue, '') ilike '%' || kw1 || '%')
          and (
            kw2 = ''
            or n.title ilike '%' || kw2 || '%'
            or coalesce(n.key_issue, '') ilike '%' || kw2 || '%'
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
