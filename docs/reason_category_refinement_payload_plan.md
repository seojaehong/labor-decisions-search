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

#### `probation` 코어 정의

- 시용·수습·본채용 전 평가 단계에서 근로자의 업무 적격성, 조직 적응성, 기본 자질을 이유로 채용 유지 여부를 판단하는 쟁점
- `계약만료/갱신거절`, `정규 재직자 저성과`, `근로자성`과는 분리해서 본다

### 3순위

- `misconduct`
- `violence`
- `embezzlement`

비위행위 내부에서 상호 오염이 있어도, 1~2순위보다 화면 오염도는 낮다.

#### `misconduct` 코어 정의

- 일반적인 복무·규율·지시 위반, 허위보고, 무단행동 등 비위행위의 존재와 징계 정당성을 다투는 쟁점
- `violence`, `embezzlement`, `sexual_harassment`, `workplace_bullying`, `incompetence`를 적극적으로 분리한다

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
6. `probation` 유지 샘플에 `계약만료/갱신거절`이 과다 섞이지 않는지
7. `misconduct` 유지 샘플에 `폭행/횡령/성희롱/괴롭힘/저성과`가 과다 섞이지 않는지

## DB 반영 보류 사유

- 현재 단계는 `payload v2` 품질을 높여 사람이 DB 반영 여부를 결정할 수 있게 만드는 것이 목적이다.
- `worker_status`, `no_dismissal`, `incompetence`는 아직 수기 판단을 바탕으로 2차 규칙 보정이 필요하다.
- `probation`, `misconduct`는 이번 1차 정교화에서 새로 점수화 규칙과 경쟁 카테고리 이관 로직을 도입하므로, 새 산출물 검토 전에는 DB 반영하지 않는다.

## 2026-04-02 Phase 2 v3 결과

- 범위: `probation`, `misconduct`
- 산출물 폴더: `evaluation/reason_category_refinement/20260402_111010/`
- 전체:
  - 대상 `17,742`
  - 유지 `8,843`
  - 제거 후보 `782`
  - 검토 필요 `8,117`
  - DB 반영 `false`

### `probation` v3

- 전체 `3,984`
- 유지 `1,774`
- 제거 후보 `492`
- 검토 필요 `1,718`
- v2 대비: `keep +3 / remove +0 / review -3`

판단:

- `시용/수습 + 본채용 거부` 코어는 유지됐고, browse/list 방어에도 유의미하다.
- 다만 `해고 부존재`, `사직서`, `합의해지`, `일용계약 종료` 계열이 일부 남아 있어 `no_dismissal`과의 경계가 아직 완전히 정리되지는 않았다.
- 따라서 DB 반영 전에는 `사직/합의해지/해고 부존재` 문맥을 더 적극적으로 review 쪽으로 보내는 추가 보정이 필요하다.

### `misconduct` v3

- 전체 `13,758`
- 유지 `7,069`
- 제거 후보 `290`
- 검토 필요 `6,399`
- v2 대비: `keep -34 / remove +0 / review +34`

판단:

- `misconduct`의 블랙홀 성향은 줄었고, `violence`, `embezzlement`, `sexual_harassment`, `workplace_bullying`, `transfer`, `probation` 분리 방향도 맞다.
- 다만 `징계사유`, `양정`, `절차` 같은 일반 문구 때문에 특수 비위가 `keep` 또는 `needs_review`에 남는 경우가 있다.
- `음주운전`은 `subtype=dui` 보조 신호를 유지하되, `당연퇴직`, `면허취소 후 해고`, `통상해고` 같은 후속 처분 문맥은 일반 `misconduct` keep으로 두지 않도록 한 번 더 정리할 필요가 있다.

## 2026-04-02 Phase 2 v4 결과

- 범위: `probation`, `misconduct`
- 산출물 폴더: `evaluation/reason_category_refinement/20260402_122500/`
- 전체:
  - 대상 `17,742`
  - 유지 `8,098`
  - 제거 후보 `986`
  - 검토 필요 `8,658`
  - DB 반영 `false`

### `probation` v4

- 전체 `3,984`
- 유지 `1,466`
- 제거 후보 `708`
- 검토 필요 `1,810`
- v3 대비: `keep -308 / remove +216 / review +92`

판단:

