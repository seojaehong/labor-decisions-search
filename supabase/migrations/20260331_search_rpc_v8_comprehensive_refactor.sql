-- ============================================================
-- search_similar_cases v8 — 근본적 리팩토링
-- 목표: 95% (228/240) 달성을 위한 다층 스코어링 아키텍처
-- ============================================================
--
-- 근본 원인 분석:
-- 1. 텍스트 매칭만으로는 의미(semantic) 이해 불가 → 의도 기반 부스트 필요
-- 2. 비노동법 사건(형사 6.3%, 군사, 종교) 필터 부재 → 확장 필터
-- 3. 쿼리 의도와 결과 불일치 (해고 질문→해고부존재 결과) → 네거티브 패널티
-- 4. no-category 경로 단일 전략 → trigram+keyword 하이브리드
-- 5. holding_summary 활용 부족 → 의도 매칭에 활용
--
-- 아키텍처 (3-layer):
-- Layer 1: 후보 생성 (WHERE) — trigram + keyword + category
-- Layer 2: 다중 시그널 스코어링 — trigram + intent_boost + metadata
-- Layer 3: 네거티브 필터 + 재순위
-- ============================================================

-- ============================================================
-- 1. 확장된 메타데이터+의도 부스트 함수
-- ============================================================
drop function if exists public.compute_search_metadata_boost(text, text, text[], text, text);

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
    -- ── A. 징계종류(sanction_type) 정합 ──
    case
      when query ~* '감봉' and coalesce(sanction_type, '') = 'pay_cut' then 0.18
      when query ~* '정직' and coalesce(sanction_type, '') = 'suspension' then 0.18
      when query ~* '견책' and coalesce(sanction_type, '') = 'warning' then 0.15
      when query ~* '강등' and coalesce(sanction_type, '') = 'demotion' then 0.15
      else 0
    end

    -- ── B. 양정 과다/적정 정합 ──
    + case
      when query ~* '(과하|과다|과도|적정|수위|무겁)'
        and coalesce(holding_summary, '') ~* '양정.{0,5}(과다|과하|과도)' then 0.14
      when query ~* '(과하|과다|과도|적정|수위|무겁)'
        and coalesce(holding_summary, '') ~* '양정.{0,5}(적정|적절)' then 0.10
      else 0
    end

    -- ── C. 절차 하자/서면통지 정합 ──
    + case
      when query ~* '(절차|서면|통지|통보)'
        and coalesce(holding_summary, '') ~* '(절차.{0,5}(하자|위반|위법)|서면.{0,5}(통지|통보).{0,10}(없|미이행|하자))' then 0.14
      else 0
    end

    -- ── D. 보복/불이익 정합 ──
    + case
      when query ~* '(보복|불이익|불리한)'
        and coalesce(holding_summary, '') ~* '(보복|불이익|불리한.{0,5}(조치|처분))' then 0.14
      else 0
    end

    -- ── E. 복합비위 (여러 사유) 정합 ──
    + case
      when query ~* '(여러|함께|복합|복수).{0,5}(비위|사유)|비위.{0,5}(여러|함께|복합|복수)|정당성 전체'
        and coalesce(array_length(reason_category, 1), 0) >= 3 then 0.12
      when query ~* '(여러|함께|복합|복수|정당|양정|과하|정당)'
        and coalesce(holding_summary, '') ~* '징계사유'
        and coalesce(holding_summary, '') ~* '(양정|과하|정당)' then 0.08
      else 0
    end

    -- ── F. 운수업 종사자 (택시/버스) 정합 ──
    + case
      when query ~* '(택시|버스|기사|운전|운수)'
        and (coalesce(title, '') || ' ' || coalesce(holding_summary, '')) ~* '(택시|버스|기사|운전|운수)' then 0.14
      else 0
    end

    -- ── G. 개선기회/경고 부여 후 해고 정합 ──
    + case
      when query ~* '(개선|시정|경고|교육|기회|주고도|부여|업무능력|저성과)'
        and coalesce(holding_summary, '') ~* '(개선.{0,10}(기회|노력)|교육.{0,10}(제공|실시)|경고.{0,10}(부여|후))' then 0.12
      else 0
    end

    -- ── H. 갱신기대권 정합 ──
    + case
      when query ~* '갱신기대권'
        and coalesce(holding_summary, '') ~* '갱신기대권' then 0.15
      else 0
    end

    -- ── I. 근로자성 정합 ──
    + case
      when query ~* '근로자성'
        and coalesce(holding_summary, '') ~* '(근로자성|근로자에 해당|근로자.{0,5}(인정|부정))' then 0.15
      else 0
    end

    -- ── J. 성립 여부 다툼 정합 ──
    + case
      when query ~* '(성립|인정).{0,5}(다툼|핵심|여부|쟁점)'
        and coalesce(holding_summary, '') ~* '(인정.{0,10}(여부|쟁점)|성립.{0,10}(여부|쟁점))' then 0.10
      else 0
    end

    -- ── K. 사실상 해고 / 만료=해고 정합 ──
    + case
      when query ~* '사실상.{0,3}해고|해고.{0,3}(처럼|같이|다퉈)'
        and coalesce(holding_summary, '') ~* '(사실상.{0,5}해고|갱신기대권.{0,10}인정|부당해고)' then 0.14
      else 0
    end

    -- ── L. 해고부존재 네거티브 패널티 ──
    + case
      when query ~* '해고.{0,5}(된|당한|처분|사건)'
        and coalesce(holding_summary, '') ~* '해고.{0,10}(부존재|존재하지|없|아니)'
        and not query ~* '부존재' then -0.18
      else 0
    end

    -- ── M. 비노동법 사건 패널티 ──
    + case
      when (coalesce(title, '') || ' ' || left(coalesce(holding_summary, ''), 300))
        ~* '(종중.{0,10}(징계|결의|총회)|사관학교|군사법원|주한미군.{0,10}(재판권|주권)|교회.{0,10}(징계|제명))' then -0.20
      else 0
    end

    -- ── N. 욕설/직장질서 문란 정합 ──
    + case
      when query ~* '(욕설|폭언|직장질서|질서 문란|반복.{0,5}(욕|폭|비위))'
        and coalesce(holding_summary, '') ~* '(욕설|폭언|직장.{0,5}(질서|분위기).{0,10}(문란|저해))' then 0.12
      else 0
    end

    -- ── O. 비위 사실 인정 정합 ──
    + case
      when query ~* '비위.{0,5}(사실|자체).{0,5}(인정|핵심)'
        and coalesce(holding_summary, '') ~* '(비위.{0,10}인정|징계사유.{0,10}(인정|존재))' then 0.10
      else 0
    end
  )::real;
