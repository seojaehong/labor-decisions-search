# misconduct_remaining_batch_135 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_135`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_57373`
  - reviewed primary/disposition: workplace_harassment / ['dismissal']
  - secondary: ['attendance', 'misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: 반복성·지위이용 구조상 단순 비위보다 괴롭힘 성격이 두드러져 workplace_harassment 선택
- `id_57377`
  - reviewed primary/disposition: unfair_treatment / ['suspension']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_57415`
  - reviewed primary/disposition: unfair_treatment / ['suspension']
  - secondary: ['misconduct']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리
- `id_57417`
  - reviewed primary/disposition: workplace_harassment / ['dismissal']
  - secondary: ['misconduct', 'evaluation', 'procedure', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: 반복성·지위이용 구조상 단순 비위보다 괴롭힘 성격이 두드러져 workplace_harassment 선택
- `id_5743`
  - reviewed primary/disposition: unfair_treatment / ['disciplinary_dismissal']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: misconduct보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
