# incompetence_batch_004 self-review

## 1. batch 개요
- batch: `incompetence_batch_004`
- reviewed 건수: 30
- 작업 기준:
  - `docs/tagging-schema-v1.json`
  - work_ability vs dismissal_validity 구분 중점
  - 갱신기대권 혼입 시 exclusion_flags 처리
  - 수습 vs 정규직 구분

## 2. primary 분포
- `work_ability`: 10
- `disciplinary_severity`: 3
- `dismissal_validity`: 5
- `renewal_expectation`: 4
- `misconduct`: 2
- `procedure`: 1
- `redundancy`: 1
- `transfer_validity`: 1
- `unfair_treatment`: 1
- `discrimination`: 1
- `other` (구제신청 대상 여부): 1 → dismissal_validity로 처리

## 3. employment_stage 분포
- `regular`: 14
- `probation`: 10
- `renewal_stage`: 4
- `fixed_term`: 2

## 4. disposition_type 분포
- `rejection_of_regular_employment`: 8
- `disciplinary_dismissal`: 5
- `dismissal`: 8
- `nonrenewal`: 4
- `transfer`: 2
- `no_formal_disposition`: 1
- `contract_termination`: 1
- `other`: 1 (차별시정)

## 5. 주요 판단 사례

### work_ability vs dismissal_validity 구분
- **work_ability로 분류** (10건): 수습 본채용 거부(id_33125, id_33735, id_343439, id_343669, id_344265, id_344535, id_34455, id_345837), 정규직 PIP 해고(id_33139), 경력직 업무능력 부족 해고(id_33547)
- **dismissal_validity로 분류** (5건): 시용근로자 여부 자체가 쟁점(id_3321), 수습 규정 미비(id_34477), 해고사유 입증 부족(id_346375), 각하(id_3269), 무기계약 전환 후 해고(id_345179)
- **판단 기준**: 업무능력·성적이 실질 쟁점이면 work_ability, 해고의 존재·성립·요건 자체가 쟁점이면 dismissal_validity

### 갱신기대권 혼입 처리 (4건)
- id_32299: 정규직 전환 기대권 → `renewal_expectation` + `renewal_expectation_dominant`
- id_32415: 무기계약직 전환 기대권 → `renewal_expectation` + `renewal_expectation_dominant`
- id_345371: 갱신기대권 인정 + 갱신거절 합리적 → `renewal_expectation` + `renewal_expectation_dominant`
- id_346187: 갱신기대권 부정 → `renewal_expectation` + `renewal_expectation_dominant`

### 수습 vs 정규직 구분
- **수습(probation)**: id_33125, id_33735, id_343439, id_343669, id_344265, id_344535, id_34455, id_34477, id_345837 — 총 9건 (id_34477은 수습 규정 미비로 실질 정규직이나 수습 stage로 분류)
- **시용 아닌 정규직으로 판단**: id_3321 (훈련근로계약서에 시용 관련 없어 정규직 인정), id_344901 (시용기간 연장 무효로 정규직 전환)

### 특수 사례
- id_3269: 근무성적 불량자 결정 → 각하 사례. `dismissal_validity` / `no_formal_disposition`
- id_32395: CIO 조직 폐지 → `redundancy` (경영상 해고)
- id_34263: 부당노동행위(불이익취급) 승진누락 → `unfair_treatment`
- id_344381: 육아휴직 간접차별 → `discrimination`
- id_344901: 시용기간 연장 합의 무효 → `procedure` (절차 지배적)

## 6. batch 메모
- batch 004는 수습 본채용 거부 사례가 10건(33%)으로 높은 비중. 평가 점수 미달(80점, 60점 등) 패턴이 반복됨.
- incompetence 레거시 태그가 실제로는 갱신기대권·경영상 해고·부당노동행위·차별시정 등 다양한 쟁점에 부착되어 있어 primary 분류 시 원문 재분석이 필수.
- 복수 비위(misconduct + work_ability) 혼재 시, 결론을 좌우한 핵심 쟁점으로 primary를 결정함 (예: id_33547은 업무능력이 핵심이므로 work_ability, id_344363은 비위행위가 핵심이므로 misconduct).
- 시용기간 연장의 취업규칙 위반 효력(id_344901)은 드문 쟁점으로, procedure_dominant 플래그 부여.
