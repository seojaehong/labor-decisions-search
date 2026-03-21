# misconduct_remaining_batch_142 self-review

## 1. batch 개요
- batch: `misconduct_remaining_batch_142`
- reviewed 건수: 50
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - misconduct vs disciplinary_severity vs procedure 3-way 구분

## 2. representative review notes
- `id_60341`
  - reviewed primary/disposition: workplace_harassment / ['pay_cut']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: 반복성·지위이용 구조상 단순 비위보다 괴롭힘 성격이 두드러져 workplace_harassment 선택
- `id_60347`
  - reviewed primary/disposition: dismissal_validity / ['suspension']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: 비위 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건
- `id_6035`
  - reviewed primary/disposition: dismissal_validity / ['no_formal_disposition']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity', 'unfair_treatment']
  - exclusion_flags: ['resignation_dispute']
  - 변경 이유: 비위 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건
- `id_60359`
  - reviewed primary/disposition: workplace_harassment / ['dismissal']
  - secondary: ['misconduct', 'procedure', 'disciplinary_severity']
  - exclusion_flags: []
  - 변경 이유: 반복성·지위이용 구조상 단순 비위보다 괴롭힘 성격이 두드러져 workplace_harassment 선택
- `id_6037`
  - reviewed primary/disposition: workplace_harassment / ['suspension']
  - secondary: ['misconduct', 'evaluation', 'procedure', 'disciplinary_severity']
  - exclusion_flags: ['unrelated_to_dismissal']
  - 변경 이유: 반복성·지위이용 구조상 단순 비위보다 괴롭힘 성격이 두드러져 workplace_harassment 선택

## 3. batch-level consistency notes
- 비위사실이 인정되더라도 결론이 양정 판단이면 `disciplinary_severity`를 우선으로 선택했다.
- 비위사실 존부/입증이 핵심이면 `misconduct`, 절차 하자가 결론을 좌우하면 `procedure`를 선택했다.
- 해고 부존재/합의해지 사건은 legacy misconduct 태그를 따라가지 않고 `dismissal_validity`로 보정했다.
