# violence_batch_004 self-review

## 1. batch 개요
- batch: `violence_batch_004`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. representative review notes
- `id_13359`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: ['misconduct']
  - exclusion_flags: ['not_really_harassment_case', 'unrelated_to_probation', 'procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_13415`
  - reviewed primary/disposition: dismissal_validity / ['rejection_of_regular_employment']
  - secondary: ['misconduct', 'evaluation']
  - exclusion_flags: []
  - 변경 이유: 폭언·협박 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건
- `id_13975`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['not_really_harassment_case', 'procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_14317`
  - reviewed primary/disposition: procedure / ['disciplinary_dismissal']
  - secondary: ['misconduct']
  - exclusion_flags: ['not_really_harassment_case', 'procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_1441`
  - reviewed primary/disposition: dismissal_validity / ['probation_termination']
  - secondary: ['misconduct', 'procedure']
  - exclusion_flags: []
  - 변경 이유: 폭언·협박 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건

## 3. batch-level consistency notes
- violence 배치에서는 폭행·폭언 사실이 있어도 결론이 양정 판단이면 `disciplinary_severity`를 우선 유지했다.
- 반복적·지위이용형 폭언/협박은 `workplace_harassment`를 검토했고, 단발적 다툼·복합 비위는 `misconduct` 또는 `disciplinary_severity`로 정리했다.
- 해고 부존재/합의해지/부당노동행위 결합 사건은 legacy violence 태그를 따라가지 않고 `dismissal_validity` 또는 `unfair_treatment`로 보정했다.
