# Search Architecture v2

## 목적

`merged_final_v1.jsonl`를 기준본으로 삼아 `baseline 유지 + candidate 병행 + compare 검증`이 가능한 검색 구조를 안정화한다.

이 문서는 구현자와 검증자가 바로 따라갈 수 있도록 현재안의 계약, 질의 파서 출력, candidate 파이프라인, local model 삽입점, 최소 acceptance 기준만 정리한다.

## 현재안 요약

- `baseline`
  - 기존 `reason_category + search_vector` 경로를 유지한다.
  - 회귀 기준선으로만 사용한다.
- `candidate`
  - 8축 태그 기반 검색을 사용한다.
  - 질의 구조화 결과를 바탕으로 recall과 precision을 분리한다.
- `compare`
  - 같은 질의를 baseline/candidate에 각각 실행한다.
  - top 결과를 나란히 보여준다.

원칙:

- baseline은 건드리지 않는다.
- candidate만 query-aware 정책을 강화한다.
- compare는 검증용으로 유지한다.

## Payload Contract

`/api/search`는 아래 형태를 안정적으로 반환한다.

```ts
type SearchResponsePayload = {
  mode: 'baseline' | 'candidate' | 'compare';
  query: string;
  reason: string;
  result: string;
  baseline?: SearchBucket;
  candidate?: SearchBucket;
  baselineError?: string;
  candidateError?: string;
};
```

`SearchBucket`:

```ts
type SearchBucket = {
  items: SearchCard[];
  total: number;
  page: number;
  pageSize: number;
};
```

`SearchCard` 최소 필드:

- `id`
- `case_number`
- `title`
- `department`
- `decision_date`
- `decision_result`
- `key_issue`
- `holding_summary`
- `holding_points`
- `url`
- `reason_category`

주의:

- 프론트는 payload shape drift를 방어해야 한다.
- candidate가 비어도 baseline은 계속 렌더링되어야 한다.
- 내부 디버그 값은 production UI에 노출하지 않는다.

## Query Parser Output

candidate 검색은 먼저 질의를 구조화한다.

```ts
type ParsedCandidateQuery = {
  raw_query: string;
  normalized_query: string;
  keywords: string[];
  intended_primary: string[];
  intended_stage: string[];
  intended_disposition: string[];
  must_have_markers: string[];
  penalized_markers: string[];
  query_scenario: 'generic' | 'absence_procedure' | 'regular_work_ability' | 'retaliation' | 'severity_excessive';
  explanation: string;
};
```

현재 parser는 다음 시나리오를 분기한다.

- `absence_procedure`
  - 무단결근 + 절차위반
- `regular_work_ability`
  - 정규직 + 저성과/업무능력 부족
- `retaliation`
  - 괴롭힘 신고 후 보복
- `severity_excessive`
  - 징계사유 인정 + 해고 과다

출력의 용도:

- `normalized_query`
  - 검색용 핵심 질의
- `intended_primary`
  - candidate 우선 primary 후보
- `intended_stage`
  - probation/regular 같은 stage 후보
- `intended_disposition`
  - dismissal / suspension / nonrenewal 같은 disposition 후보
- `must_have_markers`
  - 시나리오에서 꼭 필요한 사실 마커
- `penalized_markers`
  - 잘못 섞이면 안 되는 마커

## Candidate Pipeline

candidate는 아래 5단계로 고정한다.

1. `query normalization`
2. `tag extraction`
3. `candidate recall`
4. `precision rerank`
5. `hydration`

### 1. Query normalization

- 자연어 질의를 검색용 토큰으로 줄인다.
- query parser 결과를 candidate 정책의 입력으로 사용한다.

### 2. Tag extraction

- query parser가 scenario와 intent tag를 만든다.
- 여기서 `primary/stage/disposition/must_have/penalty`가 나온다.

### 3. Candidate recall

- 8축 태그, reason fallback, exclusion filter로 넓게 후보를 회수한다.
- 이 단계는 recall을 우선한다.
- 결과를 너무 일찍 좁히지 않는다.

### 4. Precision rerank

- query scenario에 맞는 점수를 다시 계산한다.
- 핵심은:
  - primary/stage/disposition 일치
  - legal focus / fact marker 일치
  - exclusion / penalty
  - scenario bonus
- Q4/Q7/Q2/Q8 잔여 노이즈는 이 단계에서 줄인다.

### 5. Hydration

- 최종 후보 ID를 실제 카드 데이터로 다시 채운다.
- 이 단계에서는 `case_number`, `department`, `decision_date`, `holding_summary`를 포함해 UI가 바로 렌더링할 수 있어야 한다.

## Local Model Adapter Insertion Point

local model은 검색 보조 전용으로만 먼저 붙인다.

우선 삽입점:

- `query normalization`
- `query-to-tag parsing`
- `top-N rerank justification`
- `compare/debug용 why surfaced 보조`

권장 인터페이스:

- OpenAI 호환 chat/completions 스타일의 내부 adapter
- 실패 시 규칙형 parser/rerank로 fallback

금지:

- 최종 AI 답변 본문 생성
- 급여 계산
- 신고 생성
- 산식 판단

권장 원칙:

- local model이 죽어도 search는 살아 있어야 한다.
- local model은 candidate 품질을 올리는 보조 레이어여야 한다.

## Implementation Order

1. `/api/search` 응답 타입 고정
2. search service에서 baseline/candidate/compare 분리
3. query parser 결과를 candidate에 연결
4. recall/precision score 정식화
5. local model adapter 추가
6. 라이브 13질의 검증

## Acceptance Checklist

- `/search?mode=baseline|candidate|compare`가 안정적으로 렌더링된다.
- `/api/search` payload shape가 baseline/candidate/compare에서 흔들리지 않는다.
- candidate가 0건이어도 baseline이 같이 죽지 않는다.
- Q2/Q4/Q7/Q8이 baseline보다 candidate에서 더 잘 맞는다.
- 상세 페이지는 `holding_points` 본문형 렌더링을 유지한다.
- search 카드에서는 내부 디버그 정보가 노출되지 않는다.
- local model이 없어도 규칙형 v2가 동작한다.

