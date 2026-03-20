# probation_batch_003 self-review

## 1. batch 개요
- batch: `probation_batch_003`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. primary/secondary가 흔들린 대표 사례
- `id_13103`
  - 수습기간 적용 부당도 보이지만 핵심은 조합원 대상 불이익취급·지배개입이라 `unfair_treatment`를 primary로 보정.
- `id_13359`
  - 수습기간이 등장하더라도 만료 후에는 정식채용 상태로 보아 일반해고 구조로 정리해야 했음.
- `id_13693`
  - 본채용 가능성 판단이 전제되지만 결론은 구두해고와 서면통지 위반이므로 `procedure`가 중심.
- `id_13483`, `id_14033`
  - probation 배치 안의 정규직 전환 기대권/갱신거절 사건으로 `renewal_stage` 전환이 필요했음.

## 3. disposition_type 판단이 애매했던 사례
- `id_13391`, `id_14229`, `id_1441`
  - 시용기간 중 종료이므로 `probation_termination`과 일반 `dismissal`을 구분해 검토.
- `id_13293`, `id_1443`, `id_14433`
  - 시용기간 만료 후의 불채용 구조라 `rejection_of_regular_employment`로 유지.
- `id_1309`
  - 당사자 적격 부재 사건이라 disposition을 `other`로 처리하고 notes로 보완.

## 4. 이번 배치에서 확인한 운영 메모
- worker_status와 unfair_treatment가 함께 걸린 사건은 v1 primary enum 한계가 더 뚜렷하게 드러남.
- 수습기간 만료 전/후의 시점 차이가 disposition과 stage를 크게 바꾼다는 점을 다시 확인.
- probation 배치 안의 갱신기대권 사건은 적극적으로 `renewal_expectation_dominant`를 부여하는 편이 검색 품질에 유리함.
