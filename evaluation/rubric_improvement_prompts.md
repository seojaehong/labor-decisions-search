# 판례검색 루브릭 77→99 개선 프롬프트

현재 점수: 185/240 = 77.1% (하이쿠 평가 + 오퍼스 검수)
목표: 237/240 = 99%
Supabase project_id: mewqgevgdgghhatqtuos

---

## Phase 1: RPC 메타데이터 필터 강화 (예상 +12점)

```
판례검색 RPC search_similar_cases를 개선해주세요.

■ 배경
- Supabase project: mewqgevgdgghhatqtuos
- 현재 RPC v3: /home/ubuntu/work-orchestrator/repos/labor-decisions-search/supabase/migrations/20260330_add_search_similar_cases_rpc.sql
- nlrc_decisions 테이블에 sanction_type 컬럼 있음 (dismissal, suspension, pay_cut, warning, demotion 등)
- reason_category 컬럼은 text[] 배열 (영문 코드: absence, violence, misconduct 등)
- 현재 점수: 185/240 = 77.1%

■ 해결할 약점 쿼리 4개

1) Q14 (5/10) "감봉 처분이 과한지 본 사건" category=''
   - 문제: category 비어있어서 sanction_type='pay_cut' 필터링 안 됨
   - 해결: 쿼리 텍스트에 '감봉'이 포함되면 sanction_type='pay_cut'인 결과에 relevance +0.15 부스트
   - 마찬가지로 '정직' → sanction_type='suspension' +0.12 부스트

2) Q24 (4/10) "여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건" category=''
   - 문제: 복합비위 케이스를 찾지 못함
   - 해결: reason_category 배열 길이 >= 3인 결과에 relevance +0.1 부스트
   - holding_summary에 '징계사유' AND ('양정' OR '과하' OR '정당') 동시 포함 시 +0.08 추가

3) Q03 (6/10) "택시나 버스 기사 무단결근 징계해고" category='absence'
   - 문제: 산업(운수) 특정성 반영 안 됨
   - 해결: 쿼리에 '택시|버스|기사|운전|운수' 키워드가 있고, title이나 holding_summary에도 해당 키워드 있으면 relevance +0.12 부스트

4) Q11 (4/10) "개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건" category='incompetence'
   - 문제: "개선기회 부여" 맥락 매칭 안 됨
   - 해결: holding_summary에 '개선|시정|경고|교육|기회|주고도|부여' 키워드 포함 시 relevance +0.1 부스트

■ 구현 방법
scored CTE의 relevance 계산에 위 부스트 로직을 추가하세요. 기존 category 부스트(0.08) 아래에 텍스트 기반 부스트를 추가합니다.

■ 작업 순서
1. 현재 배포된 RPC 확인: SELECT pg_get_functiondef(oid) FROM pg_proc WHERE proname = 'search_similar_cases';
2. scored CTE에 부스트 로직 추가
3. execute_sql로 Supabase에 직접 배포
4. 마이그레이션 파일 동기화: 20260330_add_search_similar_cases_rpc.sql
5. 검증 쿼리 4개 실행:
   - SELECT id, title, holding_summary, relevance FROM search_similar_cases('감봉 처분이 과한지 본 사건', '', 5);
   - SELECT id, title, holding_summary, reason_category, relevance FROM search_similar_cases('여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건', '', 5);
   - SELECT id, title, holding_summary, relevance FROM search_similar_cases('택시나 버스 기사 무단결근 징계해고', 'absence', 5);
   - SELECT id, title, holding_summary, relevance FROM search_similar_cases('개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건', 'incompetence', 5);
```

---

## Phase 2: 하이브리드 검색 RPC (예상 +25점)

