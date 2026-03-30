CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS idx_nlrc_decisions_similarity_text
  ON nlrc_decisions
  USING gin (
    (
      coalesce(title, '') || ' ' ||
      coalesce(holding_summary, '') || ' ' ||
      coalesce(holding_points, '')
    ) gin_trgm_ops
  );

DROP FUNCTION IF EXISTS public.search_similar_cases(text, text, integer);

CREATE OR REPLACE FUNCTION public.search_similar_cases(
  query text,
  category text DEFAULT NULL,
  "limit" integer DEFAULT 5
)
RETURNS TABLE (
  id text,
  case_number text,
  title text,
  department text,
  decision_date date,
  case_type text,
  decision_result text,
  reason_category text[],
  holding_summary text,
  holding_points text,
  relevance real
)
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
  normalized_query text := trim(coalesce(query, ''));
  normalized_category text := lower(regexp_replace(coalesce(category, ''), '\s+', '', 'g'));
  per_bucket_limit integer := greatest(coalesce("limit", 5), 1);
  has_category boolean;
BEGIN
  IF normalized_query = '' THEN
    RETURN;
  END IF;

  has_category := (normalized_category != '');

  RETURN QUERY
  WITH query_tokens AS (
    SELECT DISTINCT token
    FROM regexp_split_to_table(normalized_query, '\s+') AS token
    WHERE char_length(token) >= 2
  ),
  candidate_pool AS (
    SELECT
      d.id,
      d.case_number,
      d.title,
      d.department,
      d.decision_date,
      d.case_type,
      d.decision_result,
      d.reason_category,
      d.holding_summary,
      d.holding_points,
      d.sanction_type,
      coalesce(d.title, '') || ' ' || coalesce(d.holding_summary, '') || ' ' || coalesce(d.holding_points, '') AS search_text
    FROM nlrc_decisions AS d
    WHERE coalesce(d.case_type, '') NOT IN ('형사', '헌법', '특허', '신청')
    AND (
      -- Category filter: pass through when no category given
      NOT has_category
      OR normalized_category NOT IN (
        '부당해고', '해고', 'dismissal',
        '부당노동행위', '노동조합', '노조', 'union_activity',
        '부당징계', '징계', 'discipline',
        '무단결근', '결근', 'absence',
        '성희롱', 'sexual_harassment',
        '직장내괴롭힘', '괴롭힘', 'workplace_bullying',
        '전보', '인사이동', 'transfer',
        '수습', '시용', 'probation',
        '갱신기대권', '계약만료', 'contract_expiry',
        '해고부존재', '사직', 'no_dismissal',
        '근로자성', 'worker_status',
        '차별', '차별시정', 'discrimination',
        '경영상해고', '정리해고', 'redundancy',
        '비위행위', 'misconduct',
        '폭행', '폭언', 'violence',
        '횡령', '배임', 'embezzlement',
        '업무능력부족', '저성과', 'incompetence',
        '양정', '징계양정', '양정과다', 'disciplinary_severity'
      )
      OR (normalized_category IN ('부당해고', '해고', 'dismissal')
        AND (d.sanction_type = 'dismissal' OR coalesce(d.case_type, '') ILIKE '%부당해고%' OR coalesce(d.title, '') ILIKE '%해고%'))
      OR (normalized_category IN ('부당노동행위', '노동조합', '노조', 'union_activity')
        AND (coalesce(d.reason_category, '{}'::text[]) && ARRAY['union_activity'] OR coalesce(d.case_type, '') ILIKE '%부당노동행위%' OR coalesce(d.title, '') ILIKE '%노동조합%'))
      OR (normalized_category IN ('부당징계', '징계', 'discipline')
        AND (d.sanction_type IN ('suspension', 'pay_cut', 'warning', 'demotion') OR coalesce(d.case_type, '') ILIKE '%부당징계%' OR coalesce(d.title, '') ILIKE '%징계%'))
      OR (normalized_category IN ('무단결근', '결근', 'absence') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['absence'])
      OR (normalized_category IN ('성희롱', 'sexual_harassment') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['sexual_harassment'])
      OR (normalized_category IN ('직장내괴롭힘', '괴롭힘', 'workplace_bullying') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['workplace_bullying'])
      OR (normalized_category IN ('전보', '인사이동', 'transfer') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['transfer'])
      OR (normalized_category IN ('수습', '시용', 'probation') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['probation'])
      OR (normalized_category IN ('갱신기대권', '계약만료', 'contract_expiry') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['contract_expiry'])
      OR (normalized_category IN ('해고부존재', '사직', 'no_dismissal') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['no_dismissal'])
      OR (normalized_category IN ('근로자성', 'worker_status') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['worker_status'])
      OR (normalized_category IN ('차별', '차별시정', 'discrimination') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['discrimination'])
      OR (normalized_category IN ('경영상해고', '정리해고', 'redundancy') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['redundancy'])
      OR (normalized_category IN ('비위행위', 'misconduct') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['misconduct'])
      OR (normalized_category IN ('폭행', '폭언', 'violence') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['violence'])
      OR (normalized_category IN ('횡령', '배임', 'embezzlement') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['embezzlement'])
      OR (normalized_category IN ('업무능력부족', '저성과', 'incompetence') AND coalesce(d.reason_category, '{}'::text[]) && ARRAY['incompetence'])
      OR (normalized_category IN ('양정', '징계양정', '양정과다', 'disciplinary_severity')
        AND (coalesce(d.holding_summary, '') ILIKE '%양정%' OR coalesce(d.holding_points, '') ILIKE '%양정%' OR coalesce(d.key_issue, '') ILIKE '%양정%'))
    )
    AND (
      -- Text matching: use trigram only when category narrows the pool; otherwise token ILIKE only
      CASE WHEN has_category THEN
        (coalesce(d.title, '') || ' ' || coalesce(d.holding_summary, '') || ' ' || coalesce(d.holding_points, '')) % normalized_query
        OR coalesce(d.title, '') % normalized_query
        OR coalesce(d.holding_summary, '') % normalized_query
        OR coalesce(d.holding_points, '') % normalized_query
        OR EXISTS (SELECT 1 FROM query_tokens AS qt WHERE (coalesce(d.title, '') || ' ' || coalesce(d.holding_summary, '') || ' ' || coalesce(d.holding_points, '')) ILIKE '%' || qt.token || '%')
      ELSE
        -- No category: rely on token ILIKE matching only (fast, no full-table trigram scan)
        EXISTS (
          SELECT 1 FROM query_tokens AS qt
          WHERE (coalesce(d.title, '') || ' ' || coalesce(d.holding_summary, '') || ' ' || coalesce(d.holding_points, '')) ILIKE '%' || qt.token || '%'
        )
      END
    )
    LIMIT 1000
  ),
  scored AS (
    SELECT
      candidate_pool.id,
      candidate_pool.case_number,
      candidate_pool.title,
      candidate_pool.department,
      candidate_pool.decision_date,
      candidate_pool.case_type,
      candidate_pool.decision_result,
      candidate_pool.reason_category,
      candidate_pool.holding_summary,
      candidate_pool.holding_points,
      (
        greatest(
          similarity(candidate_pool.search_text, normalized_query),
          word_similarity(candidate_pool.search_text, normalized_query),
          similarity(coalesce(candidate_pool.title, ''), normalized_query) * 1.15,
          similarity(coalesce(candidate_pool.holding_summary, ''), normalized_query),
          similarity(coalesce(candidate_pool.holding_points, ''), normalized_query)
        )
        + CASE
            WHEN NOT has_category THEN 0
            WHEN normalized_category IN ('부당노동행위', '노동조합', '노조', 'union_activity')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['union_activity'] THEN 0.08
            WHEN normalized_category IN ('무단결근', '결근', 'absence')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['absence'] THEN 0.08
            WHEN normalized_category IN ('성희롱', 'sexual_harassment')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['sexual_harassment'] THEN 0.08
            WHEN normalized_category IN ('직장내괴롭힘', '괴롭힘', 'workplace_bullying')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['workplace_bullying'] THEN 0.08
            WHEN normalized_category IN ('전보', '인사이동', 'transfer')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['transfer'] THEN 0.08
            WHEN normalized_category IN ('수습', '시용', 'probation')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['probation'] THEN 0.08
            WHEN normalized_category IN ('갱신기대권', '계약만료', 'contract_expiry')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['contract_expiry'] THEN 0.08
            WHEN normalized_category IN ('해고부존재', '사직', 'no_dismissal')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['no_dismissal'] THEN 0.08
            WHEN normalized_category IN ('근로자성', 'worker_status')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['worker_status'] THEN 0.08
            WHEN normalized_category IN ('경영상해고', '정리해고', 'redundancy')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['redundancy'] THEN 0.08
            WHEN normalized_category IN ('비위행위', 'misconduct')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['misconduct'] THEN 0.08
            WHEN normalized_category IN ('폭행', '폭언', 'violence')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['violence'] THEN 0.08
            WHEN normalized_category IN ('횡령', '배임', 'embezzlement')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['embezzlement'] THEN 0.08
            WHEN normalized_category IN ('업무능력부족', '저성과', 'incompetence')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['incompetence'] THEN 0.08
            WHEN normalized_category IN ('차별', '차별시정', 'discrimination')
              AND coalesce(candidate_pool.reason_category, '{}'::text[]) && ARRAY['discrimination'] THEN 0.08
            ELSE 0
          END
      )::real AS relevance,
      CASE
        WHEN candidate_pool.decision_result IN ('granted', '전부인정', '인정', 'overturned') THEN 'granted'
        WHEN candidate_pool.decision_result IN ('partial', '일부인정') THEN 'partial'
        WHEN candidate_pool.decision_result IN ('dismissed', 'rejected', 'upheld', '기각', '각하', '초심유지') THEN 'dismissed'
        ELSE NULL
      END AS balance_bucket
    FROM candidate_pool
  ),
  ranked AS (
    SELECT
      scored.*,
      row_number() OVER (
        PARTITION BY scored.balance_bucket
        ORDER BY scored.relevance DESC, scored.decision_date DESC NULLS LAST, scored.id
      ) AS bucket_rank
    FROM scored
    WHERE scored.balance_bucket IS NOT NULL
  )
  SELECT
    ranked.id,
    ranked.case_number,
    ranked.title,
    ranked.department,
    ranked.decision_date,
    ranked.case_type,
    ranked.decision_result,
    ranked.reason_category,
    ranked.holding_summary,
    ranked.holding_points,
    ranked.relevance
  FROM ranked
  WHERE ranked.bucket_rank <= per_bucket_limit
  ORDER BY
    CASE ranked.balance_bucket
      WHEN 'granted' THEN 1
      WHEN 'dismissed' THEN 2
      WHEN 'partial' THEN 3
      ELSE 4
    END,
    ranked.relevance DESC,
    ranked.decision_date DESC NULLS LAST,
    ranked.id;
END;
$$;

GRANT EXECUTE ON FUNCTION public.search_similar_cases(text, text, integer) TO anon;
GRANT EXECUTE ON FUNCTION public.search_similar_cases(text, text, integer) TO authenticated;
GRANT EXECUTE ON FUNCTION public.search_similar_cases(text, text, integer) TO service_role;

COMMENT ON FUNCTION public.search_similar_cases(text, text, integer) IS
  'Trigram similarity RPC for balanced NLRC case retrieval (v3). Uses has_category flag to switch between trigram+ILIKE (with category) and ILIKE-only (without category) for performance. Returns up to limit rows per decision bucket (granted, dismissed, partial).';
