# violence_batch_005 self-review

## 1. batch 개요
- batch: `violence_batch_005`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. representative review notes
- `id_14835`
  - reviewed primary/disposition: disciplinary_severity / ['dismissal']
  - secondary: ['misconduct']
  - exclusion_flags: ['not_really_harassment_case']
  - 변경 이유: 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지
- `id_14863`
  - reviewed primary/disposition: disciplinary_severity / ['disciplinary_dismissal']
  - secondary: ['misconduct', 'training_opportunity']
  - exclusion_flags: ['not_really_harassment_case']
  - 변경 이유: 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지
- `id_1487`
  - reviewed primary/disposition: disciplinary_severity / ['suspension']
  - secondary: ['misconduct', 'procedure']
  - exclusion_flags: ['not_really_harassment_case', 'unrelated_to_dismissal']
  - 변경 이유: 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지
- `id_14901`
  - reviewed primary/disposition: disciplinary_severity / ['dismissal']
  - secondary: ['misconduct']
  - exclusion_flags: []
  - 변경 이유: 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지
- `id_14913`
  - reviewed primary/disposition: disciplinary_severity / ['dismissal']
  - secondary: ['misconduct', 'procedure', 'unfair_treatment']
  - exclusion_flags: ['not_really_harassment_case']
  - 변경 이유: 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지

## 3. batch-level consistency notes
- violence 배치에서는 폭행·폭언 사실이 있어도 결론이 양정 판단이면 `disciplinary_severity`를 우선 유지했다.
- 반복적·지위이용형 폭언/협박은 `workplace_harassment`를 검토했고, 단발적 다툼·복합 비위는 `misconduct` 또는 `disciplinary_severity`로 정리했다.
- 해고 부존재/합의해지/부당노동행위 결합 사건은 legacy violence 태그를 따라가지 않고 `dismissal_validity` 또는 `unfair_treatment`로 보정했다.
