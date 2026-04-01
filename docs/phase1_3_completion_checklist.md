# Hybrid Search Phase 1-3 Completion Checklist

작성일: 2026-04-01

## 목적

판례검색 품질 개선 작업의 `Phase 1 ~ Phase 3`가 현재 코드와 RPC 기준으로 어느 수준까지 반영되어 있는지 고정된 체크리스트로 남긴다.

## Phase 1. RPC 메타데이터 필터 강화

상태: 완료

확인 파일:

- `supabase/migrations/20260330_add_search_similar_cases_rpc.sql`

반영 항목:

- `감봉` 쿼리에서 `sanction_type='pay_cut'` 부스트
- `정직` 쿼리에서 `sanction_type='suspension'` 부스트
- 복합비위 케이스 (`reason_category` 다중 매칭) 부스트
- `징계사유` + `양정/과하/정당` 맥락 부스트
- `택시/버스/기사/운전/운수` 산업 맥락 부스트
- `개선/시정/경고/교육/기회` 맥락 부스트

추가 확인 포인트:

- 서버 배포본과 migration SQL이 동일한지 주기적으로 재확인 필요

## Phase 2. 하이브리드 검색 RPC

상태: 완료

확인 파일:

- `supabase/migrations/20260331_search_similar_cases_hybrid_rpc.sql`

반영 항목:

- `pgvector` 확장 사용
- `ivfflat` 인덱스 사용
- `search_similar_cases_hybrid(...)` 함수 정의
- `trigram_score + semantic_score + category_boost + metadata_boost`
- vector 후보와 trigram 후보를 분리한 뒤 merge

운영 메모:

- 성능 개선 이후 direct REST 평가 가능 상태로 확인
- 여전히 최적화 여지는 있으나, 평가/서비스 적용 가능한 수준

## Phase 3. AI 쿼리 리라이팅 + 호출 측 통합

상태: 완료

확인 파일:

- `src/lib/search/ai-query-rewriter.ts`
- `src/lib/ai/retrieval.ts`

반영 항목:

- AI query rewriting
- category 추론
- intent 추론
- OpenAI embedding 생성
- hybrid RPC 우선 호출
- legacy RPC fallback
- AI reranking

추가 반영:

- intent-aware query expansion
  - `괴롭힘 불인정`
  - `신고 후 보복/불이익`
  - `사실상 해고`
  - `양정과다`
  - `개선 기회`

## 현재 평가 기준 산출물

대표 최신 산출물:

- `evaluation/search_quality_99/20260331_163224/report.json`
- `evaluation/search_quality_99/20260331_163224/summary.md`

요약:

- baseline: `165`
- upgraded: `188`
- delta: `+23`

## 남은 과제

우선순위 높은 남은 항목:

1. `Q10` 저성과/업무능력 부족 케이스에서 probation/transfer 혼입 억제
2. `Q16` 계약기간 만료 + 사실상 해고 계열에서 `갱신기대권 인정` 및 `부당해고 다툼` 맥락 강화
3. 약한 쿼리 debug artifact를 기준으로 시나리오별 retrieval 분기 정교화

## 결론

Phase 1~3은 신규 구현 단계가 아니라, 현재는 **검증 + 시나리오별 미세조정 단계**로 보는 것이 맞다.
