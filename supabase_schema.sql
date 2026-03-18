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
