# reason_category browse/list 가드 확장 메모

최신 전수 진단:
- 산출물: `evaluation/reason_category_guard_audit/20260401_*.json`
- 목적: `검색어 없음 + 사유 필터` browse/list에서 태그 과다 부착으로 인한 오염을 줄이기

## 현재 판단

가드 적용 우선순위는 아래 순서가 적절하다.

1. `worker_status`
- 전체 `12,196`
- 가드 통과 `3,690`
- 제거 후보 `8,506`
- `인정(구제)` 전/후 `2,487 -> 629`
- 가장 오염이 크고, 실제 사용자 체감 문제도 이미 확인됨

2. `no_dismissal`
- 전체 `14,230`
- 가드 통과 `6,444`
- 제거 후보 `7,786`
- `인정(구제)` 전/후 `2,754 -> 727`
- `사직`, `권고사직`, `해고부존재`와 일반 부당해고 사건이 혼재할 가능성이 높음

3. `incompetence`
- 전체 `2,239`
- 가드 통과 `429`
- 제거 후보 `1,810`
- `인정(구제)` 전/후 `524 -> 112`
- `저성과/업무능력 부족`과 일반 징계 또는 수습 사건 혼선 가능성이 큼

4. `absence`
- 전체 `5,397`
- 가드 통과 `2,949`
- 제거 후보 `2,448`
- `인정(구제)` 전/후 `1,453 -> 674`

5. `probation`, `contract_expiry`, `redundancy`
- 중간 수준 정제 효과
- browse/list 오염을 줄일 여지는 있으나, 앞선 범주보다 급하지 않음

## 보수적으로 유지해도 되는 범주

아래 범주는 현재 가드 통과율이 높아, DB 정제보다 browse/list 유지가 우선이다.

- `union_activity` `0.9823`
- `sexual_harassment` `0.9761`
- `misconduct` `0.9497`
- `embezzlement` `0.9319`
- `violence` `0.9192`
- `discrimination` `0.8702`
- `transfer` `0.8220`
- `contract_expiry` `0.7933`
- `workplace_bullying` `0.7540`

## 실행 순서

1. `worker_status` 규칙 2차 보정 후 DB 반영
2. `no_dismissal`, `incompetence` 동일 방식으로 시범 정제
3. `absence`, `probation`, `contract_expiry` 확장
4. 고정밀 범주는 browse/list 가드만 유지하고 DB 재태깅은 후순위
