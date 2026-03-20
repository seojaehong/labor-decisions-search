-- 다축 태깅 스키마 추가 (기존 reason_category 유지, 병행)
-- Supabase SQL Editor에서 실행

-- 핵심 검색 축 (개별 컬럼 — 인덱싱 + 필터링 가능)
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS employment_stage TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS issue_type_primary TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS issue_type_secondary TEXT[] DEFAULT '{}';
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS disposition_type TEXT[] DEFAULT '{}';
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS fact_markers TEXT[] DEFAULT '{}';
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS legal_focus TEXT[] DEFAULT '{}';
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS industry_context TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS exclusion_flags TEXT[] DEFAULT '{}';

-- 태깅 메타
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS tag_confidence TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS summary_short TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retrieval_note TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retag_version TEXT;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS review_status TEXT DEFAULT 'pending';
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retagged_at TIMESTAMPTZ;
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;

-- 전체 태깅 원본 (LLM 출력 JSON 보존)
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS retag_payload JSONB;

-- 검색용 인덱스
CREATE INDEX IF NOT EXISTS idx_nlrc_issue_primary ON nlrc_decisions(issue_type_primary);
CREATE INDEX IF NOT EXISTS idx_nlrc_employment_stage ON nlrc_decisions(employment_stage);
CREATE INDEX IF NOT EXISTS idx_nlrc_issue_secondary ON nlrc_decisions USING gin(issue_type_secondary);
CREATE INDEX IF NOT EXISTS idx_nlrc_disposition ON nlrc_decisions USING gin(disposition_type);
CREATE INDEX IF NOT EXISTS idx_nlrc_fact_markers ON nlrc_decisions USING gin(fact_markers);
CREATE INDEX IF NOT EXISTS idx_nlrc_exclusion ON nlrc_decisions USING gin(exclusion_flags);
CREATE INDEX IF NOT EXISTS idx_nlrc_retag_version ON nlrc_decisions(retag_version);

-- RLS 유지 (기존 public read 정책 그대로)
