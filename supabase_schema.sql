-- 노동위 판정례 테이블 (기존 yellow-envelope Supabase에 추가)
-- Supabase Dashboard > SQL Editor에서 실행

CREATE TABLE IF NOT EXISTS nlrc_decisions (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  case_number TEXT,
  department TEXT,
  decision_date DATE,
  case_type TEXT DEFAULT '부당해고',

  -- 구조화 필드
  reason_category TEXT[] NOT NULL DEFAULT '{}',
  reason_detail TEXT,
  procedure_committee BOOLEAN DEFAULT false,
  procedure_defense BOOLEAN DEFAULT false,
  procedure_written_notice BOOLEAN DEFAULT false,
  procedure_advance_notice BOOLEAN DEFAULT false,
  procedure_note TEXT,
  sanction_type TEXT DEFAULT 'dismissal',
  decision_result TEXT NOT NULL DEFAULT 'other',
  key_issue TEXT,

  -- 원본
  holding_points TEXT,
  holding_summary TEXT,
  url TEXT,

  -- 메타
  source TEXT DEFAULT 'law.go.kr',
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- 전문검색
  search_vector tsvector GENERATED ALWAYS AS (
    to_tsvector('simple',
      coalesce(title,'') || ' ' ||
      coalesce(holding_points,'') || ' ' ||
      coalesce(holding_summary,'') || ' ' ||
      coalesce(reason_detail,'') || ' ' ||
      coalesce(key_issue,'')
    )
  ) STORED
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_nlrc_reason ON nlrc_decisions USING gin(reason_category);
CREATE INDEX IF NOT EXISTS idx_nlrc_result ON nlrc_decisions(decision_result);
CREATE INDEX IF NOT EXISTS idx_nlrc_sanction ON nlrc_decisions(sanction_type);
CREATE INDEX IF NOT EXISTS idx_nlrc_date ON nlrc_decisions(decision_date);
CREATE INDEX IF NOT EXISTS idx_nlrc_search ON nlrc_decisions USING gin(search_vector);

-- 통계 뷰
CREATE OR REPLACE VIEW reason_stats AS
SELECT
  unnest(reason_category) as reason_category,
  decision_result,
  COUNT(*) as count
FROM nlrc_decisions
GROUP BY 1, 2
ORDER BY 1, count DESC;

-- RLS (Row Level Security) - 읽기 전용 공개
ALTER TABLE nlrc_decisions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read access" ON nlrc_decisions
  FOR SELECT USING (true);

-- BigCase/외부 판례 원문 레이어
-- 검색/태깅은 nlrc_decisions를 유지하고, 상세 소비용 원문은 별도 테이블에 저장
CREATE TABLE IF NOT EXISTS decision_source_documents (
  id BIGSERIAL PRIMARY KEY,
  internal_decision_id TEXT NOT NULL REFERENCES nlrc_decisions(id) ON DELETE CASCADE,

  source_provider TEXT NOT NULL,
  source_case_id TEXT,
  source_url TEXT,

  full_text_raw JSONB,
  full_text_clean TEXT,
  body_sections JSONB,
  summary_raw TEXT,

  coverage_ratio NUMERIC(5, 2),
  completeness_flag TEXT DEFAULT 'failed',
  parse_version TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  extracted_at TIMESTAMPTZ DEFAULT NOW(),
  last_verified_at TIMESTAMPTZ,
  parse_error TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_decision_source_documents_internal_parse_version
  ON decision_source_documents(internal_decision_id, parse_version);

CREATE INDEX IF NOT EXISTS idx_decision_source_documents_internal_decision_id
  ON decision_source_documents(internal_decision_id);

CREATE INDEX IF NOT EXISTS idx_decision_source_documents_parse_version
  ON decision_source_documents(parse_version);

CREATE INDEX IF NOT EXISTS idx_decision_source_documents_content_hash
  ON decision_source_documents(content_hash);

ALTER TABLE decision_source_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read source docs" ON decision_source_documents
  FOR SELECT USING (true);

-- law.go.kr 판례 별도축
-- 기존 nlrc_decisions와 분리하여 법제처 판례를 별도 저장
CREATE TABLE IF NOT EXISTS lawgo_precedents (
  id TEXT PRIMARY KEY,
  api_id TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  reference_number TEXT,
  decision_date TEXT,
  court TEXT,
  court_type_code TEXT,
  case_type_name TEXT,
  case_type_code TEXT,
  judgment_type TEXT,
  issue_text TEXT,
  summary_text TEXT,
  reference_statutes TEXT,
  reference_cases TEXT,
  source_url TEXT,
  source_provider TEXT NOT NULL DEFAULT 'lawgo',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_lawgo_precedents_court
  ON lawgo_precedents(court);

CREATE INDEX IF NOT EXISTS idx_lawgo_precedents_decision_date
  ON lawgo_precedents(decision_date);

ALTER TABLE lawgo_precedents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read lawgo precedents" ON lawgo_precedents
  FOR SELECT USING (true);

CREATE TABLE IF NOT EXISTS lawgo_precedent_documents (
  id BIGSERIAL PRIMARY KEY,
  precedent_id TEXT NOT NULL REFERENCES lawgo_precedents(id) ON DELETE CASCADE,
  body_text TEXT NOT NULL,
  body_sections JSONB,
  body_length INTEGER NOT NULL DEFAULT 0,
  parse_version TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  collected_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_lawgo_precedent_documents_precedent_parse
  ON lawgo_precedent_documents(precedent_id, parse_version);

CREATE INDEX IF NOT EXISTS idx_lawgo_precedent_documents_precedent_id
  ON lawgo_precedent_documents(precedent_id);

ALTER TABLE lawgo_precedent_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read lawgo precedent documents" ON lawgo_precedent_documents
  FOR SELECT USING (true);