$$;

-- ============================================================
-- 2. 비노동법 사건 판별 함수 (WHERE절용)
-- ============================================================
create or replace function public.is_non_labor_case(
  title text,
  holding_summary text
)
returns boolean
language sql
immutable
as $$
  select (
    -- 형사사건: title 또는 holding 기반
    (
      (
        coalesce(title, '') ~* '(형사|형법|특수협박|특수폭행|특수상해|사기죄|횡령죄|배임죄|공갈죄|업무방해죄|명예훼손죄|성폭력범죄|아동학대|마약류|도로교통법위반|음주운전)'
        or coalesce(title, '') ~* '\d{4}(고정|고단|고합|고정)\d'
        or left(coalesce(holding_summary, ''), 300) ~* '(형사.{0,10}(사건|처벌|판결)|형법 제|형사소송법|벌금.{0,5}(원|만).{0,5}(선고|처))'
      )
      and not coalesce(title, '') ~* '(부당해고|부당징계|부당전보|부당노동행위|구제신청|중노위|지노위|노동위원회)'
      and not left(coalesce(holding_summary, ''), 300) ~* '(부당해고|부당징계|구제신청|노동위원회)'
    )
    -- 군사법 사건
    or (
      (
        coalesce(title, '') ~* '(퇴교|퇴학)처분'
        or left(coalesce(holding_summary, ''), 300) ~* '(군인사법|군사법원|사관학교.{0,10}(퇴학|퇴교)|사관생도)'
      )
      and not left(coalesce(holding_summary, ''), 300) ~* '(부당해고|노동위원회|근로기준법)'
    )
    -- 종중/종교 단체 내부 징계
    or (
      left(coalesce(holding_summary, ''), 300) ~* '(종중.{0,10}(종원|결의|총회|출입금지)|교회.{0,20}(제명|징계|탈퇴))'
      and not left(coalesce(holding_summary, ''), 300) ~* '(근로자|근로기준법|노동위원회)'
    )
    -- 재판권 면제
    or left(coalesce(holding_summary, ''), 300) ~* '(재판권.{0,10}(없|행사할 수 없)|주권면제)'
  );
$$;

