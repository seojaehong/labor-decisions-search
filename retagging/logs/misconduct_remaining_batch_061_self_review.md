# misconduct_remaining_batch_061 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_061`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_37159`
  - reviewed primary/disposition: unfair_treatment / ['dismissal']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_3717`
  - reviewed primary/disposition: unfair_treatment / ['pay_cut', 'reprimand']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_37207`
  - reviewed primary/disposition: unfair_treatment / ['dismissal']
  - secondary: ['procedure', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_37233`
  - reviewed primary/disposition: unfair_treatment / ['suspension']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_37259`
  - reviewed primary/disposition: dismissal_validity / ['dismissal']
  - secondary: ['misconduct', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: 비위 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
