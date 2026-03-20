# Search Connection Points

## 목표

baseline(`reason_category`)와 candidate(8축 태그)를 같은 코드베이스에서 병행 비교 가능한 구조로 만든다.

## 현재 연결 지점

### 1. 브라우저 검색 UI

파일:

- `src/app/search/page.tsx`

현재:

- `reason_category`
- `decision_result`
- `search_vector`

중심 검색만 지원한다.

필요 변경:

- 검색 모드 선택 추가
  - `baseline`
  - `candidate`
  - `compare`

추천 방식:

- URL param
  - `mode=baseline|candidate|compare`

## 2. AI retrieval

파일:

- `src/lib/ai/retrieval.ts`

현재:

- Stage 1A:
  - `issue_type_primary` 기반 candidate 검색
- Stage 1B:
  - `reason_category` fallback
- Stage 1C:
  - `tags` fallback

문제:

- baseline/candidate 결과가 하나의 함수 안에서 섞인다
- compare 모드에서 같은 query의 두 결과를 나란히 보기 어렵다

권장 리팩터링:

- `searchCasesBaseline(query, tags)`
- `searchCasesCandidate(query, tags)`
- `searchCasesCompare(query, tags)`

## 3. 상세 페이지 디버깅

파일:

- `src/app/decisions/[id]/page.tsx`

추가 권장:

- baseline reason badge
- candidate primary/stage/disposition badge
- exclusion/debug block

이유:

- 회귀 디버깅 시 case 단위 비교가 쉬워진다

## compare 모드 제안

### API 응답 형태

```json
{
  "query": "수습기간 중 본채용 거부가 정당한지",
  "baseline": {
    "mode": "reason_category",
    "cases": []
  },
  "candidate": {
    "mode": "tag_8axis",
    "cases": []
  }
}
```

### 추천 구현 위치

- 신규 route:
  - `src/app/api/search-compare/route.ts`

또는

- 기존 search route/service에서 `mode=compare` 분기

## before/after 실험 경로

### baseline

- 기존 UI 그대로
- 조건:
  - `reason_category`
  - `search_vector`

### candidate

- 신규 8축 태그 검색
- 조건 예:
  - `issue_type_primary`
  - `employment_stage`
  - `disposition_type`
  - `fact_markers`
  - `legal_focus`
  - `industry_context`
  - `exclusion_flags`

### compare

- 동일 query를 baseline과 candidate에 각각 실행
- top-5를 나란히 노출
- 오프라인 평가 질의셋 24개를 그대로 재사용 가능

## 안전한 출시 순서

1. baseline 유지
2. candidate 경로를 feature flag 뒤에 추가
3. compare 모드로 내부 QA
4. 평가 통과 시 candidate를 실험 노출
5. 최종 전환 여부 결정

## 최소 구현 초안

### 타입

- `SearchMode = 'baseline' | 'candidate' | 'compare'`

### 함수 분리

- baseline:
  - `reason_category` 기반 조회
- candidate:
  - `issue_type_primary` 중심 + exclusion 필터
- compare:
  - 두 결과를 모두 반환

### 로그

query 로그에는 아래를 남기는 것이 좋다.

- `mode`
- `query`
- `baseline_top_ids`
- `candidate_top_ids`
- `retag_snapshot_version`

이렇게 해야 실제 서비스에서 평가 패키지와 같은 비교가 가능해진다.