- `사직서`, `합의해지`, `해고 부존재`, `일용계약 종료` 계열이 더 잘 빠져 browse/list 방어 측면은 개선됐다.
- 반면 자동 `keep`이 줄고 `review`가 늘어, DB 정제 자동화 관점에서는 더 보수적인 판정이 되었다.
- 오늘 기준으로는 **precision 우선의 안전한 분리안**으로 볼 수 있다.

### `misconduct` v4

- 전체 `13,758`
- 유지 `6,632`
- 제거 후보 `278`
- 검토 필요 `6,848`
- v3 대비: `keep -437 / remove -12 / review +449`

판단:

- `violence`, `sexual_harassment`, `workplace_bullying`, `transfer`, `probation`과 충돌하는 사례가 `keep`보다 `review`로 더 이동했다.
- 즉 블랙홀 성향은 더 줄었지만, 그만큼 보수적인 review 비율이 올라갔다.
- `dui` subtype은 유지하되, `당연퇴직`, `면허취소 후 해고`, `통상해고` 같은 후속 처분 문맥 분리는 다음 단계 보강 포인트로 남는다.

## 2026-04-02 Phase 2 v5 결과

- 범위: `probation`, `misconduct`
- 산출물 폴더: `evaluation/reason_category_refinement/20260402_224157/`
- 전체:
  - 대상 `17,742`
  - 유지 `8,310`
  - 제거 후보 `1,095`
  - 검토 필요 `8,337`
  - DB 반영 `false`

### v5 공통 변화

- `needs_review`를 `lean_keep`, `lean_remove`, `ambiguous`로 세분화했다.
- negative는 단순 개수 차감이 아니라 `weight + group` 기반으로 평가한다.
- 따라서 `review`가 많더라도, 다음 라운드에서 자동 `keep/remove`로 옮길 우선군이 드러난다.

### `probation` v5

- 전체 `3,984`
- 유지 `1,418`
- 제거 후보 `774`
- 검토 필요 `1,792`
- v4 대비: `keep -48 / remove +66 / review -18`
- review 세부분류:
  - `lean_remove 569`
  - `ambiguous 1,100`
  - `lean_keep 123`

판단:

- `사직서`, `합의해지`, `해고 부존재`, `당연퇴직` 계열은 v4보다 더 안정적으로 `remove/lean_remove`로 이동했다.
- `수습/시용 + 본채용 거부` 코어는 여전히 유지되지만, `수습` 단어만 있고 `본채용 거부`가 없는 케이스는 더 보수적으로 분류된다.
- 다음 보정은 `ambiguous` 1,100건을
  - `본채용 거부 실질 판단`
  - `기간만료/갱신거절`
  - `해고 존재/절차`
  로 더 쪼개는 방향이 맞다.

### `misconduct` v5

- 전체 `13,758`
- 유지 `6,892`
- 제거 후보 `321`
- 검토 필요 `6,545`
- v4 대비: `keep +260 / remove +43 / review -303`
- review 세부분류:
  - `lean_remove 4,376`
  - `ambiguous 1,924`
  - `lean_keep 245`

판단:

- `misconduct` 블랙홀은 한 단계 더 완화됐다.
- `violence`, `embezzlement`, `sexual_harassment`, `workplace_bullying`, `transfer`, `probation` 충돌 사례가 `lean_remove`로 많이 모여, 다음 자동 이관 후보군이 선명해졌다.
- `dui`는 완전 제거하지 않고 `dui`, `dui_termination` 하위유형을 남겨 실무 맥락을 보존했다.
- 다음 보정은 `lean_remove` 대량 묶음을 하위유형별로 더 정리하는 것이다.

## 다음 실행 순서

1. `worker_status_samples.md` 수동 검토
2. 이상 없으면 `worker_status`만 DB 반영
3. browse/list 확인
4. `no_dismissal`
5. `incompetence`
6. 이후 나머지 범주 확장

## v5 이후 권장 순서

1. `probation.ambiguous`를 `contract_expiry / no_dismissal / dismissal_procedure` 축으로 세분화
2. `misconduct.lean_remove`를 `violence / sexual_harassment / workplace_bullying / embezzlement / transfer / probation` 하위군으로 자동 이관
3. `dui`와 `dui_termination`의 browse/list 표시 정책 별도 정리
4. 그 다음에야 DB 반영 검토
