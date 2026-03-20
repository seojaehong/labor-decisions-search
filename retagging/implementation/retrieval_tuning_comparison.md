# Retrieval Tuning Before/After Comparison

## Q8 징계사유는 인정되지만 해고까지는 과하다고 본 사건

- observed before status: `실패`
- after retrieval status: `양호`

### Before Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_24205 | disciplinary_severity | regular | disciplinary_dismissal | 16 | issue_type_primary, legal_focus x2, text overlap x4 |
| 2 | id_1989 | disciplinary_severity | regular | dismissal | 15 | issue_type_primary, legal_focus x2, text overlap x3 |
| 3 | id_11561 | disciplinary_severity | regular | suspension | 14 | issue_type_primary, legal_focus x2, text overlap x2 |
| 4 | id_11595 | disciplinary_severity | regular | disciplinary_dismissal | 14 | issue_type_primary, legal_focus x2, text overlap x2 |
| 5 | id_11735 | disciplinary_severity | regular | dismissal | 14 | issue_type_primary, legal_focus x2, text overlap x2 |

### After Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_25603 | disciplinary_severity | regular | pay_cut, suspension | 50 | primary:disciplinary_severity, secondary:misconduct, disposition:suspension,pay_cut, focus:proportionality,appropriateness_of_discipline, text:2, cross:severity_proportionality |
| 2 | id_11909 | disciplinary_severity | regular | suspension, other, disciplinary_dismissal | 49 | primary:disciplinary_severity, secondary:misconduct, disposition:disciplinary_dismissal,suspension, focus:proportionality,appropriateness_of_discipline, text:1, cross:severity_proportionality |
| 3 | id_12063 | disciplinary_severity | regular | suspension, dismissal | 49 | primary:disciplinary_severity, secondary:misconduct, disposition:dismissal,suspension, focus:proportionality,appropriateness_of_discipline, text:1, cross:severity_proportionality |
| 4 | id_26813 | disciplinary_severity | regular | suspension, pay_cut | 49 | primary:disciplinary_severity, secondary:misconduct, disposition:suspension,pay_cut, focus:proportionality,appropriateness_of_discipline, text:1, cross:severity_proportionality |
| 5 | id_33627 | disciplinary_severity | regular | suspension, dismissal | 49 | primary:disciplinary_severity, secondary:misconduct, disposition:dismissal,suspension, focus:proportionality,appropriateness_of_discipline, text:1, cross:severity_proportionality |

## Q7 정규직 저성과/업무능력 부족 해고

- observed before status: `대체로 양호`
- after retrieval status: `양호`

### Before Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_17059 | work_ability | regular | dismissal | 15 | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |
| 2 | id_22323 | work_ability | regular | pay_cut | 15 | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |
| 3 | id_43869 | work_ability | regular | dismissal | 15 | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |
| 4 | id_46597 | work_ability | regular | dismissal | 15 | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |
| 5 | id_347233 | work_ability | probation | rejection_of_regular_employment | 14 | issue_type_primary, fact_markers x2, text overlap x2 |

### After Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_33547 | work_ability | regular | disciplinary_dismissal | 53 | primary:work_ability, fact:improvement_opportunity_given,training_provided, focus:just_cause,social_norm_reasonableness, stage:regular, text:2, cross:regular_work_ability |
| 2 | id_43869 | work_ability | regular | dismissal | 52 | primary:work_ability, fact:quantitative_evaluation,training_provided, focus:just_cause,social_norm_reasonableness, stage:regular, text:1, cross:regular_work_ability |
| 3 | id_33139 | work_ability | regular | dismissal | 46 | primary:work_ability, fact:improvement_opportunity_given, focus:just_cause,social_norm_reasonableness, stage:regular, cross:regular_work_ability |
| 4 | id_348635 | work_ability | regular | dismissal | 46 | primary:work_ability, fact:warning_given, focus:just_cause,social_norm_reasonableness, stage:regular, cross:regular_work_ability |
| 5 | id_23075 | work_ability | regular | dismissal | 41 | primary:work_ability, fact:improvement_opportunity_given, focus:just_cause,social_norm_reasonableness, stage:regular, keyword_penalty:수습, text:1, cross:regular_work_ability |

## Q2 무단결근 + 절차위반

- observed before status: `실패`
- after retrieval status: `양호`