```
판례검색에 벡터 코사인 유사도를 결합한 하이브리드 검색 RPC를 만들어주세요.

■ 배경
- Supabase project: mewqgevgdgghhatqtuos
- nlrc_decisions 테이블에 embedding 컬럼 있음 (vector 타입, 99.2% 커버리지)
- 현재 search_similar_cases는 trigram(pg_trgm)만 사용 → 텍스트 유사도만 봄
- 의미(semantic) 유사도를 추가하면 뉘앙스 쿼리(Q23 "괴롭힘 미인정", Q11 "개선기회 부여 후") 성능이 크게 향상됨

■ 아키텍처

search_similar_cases_hybrid(
  query text,
  query_embedding vector,     -- 호출 측에서 OpenAI API로 생성해서 전달
  category text DEFAULT NULL,
  "limit" integer DEFAULT 5,
  trigram_weight real DEFAULT 0.4,
  semantic_weight real DEFAULT 0.6
)

스코어링:
  final_relevance = (trigram_weight * trigram_score) + (semantic_weight * semantic_score) + category_boost + metadata_boost

trigram_score: 기존 greatest(similarity(...), word_similarity(...), ...) 방식 유지
semantic_score: 1 - (embedding <=> query_embedding)  -- cosine distance를 similarity로 변환
category_boost: 기존 0.08 부스트 유지
metadata_boost: Phase 1에서 추가한 sanction_type/keyword 부스트

■ 구현 상세

1. pgvector 확장 확인: CREATE EXTENSION IF NOT EXISTS vector;
2. 임베딩 인덱스 확인/생성:
   CREATE INDEX IF NOT EXISTS idx_nlrc_decisions_embedding ON nlrc_decisions USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
3. RPC 함수 생성 (기존 search_similar_cases 구조 기반)
4. candidate_pool에서:
   - has_category=true: 카테고리 필터 + trigram OR ILIKE + 벡터 유사도 상위 200건
   - has_category=false: 벡터 유사도 상위 500건 (trigram 생략, 타임아웃 방지)
5. scored CTE에서 trigram_score + semantic_score 가중 합산

■ 호출 측 수정 (retrieval.ts)

파일: /home/ubuntu/work-orchestrator/repos/labor-decisions-search/src/lib/ai/retrieval.ts

searchCases() 함수에서:
1. 쿼리 텍스트를 OpenAI text-embedding-3-small로 임베딩 생성
2. supabase.rpc('search_similar_cases_hybrid', { query, query_embedding, category, limit }) 호출
3. 기존 search_similar_cases는 폴백으로 유지

OpenAI API 키: process.env.OPENAI_API_KEY (이미 .env에 있음)
임베딩 모델: text-embedding-3-small (1536 dimensions)
임베딩 차원 확인: SELECT vector_dims(embedding) FROM nlrc_decisions WHERE embedding IS NOT NULL LIMIT 1;

■ 검증
Phase 1과 동일한 4개 쿼리 + 추가:
- SELECT id, title, holding_summary, relevance FROM search_similar_cases_hybrid('근로자성이 실제 핵심 쟁점인 사건', <embedding>, 'worker_status', 5);
- SELECT id, title, holding_summary, relevance FROM search_similar_cases_hybrid('괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건', <embedding>, 'workplace_bullying', 5);
- Q23 결과에 "괴롭힘 불인정" "괴롭힘 미해당" 관련 사례가 상위에 오는지 확인

■ 주의사항
- 임베딩 차원을 먼저 확인하고 query_embedding 타입을 맞출 것
- ivfflat 인덱스 lists 수는 sqrt(총건수) ≈ 238이지만, 100으로 시작해도 충분
- LIMIT 1000은 유지 (candidate_pool 크기 제한)
```

---

## Phase 3: AI 쿼리 리라이팅 (예상 +10점)

