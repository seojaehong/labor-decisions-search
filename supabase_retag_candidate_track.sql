-- merged_final_v1.jsonl 기준의 candidate 8축 태그 병행 경로용 보강 스키마
-- 기존 baseline(reason_category) 유지
-- 기존 supabase_retag_schema.sql 위에 추가 적용 가능

ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS include_for_queries TEXT[] DEFAULT '{}';
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS exclude_for_queries TEXT[] DEFAULT '{}';
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retag_notes TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retag_source_basis TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retag_snapshot_version TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retag_loaded_at TIMESTAMPTZ;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS tag_search_enabled BOOLEAN DEFAULT false;

CREATE INDEX IF NOT EXISTS idx_nlrc_include_for_queries ON nlrc_decisions USING gin(include_for_queries);
CREATE INDEX IF NOT EXISTS idx_nlrc_exclude_for_queries ON nlrc_decisions USING gin(exclude_for_queries);
CREATE INDEX IF NOT EXISTS idx_nlrc_retag_snapshot_version ON nlrc_decisions(retag_snapshot_version);
CREATE INDEX IF NOT EXISTS idx_nlrc_tag_search_enabled ON nlrc_decisions(tag_search_enabled);

CREATE OR REPLACE VIEW nlrc_decisions_candidate_v1 AS
SELECT
  id,
  title,
  decision_result,
  url,
  reason_category,
  employment_stage,
  issue_type_primary,
  issue_type_secondary,
  disposition_type,
  fact_markers,
  legal_focus,
  industry_context,
  exclusion_flags,
  include_for_queries,
  exclude_for_queries,
  summary_short,
  retrieval_note,
  tag_confidence,
  retag_notes,
  retag_version,
  review_status,
  retag_snapshot_version,
  retag_loaded_at
FROM nlrc_decisions
WHERE retag_snapshot_version = 'merged_final_v1'
  AND tag_search_enabled = true;