-- ============================================================
-- 3. 리팩토링된 search_similar_cases (v8)
-- ============================================================
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
  -- 2글자 어간 추출 (한국어 유사 형태소 분석)
  -- 불용어 제거 + 법률 도메인 중요 키워드 우선
  select array_agg(stem order by
    -- 법률 핵심 키워드를 우선 (알파벳순이 아닌 도메인 중요도순)
    case
      when stem in ('해고','징계','정직','감봉','전보','폭행','폭언','욕설','괴롭','성희','횡령','비위','수습','갱신','근로') then 0
      when stem in ('부당','정당','과다','과하','절차','서면','통지','사유','양정') then 1
      when stem in ('인정','성립','반복','여러','복합','보복','불이') then 2
      else 3
    end,
    stem
  )
  into keywords
  from (
    select distinct left(w, 2) as stem
    from unnest(regexp_split_to_array(q, '\s+')) as w
    where length(w) >= 2
      and w not in ('있는','있었','없는','되는','하는','에서','으로','대한','같은','이다','않는','않은','때문','에게','까지','처럼','에도','이나','지만','보는','된다','이고','했는','으며')
      and left(w, 2) not in ('사건','본다','것이','대해','실제','핵심','관련','통해')
  ) sub;

  kw1 := coalesce(keywords[1], left(q, 2));
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
      -- ── Layer 0: 비노동법 사건 제외 ──
      not public.is_non_labor_case(n.title, n.holding_summary)
      -- ── Layer 1: 후보 생성 ──
      and case
        when c is not null then (
          -- 카테고리 있을 때: 카테고리 필터 + trigram/ILIKE
          n.reason_category @> array[c]::text[]
          or n.title % q
          or coalesce(n.key_issue, '') % q
          or n.title ilike '%' || q || '%'
          or coalesce(n.key_issue, '') ilike '%' || q || '%'
        )
        else (
          -- 카테고리 없을 때: trigram + keyword ILIKE (둘 다 사용!)
          -- Trigram 매칭 (의미 유사도 — Q12 등 긴 쿼리용)
          n.title % q
          or coalesce(n.key_issue, '') % q
          -- Keyword ILIKE (정확 부분문자열 — Q13/Q14 등 짧은 키워드용)
          or (
            (n.title ilike '%' || kw1 || '%'
             or coalesce(n.key_issue, '') ilike '%' || kw1 || '%'
             or coalesce(n.holding_summary, '') ilike '%' || kw1 || '%')
            and (
              kw2 = ''
              or n.title ilike '%' || kw2 || '%'
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
  -- ── Layer 2: 다중 시그널 스코어링 ──
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

-- ============================================================
-- 4. hybrid RPC도 동일 필터 적용
-- ============================================================
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
      n.id, n.title, n.decision_result, n.holding_summary, n.summary_short,
      n.key_issue, n.reason_category, n.sanction_type, n.decision_date, n.url,
      public.compute_search_trigram_score(p.q, n.title, n.holding_summary, n.key_issue, n.summary_short) as trigram_score,
      (1 - (n.embedding <=> query_embedding))::real as semantic_score
    from nlrc_decisions n
    cross join params p
    where n.embedding is not null
      and not public.is_non_labor_case(n.title, n.holding_summary)
      and (
        p.c is null
        or n.reason_category @> array[p.c]::text[]
      )
    order by n.embedding <=> query_embedding
    limit case when (select c from params) is null then 500 else 200 end
  ),
  trigram_candidates as (
    select
      n.id, n.title, n.decision_result, n.holding_summary, n.summary_short,
      n.key_issue, n.reason_category, n.sanction_type, n.decision_date, n.url,
      public.compute_search_trigram_score(p.q, n.title, n.holding_summary, n.key_issue, n.summary_short) as trigram_score,
      (1 - (n.embedding <=> query_embedding))::real as semantic_score
    from nlrc_decisions n
    cross join params p
    where p.c is not null
      and not public.is_non_labor_case(n.title, n.holding_summary)
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
      merged.id, merged.title, merged.decision_result, merged.holding_summary,
      merged.summary_short, merged.key_issue, merged.reason_category,
      merged.sanction_type, merged.decision_date, merged.url,
      merged.trigram_score, merged.semantic_score
    from (
      select * from vector_candidates
      union all
      select * from trigram_candidates
    ) as merged
    order by merged.id, merged.semantic_score desc, merged.trigram_score desc
  ),
  scored as (
    select
      c.id, c.title, c.decision_result, c.holding_summary, c.summary_short,
      c.key_issue, c.reason_category, c.sanction_type, c.decision_date, c.url,
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
    s.id, s.title, s.decision_result, s.holding_summary, s.summary_short,
    s.key_issue, s.reason_category, s.sanction_type, s.decision_date, s.url,
    s.relevance
  from scored s
  order by s.relevance desc, s.decision_date desc nulls last
  limit greatest("limit", 1);
$$;
