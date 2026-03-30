-- 고용노동부 행정해석 테이블
-- 법제처 Open API에서 수집한 행정해석을 저장하는 테이블

CREATE TABLE IF NOT EXISTS public.molab_interpretations (
  -- 기본 정보
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
  case_id TEXT NOT NULL UNIQUE,  -- 법령해석 일련번호 (API ID)
  case_number TEXT,  -- 해석 번호 (예: 해석-2024-00123)
  title TEXT,  -- 해석 제목

  -- 조직 정보
  inquiry_org TEXT,  -- 질의 기관 (예: 산업통상자원부, 중소벤처기업부)
  answer_org TEXT DEFAULT '고용노동부',  -- 답변 기관

  -- 내용
  inquiry_summary TEXT,  -- 질의 요지 (최대 1000자)
  answer_summary TEXT,  -- 답변 요약 (최대 2000자)
  full_text TEXT,  -- 회시 전문 (최대 10000자)

  -- 참고 정보
  related_laws TEXT[],  -- 관련 법령 목록 (배열)
  tags TEXT[],  -- 검색 키워드 태그 (배열, 예: ['해고', '임금'])

  -- 메타정보
  decision_date DATE,  -- 해석 결정 날짜 (예: 2024-03-15)
  url TEXT,  -- 원본 API URL
  source TEXT DEFAULT 'molab.api',  -- 데이터 출처

  -- 추적 정보
  collected_at TIMESTAMP WITH TIME ZONE DEFAULT now(),  -- 수집 시간
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),

  -- 제약조건
  CONSTRAINT case_id_not_empty CHECK (case_id != ''),
  CONSTRAINT title_not_empty CHECK (title != '')
);

-- 인덱스 생성 (검색 성능 향상)
CREATE INDEX IF NOT EXISTS idx_molab_interpretations_case_number
  ON public.molab_interpretations(case_number);

CREATE INDEX IF NOT EXISTS idx_molab_interpretations_decision_date
  ON public.molab_interpretations(decision_date DESC);

CREATE INDEX IF NOT EXISTS idx_molab_interpretations_tags
  ON public.molab_interpretations USING GIN(tags);

CREATE INDEX IF NOT EXISTS idx_molab_interpretations_inquiry_org
  ON public.molab_interpretations(inquiry_org);

CREATE INDEX IF NOT EXISTS idx_molab_interpretations_collected_at
  ON public.molab_interpretations(collected_at DESC);

-- 전문 검색용 인덱스 (선택)
CREATE INDEX IF NOT EXISTS idx_molab_interpretations_full_text_tsvector
  ON public.molab_interpretations USING GIN(to_tsvector('korean', COALESCE(full_text, '')));

-- 댓글 관리 정책 설정 (RLS)
ALTER TABLE public.molab_interpretations ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기 가능
CREATE POLICY "allow_select_molab_interpretations"
  ON public.molab_interpretations
  FOR SELECT
  USING (true);

-- 인증된 사용자만 생성 가능
CREATE POLICY "allow_insert_molab_interpretations"
  ON public.molab_interpretations
  FOR INSERT
  WITH CHECK (true);

-- 업데이트는 관리자만 (예시)
CREATE POLICY "allow_update_molab_interpretations"
  ON public.molab_interpretations
  FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- 테이블 설명
COMMENT ON TABLE public.molab_interpretations IS '고용노동부 행정해석 (법제처 Open API)';
COMMENT ON COLUMN public.molab_interpretations.case_id IS '법령해석 일련번호 (고유값, API에서 부여)';
COMMENT ON COLUMN public.molab_interpretations.case_number IS '해석 번호 형식 (예: 해석-2024-00123)';
COMMENT ON COLUMN public.molab_interpretations.inquiry_summary IS '질의 내용 요약';
COMMENT ON COLUMN public.molab_interpretations.answer_summary IS '답변 내용 요약';
COMMENT ON COLUMN public.molab_interpretations.full_text IS '회시 전문 (최대 길이)';
COMMENT ON COLUMN public.molab_interpretations.tags IS '검색 키워드 배열 (예: ARRAY[''해고'', ''임금''])';
COMMENT ON COLUMN public.molab_interpretations.related_laws IS '관련 법령 배열 (예: ARRAY[''근로기준법'', ''노동조합법''])';

-- View: 최신 행정해석 (선택)
CREATE OR REPLACE VIEW molab_latest_interpretations AS
SELECT
  id, case_id, case_number, title,
  inquiry_org, answer_org,
  decision_date, tags,
  collected_at
FROM public.molab_interpretations
WHERE decision_date >= CURRENT_DATE - INTERVAL '180 days'
ORDER BY decision_date DESC, collected_at DESC
LIMIT 500;

COMMENT ON VIEW molab_latest_interpretations IS '최근 6개월 행정해석 (최대 500건)';
