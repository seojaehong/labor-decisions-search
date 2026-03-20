# violence_batch_003 self-review

## 1. batch 개요
- batch: `violence_batch_003`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. representative review notes
- `id_12389`
  - reviewed primary/disposition: dismissal_validity / ['no_formal_disposition']
  - secondary: ['misconduct']
  - exclusion_flags: ['settlement_or_mutual_termination', 'resignation_dispute']
  - 변경 이유: 폭언·협박 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건
- `id_12491`
  - reviewed primary/disposition: workplace_harassment / ['pay_cut']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: 반복성·관계구조상 단순 폭언보다 괴롭힘 구조가 두드러져 workplace_harassment를 선택
- `id_12497`
  - reviewed primary/disposition: workplace_harassment / ['disciplinary_dismissal']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: 반복성·관계구조상 단순 폭언보다 괴롭힘 구조가 두드러져 workplace_harassment를 선택
- `id_12567`
  - reviewed primary/disposition: disciplinary_severity / ['disciplinary_dismissal']
  - secondary: ['misconduct', 'procedure']
  - exclusion_flags: ['not_really_harassment_case', 'evidence_too_thin']
  - 변경 이유: 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지
- `id_1257`
  - reviewed primary/disposition: unfair_treatment / ['suspension']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: violence보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리

## 3. batch-level consistency notes
- violence 배치에서는 폭행·폭언 사실이 있어도 결론이 양정 판단이면 `disciplinary_severity`를 우선 유지했다.
- 반복적·지위이용형 폭언/협박은 `workplace_harassment`를 검토했고, 단발적 다툼·복합 비위는 `misconduct` 또는 `disciplinary_severity`로 정리했다.
- 해고 부존재/합의해지/부당노동행위 결합 사건은 legacy violence 태그를 따라가지 않고 `dismissal_validity` 또는 `unfair_treatment`로 보정했다.
