ALTER TABLE lawgo_precedents
  ADD COLUMN IF NOT EXISTS keywords_matched TEXT[] NOT NULL DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS estimated_year INTEGER,
  ADD COLUMN IF NOT EXISTS bigcase_case_id TEXT;

CREATE INDEX IF NOT EXISTS idx_lawgo_precedents_keywords_matched
  ON lawgo_precedents USING GIN (keywords_matched);

CREATE INDEX IF NOT EXISTS idx_lawgo_precedents_estimated_year
  ON lawgo_precedents (estimated_year);

CREATE INDEX IF NOT EXISTS idx_lawgo_precedents_bigcase_case_id
  ON lawgo_precedents (bigcase_case_id);