```
사용자 자연어 쿼리를 검색에 최적화된 형태로 리라이팅하는 기능을 추가해주세요.

■ 배경
- 파일: /home/ubuntu/work-orchestrator/repos/labor-decisions-search/src/lib/ai/retrieval.ts
- 현재 searchCases() 함수는 사용자 쿼리를 그대로 RPC에 전달
- "괴롭힘 미인정" 같은 부정 표현, "개선기회 부여 후" 같은 조건부 표현은 trigram이 잘 못 잡음
- AI가 쿼리를 확장/변환하면 정밀도가 올라감

■ 구현

searchCases() 함수 시작 부분에 쿼리 리라이팅 단계를 추가:

async function rewriteQueryForSearch(query: string): Promise<{
  expandedQuery: string;      // RPC에 전달할 확장된 쿼리
  suggestedCategory: string;  // 감지된 카테고리 (비어있을 수 있음)
  keywords: string[];         // 핵심 검색 키워드
}> {
  // Claude API (claude-haiku-4-5) 호출
  // 시스템 프롬프트:
  // "당신은 한국 노동위원회 판정례 검색 시스템의 쿼리 최적화 엔진입니다.
  //  사용자의 자연어 쿼리를 받아서:
  //  1. expandedQuery: 핵심 법률 용어와 동의어를 포함한 확장 쿼리 (최대 50자)
  //  2. suggestedCategory: 아래 17개 중 해당하는 것 (없으면 빈 문자열)
  //     absence, sexual_harassment, workplace_bullying, transfer, probation,
  //     contract_expiry, no_dismissal, worker_status, discrimination,
  //     redundancy, misconduct, violence, embezzlement, incompetence,
  //     dismissal, discipline, disciplinary_severity
  //  3. keywords: holding_summary에서 찾아야 할 핵심 키워드 3-5개
  //
  //  예시:
  //  입력: '괴롭힘은 인정되지 않지만 그 신고 때문에 갈등이 커진 사건'
  //  출력: {
  //    expandedQuery: '직장내괴롭힘 불인정 미해당 신고 갈등 전보 불이익',
  //    suggestedCategory: 'workplace_bullying',
  //    keywords: ['괴롭힘 불인정', '괴롭힘 미해당', '신고 후', '갈등', '전보']
  //  }
  //
  //  입력: '개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건'
  //  출력: {
  //    expandedQuery: '업무능력 부족 개선 기회 경고 시정 교육 후 해고',
  //    suggestedCategory: 'incompetence',
  //    keywords: ['개선 기회', '경고', '시정', '업무능력 부족', '해고']
  //  }
  //
  //  입력: '택시나 버스 기사 무단결근 징계해고'
  //  출력: {
  //    expandedQuery: '택시 버스 운수 기사 운전 무단결근 징계해고',
  //    suggestedCategory: 'absence',
  //    keywords: ['택시', '버스', '기사', '무단결근', '징계해고']
  //  }"
}

■ 호출 흐름

searchCases(userQuery) {
  1. rewriteQueryForSearch(userQuery) → { expandedQuery, suggestedCategory, keywords }
  2. 쿼리 임베딩 생성 (Phase 2): embed(expandedQuery)
  3. RPC 호출: search_similar_cases_hybrid(expandedQuery, embedding, suggestedCategory, limit)
  4. keywords로 결과 재랭킹: holding_summary에 keywords 많이 포함된 결과 부스트
  5. 기존 scoreTaggedCandidate() + rankTaggedCandidates() 적용
}

■ 재랭킹 로직

keywords 매칭 부스트:
- 5개 중 4-5개 매칭: +0.1
- 5개 중 2-3개 매칭: +0.05
- 5개 중 0-1개 매칭: 0

■ 비용/성능
- Haiku 호출: ~0.001$/쿼리, 지연 ~500ms
- 임베딩 생성: ~0.0001$/쿼리, 지연 ~200ms
- 총 추가 지연: ~700ms (사용자 체감 허용 범위)

■ 검증
24개 쿼리 전체 재실행하여 최종 점수 측정.
하이쿠 서브에이전트로 독립 평가 실행.
이전 평가 파일 참조: /home/ubuntu/work-orchestrator/repos/labor-decisions-search/evaluation/rubric_haiku_eval_20260330.md

■ 주의사항
- Claude API 키: process.env.ANTHROPIC_API_KEY
- 모델: claude-haiku-4-5-20251001 (비용 절감)
- 타임아웃: 3초 (실패 시 원본 쿼리 그대로 사용)
- 캐시: 동일 쿼리는 Map<string, Result>로 세션 내 캐시
```

---

## 실행 순서

1. **Phase 1 먼저** — SQL만 수정, 30분 내 완료 가능
2. **Phase 2** — 벡터 검색 추가, 핵심 개선 (1-2시간)
3. **Phase 3** — AI 리라이팅, 마무리 정밀도 (1시간)
4. **최종 평가** — 하이쿠 24쿼리 재평가 실행
