# misconduct_remaining_batch_052 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_052`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_349437`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: []
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_349441`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: ['attendance', 'absence_without_leave', 'misconduct', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_349445`
  - reviewed primary/disposition: misconduct / ['dismissal']
  - secondary: ['attendance', 'procedure', 'worker_status']
  - exclusion_flags: ['evidence_too_thin']
  - 변경 이유: 비위사실 자체는 있으나 핵심은 사용자의 입증 부족 여부 — misconduct + evidentiary focus
- `id_349471`
  - reviewed primary/disposition: disciplinary_severity / ['dismissal']
  - secondary: ['misconduct', 'procedure']
  - exclusion_flags: ['evidence_too_thin']
  - 변경 이유: 비위사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 선택
- `id_349479`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
