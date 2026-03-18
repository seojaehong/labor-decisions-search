-- AI 징계양정 추천 시스템: tags 컬럼 추가
-- Supabase Dashboard > SQL Editor에서 실행

ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}';
CREATE INDEX IF NOT EXISTS idx_nlrc_tags ON nlrc_decisions USING gin(tags);
