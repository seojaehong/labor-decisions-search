# misconduct_remaining_batch_108 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_108`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_46303`
  - reviewed primary/disposition: procedure / ['disciplinary_dismissal']
  - secondary: ['misconduct']
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_46379`
  - reviewed primary/disposition: procedure / ['dismissal']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_46393`
  - reviewed primary/disposition: unfair_treatment / ['suspension']
  - secondary: ['misconduct', 'evaluation', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_46421`
  - reviewed primary/disposition: procedure / ['suspension']
  - secondary: ['absence_without_leave', 'misconduct', 'disciplinary_severity']
  - exclusion_flags: ['not_really_absence_case', 'procedure_dominant', 'evidence_too_thin', 'unrelated_to_dismissal']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_46427`
  - reviewed primary/disposition: disciplinary_severity / ['dismissal']
  - secondary: ['misconduct', 'procedure']
  - exclusion_flags: []
  - 변경 이유: 비위사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 선택

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
