# misconduct_remaining_batch_053 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_053`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_349997`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_350017`
  - reviewed primary/disposition: procedure / ['reprimand']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant', 'unrelated_to_dismissal']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_350019`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: ['misconduct', 'training_opportunity', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_350039`
  - reviewed primary/disposition: procedure / ['disciplinary_dismissal']
  - secondary: ['attendance', 'misconduct', 'evaluation', 'disciplinary_severity']
  - exclusion_flags: ['resignation_dispute', 'procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_35007`
  - reviewed primary/disposition: unfair_treatment / ['disciplinary_dismissal']
  - secondary: ['misconduct']
  - exclusion_flags: []
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
