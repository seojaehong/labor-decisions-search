ALTER TABLE cases
  ADD COLUMN IF NOT EXISTS keywords_matched TEXT[] NOT NULL DEFAULT '{}';

ALTER TABLE cases
  ADD COLUMN IF NOT EXISTS verdict_type TEXT NOT NULL DEFAULT '';

CREATE INDEX IF NOT EXISTS idx_cases_keywords_matched
  ON cases USING gin(keywords_matched);
