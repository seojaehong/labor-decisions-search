# Retrieval Tuning v1

## 적용 원칙

- baseline/search UI는 건드리지 않는다.
- candidate 경로에서 query-aware reranking을 강화한다.
- primary 단일 일치보다 stage/disposition/fact/legal/result 교차를 더 크게 본다.

## Q8 징계사유는 인정되지만 해고까지는 과하다고 본 사건

- scenario: `severity_excessive`
- primary pool: `disciplinary_severity, misconduct`
- preferred disposition: `dismissal, disciplinary_dismissal, suspension, pay_cut`
- preferred legal focus: `proportionality, appropriateness_of_discipline`
- boosted decision_result: `granted, partial, overturned`
- excluded decision_result: `dismissed, settled`
- penalized keywords: `구제이익, 채용내정, 상시근로자 수, 복직명령, 계약기간 만료`

## Q7 정규직 저성과/업무능력 부족 해고

- scenario: `regular_work_ability`
- primary pool: `work_ability, dismissal_validity`
- preferred stage: `regular`
- penalized stage: `probation`
- preferred disposition: `dismissal, disciplinary_dismissal`
- preferred fact markers: `qualitative_evaluation, quantitative_evaluation, warning_given, improvement_opportunity_given, training_provided`
- preferred legal focus: `just_cause, social_norm_reasonableness`
- penalized keywords: `수습, 본채용, 시용`

## Q2 무단결근 + 절차위반

- scenario: `absence_procedure`
- primary pool: `procedure, dismissal_validity, absence_without_leave`
- preferred fact markers: `unauthorized_absence, written_notice_missing`
- preferred legal focus: `procedural_due_process`
- excluded decision_result: `dismissed, settled`
- penalized keywords: `구제이익, 복직명령, 상시근로자 수, 채용내정`

## Q4 괴롭힘 신고 후 보복성 인사조치

- scenario: `retaliation`
- primary pool: `retaliation, unfair_treatment, workplace_harassment`
- preferred disposition: `dismissal, disciplinary_dismissal, transfer, suspension, pay_cut, reprimand`
- preferred fact markers: `harassment_report_filed`
- preferred legal focus: `protection_against_retaliation`
- penalized keywords: `2차 가해, 성희롱, 쟁의행위, 노동조합, 조합원`

