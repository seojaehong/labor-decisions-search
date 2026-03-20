-- candidate 8축 태그 첫 적재용 staging table
-- merged_final_v1.jsonl 기준의 병행 트랙 테이블

CREATE TABLE IF NOT EXISTS nlrc_decision_tag_candidates (
  case_id TEXT PRIMARY KEY,
  source_decision_id TEXT NOT NULL,
  summary_short TEXT,
  holding_summary TEXT,
  retrieval_note TEXT,
  employment_stage TEXT,
  issue_type_primary TEXT,
  issue_type_secondary TEXT[] DEFAULT '{}',
  disposition_type TEXT[] DEFAULT '{}',
  fact_markers TEXT[] DEFAULT '{}',
  legal_focus TEXT[] DEFAULT '{}',
  industry_context TEXT,
  exclusion_flags TEXT[] DEFAULT '{}',
  include_for_queries TEXT[] DEFAULT '{}',
  exclude_for_queries TEXT[] DEFAULT '{}',
  tag_confidence TEXT,
  retag_notes TEXT,
  retag_version TEXT,
  review_status TEXT,
  retag_source_basis TEXT,
  retag_snapshot_version TEXT,
  retag_loaded_at TIMESTAMPTZ,
  retag_payload JSONB,
  promoted_to_live BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_primary ON nlrc_decision_tag_candidates(issue_type_primary);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_stage ON nlrc_decision_tag_candidates(employment_stage);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_secondary ON nlrc_decision_tag_candidates USING gin(issue_type_secondary);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_disposition ON nlrc_decision_tag_candidates USING gin(disposition_type);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_fact_markers ON nlrc_decision_tag_candidates USING gin(fact_markers);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_legal_focus ON nlrc_decision_tag_candidates USING gin(legal_focus);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_exclusion_flags ON nlrc_decision_tag_candidates USING gin(exclusion_flags);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_snapshot_version ON nlrc_decision_tag_candidates(retag_snapshot_version);
CREATE INDEX IF NOT EXISTS idx_nlrc_candidate_promoted ON nlrc_decision_tag_candidates(promoted_to_live);
