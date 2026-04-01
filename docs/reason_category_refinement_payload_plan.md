# reason_category 정교화 payload v2 실행 계획

## 목적

`reason_category` 과태깅과 browse/list 오염을 줄이기 위해, 각 범주를
`domain_gate + positive_signals + negative_signals` 구조로 재평가한
`payload v2`를 만들었다.

이번 산출물은 **실제 DB 업데이트 전 검토용 자료**이며, 바로 반영하지 않는다.

## payload v2 공통 필드

- `current_reason_category`
- `proposed_reason_category`
- `outcome`: `keep`, `remove`, `needs_review`
- `removal_basis`: `label_mismatch`, `non_labor_domain`, `guard_miss`, `needs_review`
- `domain_bucket`: `labor_case`, `non_labor_case`, `needs_review`
- `review_priority`: `high`, `medium`, `low`
- `positive_hits`
- `negative_hits`
- `domain_hits`
- `evidence_snippet`

## 전체 결과

- 전체 대상: `75,815`
- 유지: `46,806`
- 제거 후보: `20,892`
- 검토 필요: `8,117`
- 인정(구제) 전/후: `17,181 -> 10,287`

## 우선 검토 순서

### 1순위

- `worker_status`
  - 전체 `12,196`
  - 제거 후보 `8,152`
  - 검토 필요 `675`
- `no_dismissal`
  - 전체 `14,230`
  - 제거 후보 `6,358`
  - 검토 필요 `1,771`
- `incompetence`
  - 전체 `2,239`
  - 제거 후보 `1,142`
  - 검토 필요 `200`

이 3개는 browse/list 오염과 카테고리 혼선이 가장 크다.

### 2순위

- `probation`
- `contract_expiry`
- `transfer`

이 묶음은 서로 경계가 흐려서, 1순위 이후 묶어서 검토하는 것이 효율적이다.

### 3순위

- `misconduct`
- `violence`
- `embezzlement`

비위행위 내부에서 상호 오염이 있어도, 1~2순위보다 화면 오염도는 낮다.

### 4순위

- `workplace_bullying`
- `sexual_harassment`

하위 intent 분리까지 같이 봐야 해서 뒤로 둔다.

### 5순위

- `union_activity`
- `discrimination`
- `redundancy`

현재 precision이 상대적으로 높아 마지막 정리 대상으로 둔다.

## 산출물 위치

- 전체 요약:
  - `evaluation/reason_category_refinement/20260401_*/report.json`
  - `evaluation/reason_category_refinement/20260401_*/summary.md`
- 범주별 상세:
  - `evaluation/reason_category_refinement/20260401_*/<reason>_detail_v2.json`
  - `evaluation/reason_category_refinement/20260401_*/<reason>_updates_v2.jsonl`
  - `evaluation/reason_category_refinement/20260401_*/<reason>_samples.md`

## 반영 전 체크포인트

1. `remove` 샘플에 실제 정탐이 많이 섞여 있지 않은지
2. `needs_review`가 과도하게 큰 범주는 규칙이 아직 흔들리는지
3. `non_labor_domain`이 잡힌 케이스가 실제 비노동 문서인지
4. `no_dismissal` 유지 샘플에 `부당해고 인정` 문구가 섞이는지
5. `worker_status`에서 도급/파견 문맥이 근로자성 판단 문맥과 함께 있을 때 유지되는지

## 다음 실행 순서

1. `worker_status_samples.md` 수동 검토
2. 이상 없으면 `worker_status`만 DB 반영
3. browse/list 확인
4. `no_dismissal`
5. `incompetence`
6. 이후 나머지 범주 확장
