# Local App Smoke Check

- 작성시각: 2026-03-20 21:47
- 목적: retagging 품질 외에 실제 검색/AI 체인에서 어디가 병목인지 확인

## 확인 결과

### 1. 홈(`/`)

- 정상 렌더링 확인
- 브라우저 스냅샷 기준 네비게이션과 홈 카드 로딩 정상

### 2. 검색(`/search`)

- 브라우저 `goto`가 timeout으로 걸림
- shell 기준 HTTP 응답도 30초 내 완료되지 않음
- 따라서 단순 프론트 문제라기보다 페이지 진입 시점의 데이터 조회 경로가 지연되는 신호가 강함

### 3. AI 추천(`/api/sanction`)

- POST 응답이 40초 내 완료되지 않음
- 현재 route는
  - keyword 추출
  - Supabase retrieval
  - Anthropic blocking 호출
  순서라, retrieval 또는 모델 호출 둘 중 하나 이상이 병목일 가능성이 큼

## 코드 기준 관찰

### 검색 페이지

- `src/app/search/page.tsx`
- 클라이언트에서 바로 Supabase `nlrc_decisions` 조회
- `textSearch(search_vector, ...)` + `count=exact` + `order(decision_date desc)` 조합 사용
- 이 조합은 인덱스나 row count 상황에 따라 초기 로딩을 크게 늦출 수 있음

### AI retrieval

- `src/lib/ai/retrieval.ts`
- `reason_category` 우선 검색 후 부족하면 `tags` fallback
- rerank는 비활성화되어 있으므로 현재 병목은 임베딩이 아니라 DB retrieval 또는 후속 모델 호출일 가능성이 높음

### AI route

- `src/app/api/sanction/route.ts`
- Anthropic blocking JSON 호출 사용
- retrieval 이후 모델 응답까지 완료되어야 클라이언트가 응답을 받음
- 따라서 retrieval이 느리거나 모델 응답이 느리면 전체 체감속도가 그대로 늘어짐

## 현재 판단

- AI 답변 품질 저하는 retagging만의 문제가 아님
- 실제 서비스 품질은 아래 3개가 동시에 걸려 있음
  1. 태그/분류 품질
  2. Supabase 검색 경로 성능
  3. 모델 호출 응답시간

## 다음 점검 항목

- `/search`에서 `count=exact` 제거 또는 분리 시 체감이 달라지는지
- `textSearch` 없는 reason-only query는 빠른지
- `/api/sanction`에서 retrieval만 별도 측정했을 때 지연이 큰지
- Claude 신규 배치가 추가된 뒤 검색 precision이 실제로 개선되는지

## Diagnostic Snapshot (2026-03-20 22:07)

### Local endpoint timings
- `/`: error / 15091ms / error=`timed out`
- `/search`: error / 15015ms / error=`timed out`
- `/sanction`: error / 15017ms / error=`timed out`
- `/api/sanction`: error / 15018ms / error=`timed out`

### Direct Supabase REST timing
- `supabase reason_category absence`: 200 / 1431ms / size=1018

### Diagnosis
- 홈이 빠르고 `/search`, `/sanction`, `/api/sanction`이 상대적으로 느리면 초기 데이터 조회 또는 blocking 모델 호출이 병목일 가능성이 높다.
- direct Supabase REST가 빠른데 `/search`와 `/api/sanction`이 느리면 Next route/client query 조합이나 모델 호출이 우세 병목이다.
- direct Supabase REST도 느리면 DB 인덱스, `count=exact`, 정렬, text search 조건 조합을 먼저 의심한다.

### Fix proposals
- `/search`: `count=exact`를 초기 렌더에서 분리하고, free-text가 비어 있을 때 `textSearch`를 붙이지 않도록 조정
- `/search`: reason-only 조회는 더 가벼운 first page query와 별도 total count query로 분리
- `/api/sanction`: retrieval 시간과 모델 호출 시간을 별도 로깅해서 병목을 분리
- `/api/sanction`: retrieval 결과를 먼저 응답 가능한 구조로 바꾸거나, 모델 timeout 시 partial fallback을 반환
- retrieval: retagged field를 reason-only 검색 필터와 exclusion-aware filter에 더 직접 반영할 후보를 재정리

## Diagnostic Snapshot (2026-03-20 22:07)

### Local endpoint timings
- `/`: error / 8060ms / error=`timed out`
- `/search`: error / 8023ms / error=`timed out`
- `/sanction`: error / 8025ms / error=`timed out`
- `/api/sanction`: error / 8027ms / error=`timed out`

### Direct Supabase REST timing
- `supabase reason_category absence`: 200 / 407ms / size=1018

### Diagnosis
- 홈이 빠르고 `/search`, `/sanction`, `/api/sanction`이 상대적으로 느리면 초기 데이터 조회 또는 blocking 모델 호출이 병목일 가능성이 높다.
- direct Supabase REST가 빠른데 `/search`와 `/api/sanction`이 느리면 Next route/client query 조합이나 모델 호출이 우세 병목이다.
- direct Supabase REST도 느리면 DB 인덱스, `count=exact`, 정렬, text search 조건 조합을 먼저 의심한다.

### Fix proposals
- `/search`: `count=exact`를 초기 렌더에서 분리하고, free-text가 비어 있을 때 `textSearch`를 붙이지 않도록 조정
- `/search`: reason-only 조회는 더 가벼운 first page query와 별도 total count query로 분리
- `/api/sanction`: retrieval 시간과 모델 호출 시간을 별도 로깅해서 병목을 분리
- `/api/sanction`: retrieval 결과를 먼저 응답 가능한 구조로 바꾸거나, 모델 timeout 시 partial fallback을 반환
- retrieval: retagged field를 reason-only 검색 필터와 exclusion-aware filter에 더 직접 반영할 후보를 재정리