### Before Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_33381 | dismissal_validity | regular | dismissal | 12 | issue_type_primary, fact_markers x1, text overlap x3 |
| 2 | id_33463 | procedure | fixed_term | dismissal | 12 | issue_type_primary, fact_markers x1, text overlap x3 |
| 3 | id_33393 | dismissal_validity | regular | dismissal | 11 | issue_type_primary, fact_markers x1, text overlap x2 |
| 4 | id_18093 | procedure | regular | dismissal | 11 | issue_type_primary, fact_markers x1, text overlap x2 |
| 5 | id_24749 | procedure | regular | disciplinary_dismissal | 11 | issue_type_primary, fact_markers x1, text overlap x2 |

### After Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_18093 | procedure | regular | dismissal | 45 | primary:procedure, secondary:absence_without_leave, fact:unauthorized_absence,written_notice_missing, focus:procedural_due_process, text:2, cross:absence+procedure |
| 2 | id_24281 | procedure | regular | dismissal | 44 | primary:procedure, secondary:absence_without_leave, fact:unauthorized_absence,written_notice_missing, focus:procedural_due_process, text:1, cross:absence+procedure |
| 3 | id_347181 | procedure | regular | dismissal | 44 | primary:procedure, secondary:absence_without_leave, fact:unauthorized_absence,written_notice_missing, focus:procedural_due_process, text:1, cross:absence+procedure |
| 4 | id_33463 | procedure | fixed_term | dismissal | 41 | primary:procedure, secondary:absence_without_leave, fact:unauthorized_absence, focus:procedural_due_process, text:3, cross:absence+procedure |
| 5 | id_349183 | procedure | regular | disciplinary_dismissal | 40 | primary:procedure, secondary:absence_without_leave, fact:written_notice_missing, focus:procedural_due_process, text:2, cross:absence+procedure |

## Q4 괴롭힘 신고 후 보복성 인사조치

- observed before status: `실패`
- after retrieval status: `양호`

### Before Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_23343 | retaliation | probation | rejection_of_regular_employment | 14 | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |
| 2 | id_43973 | retaliation | regular | dismissal | 14 | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |
| 3 | id_10995 | unfair_treatment | regular | disciplinary_dismissal | 14 | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |
| 4 | id_11565 | unfair_treatment | regular | transfer, other | 14 | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |
| 5 | id_11929 | unfair_treatment | regular | suspension, other | 14 | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |

### After Top-5

| rank | case_id | primary | stage | disposition | score | why |
|------|---------|---------|-------|-------------|-------|-----|
| 1 | id_412537 | retaliation | regular | suspension, transfer | 47 | primary:retaliation, secondary:workplace_harassment, disposition:transfer,suspension, fact:harassment_report_filed, focus:protection_against_retaliation, text:1, cross:retaliation_structure |
| 2 | id_413701 | retaliation | regular | suspension, reprimand | 47 | primary:retaliation, secondary:workplace_harassment, disposition:suspension,reprimand, fact:harassment_report_filed, focus:protection_against_retaliation, text:1, cross:retaliation_structure |
| 3 | id_38125 | retaliation | regular | suspension, dismissal | 46 | primary:retaliation, secondary:workplace_harassment, disposition:dismissal,suspension, fact:harassment_report_filed, focus:protection_against_retaliation, cross:retaliation_structure |
| 4 | id_43547 | retaliation | regular | pay_cut, reprimand | 46 | primary:retaliation, secondary:workplace_harassment,unfair_treatment, disposition:pay_cut,reprimand, focus:protection_against_retaliation, text:1, cross:retaliation_structure |
| 5 | id_43843 | retaliation | regular | suspension, reprimand | 46 | primary:retaliation, secondary:workplace_harassment,unfair_treatment, disposition:suspension,reprimand, focus:protection_against_retaliation, text:1, cross:retaliation_structure |

## Next Priorities

1. `retaliation/unfair_treatment` 질의에서 신고 후 보복 구조를 더 직접 표현하는 fact_markers/keywords 확장
2. `disciplinary_severity` 질의에서 decision_result와 legal_focus 기반 노이즈 감점 추가 보정
3. `regular work_ability` 질의에서 probation 분리와 개선기회 marker coverage 확장
4. `absence + procedure` 질의에서 written_notice_missing 등 procedural markers 보강 여부 점검
