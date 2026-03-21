# misconduct_remaining_batch_038 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_038`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_31699`
  - reviewed primary/disposition: procedure / ['suspension']
  - secondary: []
  - exclusion_flags: ['procedure_dominant', 'unrelated_to_dismissal']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_31715`
  - reviewed primary/disposition: dismissal_validity / ['no_formal_disposition']
  - secondary: ['misconduct', 'procedure']
  - exclusion_flags: ['settlement_or_mutual_termination', 'resignation_dispute']
  - 변경 이유: 비위 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건
- `id_31719`
  - reviewed primary/disposition: procedure / ['disciplinary_dismissal']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_3181`
  - reviewed primary/disposition: unfair_treatment / ['suspension']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_3203`
  - reviewed primary/disposition: procedure / ['suspension']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant', 'unrelated_to_dismissal']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
