# misconduct_remaining_batch_134 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_134`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_56983`
  - reviewed primary/disposition: workplace_harassment / ['dismissal']
  - secondary: ['absence_without_leave', 'misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['not_really_absence_case']
  - 변경 이유: 반복성·지위이용 구조상 단순 비위보다 괴롭힘 성격이 두드러져 workplace_harassment 선택
- `id_56987`
  - reviewed primary/disposition: procedure / ['suspension', 'demotion']
  - secondary: ['misconduct', 'disciplinary_severity', 'unfair_treatment']
  - exclusion_flags: ['procedure_dominant', 'evidence_too_thin', 'unrelated_to_dismissal']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_56997`
  - reviewed primary/disposition: unfair_treatment / ['dismissal']
  - secondary: ['absence_without_leave', 'misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_5703`
  - reviewed primary/disposition: procedure / ['suspension', 'pay_cut']
  - secondary: ['misconduct', 'work_ability', 'disciplinary_severity']
  - exclusion_flags: ['procedure_dominant', 'unrelated_to_dismissal']
  - 변경 이유: 실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례
- `id_57031`
  - reviewed primary/disposition: workplace_harassment / ['dismissal']
  - secondary: ['absence_without_leave', 'misconduct', 'procedure', 'disciplinary_severity', 'transfer_validity']
  - exclusion_flags: ['not_really_absence_case']
  - 변경 이유: 반복성·지위이용 구조상 단순 비위보다 괴롭힘 성격이 두드러져 workplace_harassment 선택

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
