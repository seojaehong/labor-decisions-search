# 24-Query Blind Side-by-Side Package

## Q01 — 반복 무단결근으로 해고된 사건

- topic: `absence`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10561 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 2 | id_10563 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 3 | id_10757 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 4 | id_10815 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 5 | id_10845 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_27267 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | dismissal | issue_type_primary, disposition_type x1, fact_markers x2, text overlap x2 |  |  |
| 2 | id_16387 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, disposition_type x1, fact_markers x2, text overlap x1 |  |  |
| 3 | id_17735 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, disposition_type x1, fact_markers x2, text overlap x1 |  |  |
| 4 | id_1807 | ○ ○ ○ 부당해고 구제 재심신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, disposition_type x1, fact_markers x2, text overlap x1 |  |  |
| 5 | id_19315 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | dismissal | issue_type_primary, disposition_type x1, fact_markers x2, text overlap x1 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q02 — 무단결근이 언급되지만 실제 핵심은 절차 위반인 사건

- topic: `absence`
- query_type: `composite`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10561 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 2 | id_10563 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 3 | id_10757 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 4 | id_10815 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 5 | id_10845 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_33381 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | issue_type_primary, fact_markers x1, text overlap x3 |  |  |
| 2 | id_33463 | ○ ○ ○ 부당해고 구제신청 | procedure | fixed_term | dismissal | issue_type_primary, fact_markers x1, text overlap x3 |  |  |
| 3 | id_33393 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | issue_type_primary, fact_markers x1, text overlap x2 |  |  |
| 4 | id_18093 | ○ ○ ○ 부당해고 구제신청 | procedure | regular | dismissal | issue_type_primary, fact_markers x1, text overlap x2 |  |  |
| 5 | id_24749 | ○ ○ ○ 부당해고 구제신청 | procedure | regular | disciplinary_dismissal | issue_type_primary, fact_markers x1, text overlap x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q03 — 택시나 버스 기사 무단결근 징계해고

- topic: `absence`
- query_type: `natural_language`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_23381 | ○ ○ ○ 부당해고 구제 재심신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, fact_markers x1, industry_context, text overlap x4 |  |  |
| 2 | id_17201 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, fact_markers x1, industry_context, text overlap x3 |  |  |
| 3 | id_20949 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, fact_markers x1, industry_context, text overlap x3 |  |  |
| 4 | id_21651 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, fact_markers x1, industry_context, text overlap x3 |  |  |
| 5 | id_21797 | ○ ○ ○ 부당해고 구제신청 | absence_without_leave | regular | disciplinary_dismissal | issue_type_primary, fact_markers x1, industry_context, text overlap x3 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10561 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 2 | id_10563 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 3 | id_10757 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 4 | id_10815 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 5 | id_10845 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q04 — 직장내괴롭힘이 실제로 성립하는지 다툰 사건

- topic: `workplace_bullying`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_406201 | ○ ○ ○ 부당해고 구제신청 | workplace_harassment | regular | reprimand | issue_type_primary, legal_focus x2, text overlap x1 |  |  |
| 2 | id_255 | ○ ○ ○ 부당해고 구제신청 | workplace_harassment | regular | pay_cut, suspension, transfer | issue_type_primary, legal_focus x2 |  |  |
| 3 | id_349227 | ○ ○ ○ 부당해고 구제 재심신청 | workplace_harassment | regular | disciplinary_dismissal, transfer | issue_type_primary, legal_focus x2 |  |  |
| 4 | id_349905 | ○ ○ ○ 부당해고 구제신청 | workplace_harassment | regular | pay_cut | issue_type_primary, legal_focus x2 |  |  |
| 5 | id_40297 | ○ ○ ○ 부당해고 구제신청 | workplace_harassment | regular | disciplinary_dismissal | issue_type_primary, legal_focus x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10771 | ○ ○ ○ 부당해고 구제신청 | workplace_harassment | regular | suspension | baseline_export |  |  |
| 2 | id_10819 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal | baseline_export |  |  |
| 3 | id_10861 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | suspension | baseline_export |  |  |
| 4 | id_10901 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 5 | id_10913 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension, disciplinary_dismissal | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q05 — 직장내괴롭힘 신고 후 불이익이나 보복이 문제 된 사건

- topic: `workplace_bullying`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_23343 | ○ ○ ○ 부당해고 구제 재심신청 | retaliation | probation | rejection_of_regular_employment | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 2 | id_43973 | ○ ○ ○ 부당해고 구제신청 | retaliation | regular | dismissal | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 3 | id_10995 | ○ ○ ○ 부당해고 구제신청 | unfair_treatment | regular | disciplinary_dismissal | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 4 | id_11565 | ○ ○ ○ 부당해고 구제신청 | unfair_treatment | regular | transfer, other | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 5 | id_11929 | ○ ○ ○ 부당해고 구제신청 | unfair_treatment | regular | suspension, other | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 | id_10607 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 3 | id_10727 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 4 | id_10771 | ○ ○ ○ 부당해고 구제신청 | workplace_harassment | regular | suspension | baseline_export |  |  |
| 5 | id_10819 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q06 — 괴롭힘은 인정되는데 징계 수위가 과한지 보는 사건

- topic: `workplace_bullying`
- query_type: `composite`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_344935 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | suspension | issue_type_primary, issue_type_secondary x1, legal_focus x2, text overlap x3 |  |  |
| 2 | id_345943 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension | issue_type_primary, issue_type_secondary x1, legal_focus x2, text overlap x3 |  |  |
| 3 | id_346173 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension | issue_type_primary, issue_type_secondary x1, legal_focus x2, text overlap x3 |  |  |
| 4 | id_407587 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | dismissal | issue_type_primary, issue_type_secondary x1, legal_focus x2, text overlap x3 |  |  |
| 5 | id_29185 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | pay_cut | issue_type_primary, issue_type_secondary x1, legal_focus x2, text overlap x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 3 | id_10607 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 4 | id_10613 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 5 | id_10677 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | dismissal | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q07 — 수습기간 중 본채용 거부가 정당한지

- topic: `probation`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_19817 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x1, text overlap x3 |  |  |
| 2 | id_25883 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x1, text overlap x3 |  |  |
| 3 | id_27827 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x1, text overlap x3 |  |  |
| 4 | id_29597 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x1, text overlap x3 |  |  |
| 5 | id_34299 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x1, text overlap x3 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10575 | ○ ○ ○ 부당해고 구제신청 | work_ability | probation | rejection_of_regular_employment | baseline_export |  |  |
| 2 | id_10597 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | baseline_export |  |  |
| 3 | id_10603 | ○ ○ ○ 부당해고 구제 재심신청 | procedure | probation | rejection_of_regular_employment | baseline_export |  |  |
| 4 | id_10621 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | contract_termination | baseline_export |  |  |
| 5 | id_10633 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q08 — 수습기간 중 업무능력 부족으로 해고하거나 본채용 거부한 사건

- topic: `probation`
- query_type: `composite`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_23631 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | probation_termination, rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x2, text overlap x2 |  |  |
| 2 | id_348399 | ○ ○ ○ 부당해고 구제 재심신청 | work_ability | probation | probation_termination, rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x2, text overlap x2 |  |  |
| 3 | id_40327 | ○ ○ ○ 부당해고 구제 재심신청 | work_ability | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x1, text overlap x5 |  |  |
| 4 | id_19769 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | probation_termination | employment_stage, issue_type_primary, disposition_type x1, text overlap x4 |  |  |
| 5 | id_34299 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, disposition_type x1, text overlap x4 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10575 | ○ ○ ○ 부당해고 구제신청 | work_ability | probation | rejection_of_regular_employment | baseline_export |  |  |
| 2 | id_10597 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | baseline_export |  |  |
| 3 | id_10603 | ○ ○ ○ 부당해고 구제 재심신청 | procedure | probation | rejection_of_regular_employment | baseline_export |  |  |
| 4 | id_10621 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | contract_termination | baseline_export |  |  |
| 5 | id_10633 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q09 — 수습인데 서면통지나 절차 문제가 있는 사건

- topic: `probation`
- query_type: `composite`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10575 | ○ ○ ○ 부당해고 구제신청 | work_ability | probation | rejection_of_regular_employment | baseline_export |  |  |
| 2 | id_10597 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | baseline_export |  |  |
| 3 | id_10603 | ○ ○ ○ 부당해고 구제 재심신청 | procedure | probation | rejection_of_regular_employment | baseline_export |  |  |
| 4 | id_10621 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | contract_termination | baseline_export |  |  |
| 5 | id_10633 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | baseline_export |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_1373 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 2 | id_14245 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 3 | id_14829 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | dismissal | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 4 | id_17893 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | dismissal | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |
| 5 | id_18945 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | rejection_of_regular_employment | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q10 — 정규직 저성과나 업무능력 부족으로 해고된 사건

- topic: `incompetence`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_13295 | ○ ○ ○ 부당해고 구제신청 | procedure | regular | transfer | baseline_export |  |  |
| 2 | id_13323 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | baseline_export |  |  |
| 3 | id_14007 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal | baseline_export |  |  |
| 4 | id_14077 | ○ ○ ○ 부당해고 구제 재심신청 | work_ability | regular | dismissal | baseline_export |  |  |
| 5 | id_14241 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | disciplinary_dismissal | baseline_export |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_17059 | ○ ○ ○ 부당해고 구제신청 | work_ability | regular | dismissal | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |  |  |
| 2 | id_22323 | ○ ○ ○ 부당노동행위 구제신청 | work_ability | regular | pay_cut | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |  |  |
| 3 | id_43869 | ○ ○ ○ 부당해고 구제 재심신청 | work_ability | regular | dismissal | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |  |  |
| 4 | id_46597 | ○ ○ ○ 부당해고 구제신청 | work_ability | regular | dismissal | employment_stage, issue_type_primary, fact_markers x1, text overlap x1 |  |  |
| 5 | id_347233 | ○ ○ ○ 부당해고 구제신청 | work_ability | probation | rejection_of_regular_employment | issue_type_primary, fact_markers x2, text overlap x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q11 — 개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건

- topic: `incompetence`
- query_type: `composite`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_348399 | ○ ○ ○ 부당해고 구제 재심신청 | work_ability | probation | probation_termination, rejection_of_regular_employment | issue_type_primary, fact_markers x3, text overlap x1 |  |  |
| 2 | id_51313 | ○ ○ ○ 부당해고 구제신청 | work_ability | probation | rejection_of_regular_employment | issue_type_primary, fact_markers x3, text overlap x1 |  |  |
| 3 | id_22799 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | issue_type_primary, fact_markers x3 |  |  |
| 4 | id_33547 | ○ ○ ○ 부당해고 구제신청 | work_ability | regular | disciplinary_dismissal | issue_type_primary, fact_markers x2, text overlap x2 |  |  |
| 5 | id_40327 | ○ ○ ○ 부당해고 구제 재심신청 | work_ability | probation | rejection_of_regular_employment | issue_type_primary, fact_markers x1, text overlap x4 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_13295 | ○ ○ ○ 부당해고 구제신청 | procedure | regular | transfer | baseline_export |  |  |
| 2 | id_13323 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | baseline_export |  |  |
| 3 | id_14007 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal | baseline_export |  |  |
| 4 | id_14077 | ○ ○ ○ 부당해고 구제 재심신청 | work_ability | regular | dismissal | baseline_export |  |  |
| 5 | id_14241 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | disciplinary_dismissal | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q12 — 징계사유는 인정되지만 해고가 너무 과하다고 본 사건

- topic: `disciplinary_severity`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_24205 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, legal_focus x2, text overlap x4 |  |  |
| 2 | id_1989 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | dismissal | issue_type_primary, legal_focus x2, text overlap x3 |  |  |
| 3 | id_11561 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension | issue_type_primary, legal_focus x2, text overlap x2 |  |  |
| 4 | id_11595 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, legal_focus x2, text overlap x2 |  |  |
| 5 | id_11735 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | dismissal | issue_type_primary, legal_focus x2, text overlap x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q13 — 정직 처분 양정이 적정한지 본 사건

- topic: `disciplinary_severity`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10913 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension, disciplinary_dismissal | issue_type_primary, disposition_type x1, text overlap x4 |  |  |
| 2 | id_13989 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension | issue_type_primary, disposition_type x1, text overlap x4 |  |  |
| 3 | id_26461 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension | issue_type_primary, disposition_type x1, text overlap x4 |  |  |
| 4 | id_28987 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension | issue_type_primary, disposition_type x1, text overlap x4 |  |  |
| 5 | id_30101 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | suspension | issue_type_primary, disposition_type x1, text overlap x4 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q14 — 감봉 처분이 과한지 본 사건

- topic: `disciplinary_severity`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_2951 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | pay_cut | issue_type_primary, disposition_type x1, text overlap x3 |  |  |
| 2 | id_33995 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | pay_cut | issue_type_primary, disposition_type x1, text overlap x3 |  |  |
| 3 | id_23951 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | pay_cut | issue_type_primary, disposition_type x1, text overlap x2 |  |  |
| 4 | id_24279 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | pay_cut | issue_type_primary, disposition_type x1, text overlap x2 |  |  |
| 5 | id_26071 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | pay_cut | issue_type_primary, disposition_type x1, text overlap x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q15 — 기간제 근로자의 갱신기대권이 인정되는지

- topic: `contract_expiry`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_347015 | ○ ○ ○ 부당해고 구제 재심신청 | renewal_expectation | fixed_term | nonrenewal | employment_stage, issue_type_primary, legal_focus x1, text overlap x3 |  |  |
| 2 | id_347319 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | fixed_term | nonrenewal | employment_stage, issue_type_primary, legal_focus x1, text overlap x3 |  |  |
| 3 | id_347727 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | fixed_term | nonrenewal | employment_stage, issue_type_primary, legal_focus x1, text overlap x3 |  |  |
| 4 | id_348069 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | fixed_term | nonrenewal | employment_stage, issue_type_primary, legal_focus x1, text overlap x3 |  |  |
| 5 | id_348151 | ○ ○ ○ 부당해고 구제 재심신청 | renewal_expectation | fixed_term | nonrenewal | employment_stage, issue_type_primary, legal_focus x1, text overlap x3 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10621 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | contract_termination | baseline_export |  |  |
| 2 | id_10737 | ○ ○ ○ 부당해고 구제 재심신청 | renewal_expectation | renewal_stage | nonrenewal | baseline_export |  |  |
| 3 | id_1079 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | contract_termination | baseline_export |  |  |
| 4 | id_10819 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal | baseline_export |  |  |
| 5 | id_1083 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | no_formal_disposition | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q16 — 계약기간 만료인데 사실상 해고처럼 다퉈진 사건

- topic: `contract_expiry`
- query_type: `composite`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_350961 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | fixed_term | contract_termination, nonrenewal | employment_stage, issue_type_primary, disposition_type x2, text overlap x2 |  |  |
| 2 | id_20657 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | fixed_term | contract_termination, nonrenewal | employment_stage, issue_type_primary, disposition_type x2, text overlap x1 |  |  |
| 3 | id_28955 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | fixed_term | contract_termination, nonrenewal | employment_stage, issue_type_primary, disposition_type x2, text overlap x1 |  |  |
| 4 | id_28965 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | fixed_term | contract_termination, nonrenewal | employment_stage, issue_type_primary, disposition_type x2, text overlap x1 |  |  |
| 5 | id_37709 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | contract_termination, nonrenewal | employment_stage, issue_type_primary, disposition_type x2, text overlap x1 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_36593 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | fixed_term | contract_termination | reason_category overlap: contract_expiry, text overlap x2 |  |  |
| 2 | id_406305 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | no_formal_disposition | reason_category overlap: no_dismissal, text overlap x2 |  |  |
| 3 | id_1079 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | contract_termination | reason_category overlap: contract_expiry, text overlap x2 |  |  |
| 4 | id_14033 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal | reason_category overlap: contract_expiry, text overlap x2 |  |  |
| 5 | id_1615 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal, dismissal | reason_category overlap: contract_expiry, text overlap x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q17 — 전보나 인사발령이 정당한지 다툰 사건

- topic: `transfer`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10613 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 2 | id_10989 | ○ ○ ○ 부당해고 구제신청 | unfair_treatment | renewal_stage | transfer, nonrenewal, no_formal_disposition | baseline_export |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_26243 | ○ ○ ○ 부당해고 구제신청 | transfer_validity | fixed_term | transfer, dismissal | issue_type_primary, disposition_type x1, text overlap x1 |  |  |
| 2 | id_2637 | ○ ○ ○ 부당해고 구제 재심신청 | transfer_validity | regular | transfer | issue_type_primary, disposition_type x1, text overlap x1 |  |  |
| 3 | id_28641 | ○ ○ ○ 부당해고 구제신청 | transfer_validity | regular | transfer, reprimand, pay_cut | issue_type_primary, disposition_type x1, text overlap x1 |  |  |
| 4 | id_28937 | ○ ○ ○ 부당해고 구제신청 | transfer_validity | regular | transfer, dismissal | issue_type_primary, disposition_type x1, text overlap x1 |  |  |
| 5 | id_29861 | ○ ○ ○ 부당해고 구제신청 | transfer_validity | regular | transfer | issue_type_primary, disposition_type x1, text overlap x1 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q18 — 대기발령이나 배치전환이 징계인지 인사권 행사인지 다툰 사건

- topic: `transfer`
- query_type: `natural_language`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_27603 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | suspension, transfer | reason_category overlap: misconduct, transfer, text overlap x1 |  |  |
| 2 | id_34657 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | suspension, transfer | reason_category overlap: misconduct, transfer, text overlap x1 |  |  |
| 3 | id_25077 | ○ ○ ○ 부당해고 구제 재심신청 | misconduct | regular | disciplinary_dismissal, transfer | reason_category overlap: misconduct, transfer |  |  |
| 4 | id_2755 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | pay_cut, transfer | reason_category overlap: transfer, text overlap x2 |  |  |
| 5 | id_16541 | ○ ○ ○ 부당해고 구제 재심신청 | misconduct | probation | dismissal | reason_category overlap: misconduct, text overlap x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_348033 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension, pay_cut, transfer | issue_type_primary, disposition_type x2, text overlap x1 |  |  |
| 2 | id_400879 | ○ ○ ○ 부당해고 구제 재심신청 | transfer_validity | regular | transfer, suspension | issue_type_primary, disposition_type x2, text overlap x1 |  |  |
| 3 | id_42399 | ○ ○ ○ 부당해고 구제신청 | transfer_validity | regular | suspension, transfer | issue_type_primary, disposition_type x2, text overlap x1 |  |  |
| 4 | id_12649 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | suspension, transfer | issue_type_primary, disposition_type x2 |  |  |
| 5 | id_14653 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension, transfer | issue_type_primary, disposition_type x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q19 — 폭행이나 욕설 같은 비위 사실 자체가 인정되는지가 핵심인 사건

- topic: `violence`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_2037 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | disciplinary_dismissal | reason_category overlap: violence, text overlap x5 |  |  |
| 2 | id_29475 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | reason_category overlap: violence, text overlap x3 |  |  |
| 3 | id_30101 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | suspension | reason_category overlap: violence, text overlap x3 |  |  |
| 4 | id_31647 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | reason_category overlap: violence, text overlap x3 |  |  |
| 5 | id_34973 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | pay_cut | reason_category overlap: violence, text overlap x3 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_24289 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | disciplinary_dismissal | issue_type_primary, fact_markers x2, text overlap x2 |  |  |
| 2 | id_27091 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | disciplinary_dismissal | issue_type_primary, fact_markers x2, text overlap x2 |  |  |
| 3 | id_27289 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | disciplinary_dismissal | issue_type_primary, fact_markers x2, text overlap x2 |  |  |
| 4 | id_3503 | ○ ○ ○ 부당해고 구제 재심신청 | misconduct | regular | disciplinary_dismissal | issue_type_primary, fact_markers x2, text overlap x2 |  |  |
| 5 | id_350431 | ○ ○ ○ 부당해고 구제 재심신청 | misconduct | regular | disciplinary_dismissal | issue_type_primary, fact_markers x2, text overlap x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q20 — 폭행은 있었지만 해고까지는 과하다고 본 사건

- topic: `violence`
- query_type: `composite`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_11561 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension | issue_type_primary, issue_type_secondary x1, legal_focus x1, text overlap x2 |  |  |
| 2 | id_12065 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, issue_type_secondary x1, legal_focus x1, text overlap x2 |  |  |
| 3 | id_16071 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | issue_type_primary, issue_type_secondary x1, legal_focus x1, text overlap x2 |  |  |
| 4 | id_19741 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, issue_type_secondary x1, legal_focus x1, text overlap x2 |  |  |
| 5 | id_19787 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, issue_type_secondary x1, legal_focus x1, text overlap x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 3 | id_10607 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 4 | id_10613 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | baseline_export |  |  |
| 5 | id_10677 | ○ ○ ○ 부당해고 구제신청 | misconduct | regular | dismissal | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q21 — 욕설이나 직장질서 문란이 반복되어 징계해고된 사건

- topic: `violence`
- query_type: `natural_language`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10901 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, disposition_type x1, fact_markers x1, text overlap x1 |  |  |
| 2 | id_19569 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, disposition_type x1, fact_markers x1, text overlap x1 |  |  |
| 3 | id_27243 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, disposition_type x1, fact_markers x1, text overlap x1 |  |  |
| 4 | id_31209 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | probation | disciplinary_dismissal, probation_termination | issue_type_primary, disposition_type x1, fact_markers x1, text overlap x1 |  |  |
| 5 | id_32123 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, disposition_type x1, fact_markers x1, text overlap x1 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q22 — 근로자성이 실제 핵심 쟁점인 사건

- topic: `worker_status`
- query_type: `single_axis`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_11225 | ○ ○ ○ 부당해고 구제신청 | worker_status | probation | other | reason_category overlap: worker_status, text overlap x3 |  |  |
| 2 | id_18475 | ○ ○ ○ 부당해고 구제신청 | worker_status | regular | dismissal | reason_category overlap: worker_status, text overlap x3 |  |  |
| 3 | id_349175 | ○ ○ ○ 부당해고 구제 재심신청 | worker_status | pre_hire | dismissal | reason_category overlap: worker_status, text overlap x3 |  |  |
| 4 | id_23407 | ○ ○ ○ 부당해고 구제신청 | worker_status | unknown | dismissal | reason_category overlap: worker_status, text overlap x2 |  |  |
| 5 | id_31551 | ○ ○ ○ 부당해고 구제신청 | worker_status | regular | dismissal | reason_category overlap: worker_status, text overlap x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_18475 | ○ ○ ○ 부당해고 구제신청 | worker_status | regular | dismissal | issue_type_primary, legal_focus x1, text overlap x3 |  |  |
| 2 | id_349175 | ○ ○ ○ 부당해고 구제 재심신청 | worker_status | pre_hire | dismissal | issue_type_primary, legal_focus x1, text overlap x3 |  |  |
| 3 | id_23407 | ○ ○ ○ 부당해고 구제신청 | worker_status | unknown | dismissal | issue_type_primary, legal_focus x1, text overlap x2 |  |  |
| 4 | id_31551 | ○ ○ ○ 부당해고 구제신청 | worker_status | regular | dismissal | issue_type_primary, legal_focus x1, text overlap x2 |  |  |
| 5 | id_33863 | ○ ○ ○ 부당해고 구제신청 | worker_status | regular | dismissal | issue_type_primary, legal_focus x1, text overlap x2 |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q23 — 괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건

- topic: `workplace_bullying`
- query_type: `natural_language`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_12489 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | dismissal | issue_type_primary, text overlap x2 |  |  |
| 2 | id_1989 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | dismissal | issue_type_primary, text overlap x2 |  |  |
| 3 | id_24205 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | issue_type_primary, text overlap x2 |  |  |
| 4 | id_345795 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | pay_cut, reprimand | issue_type_primary, text overlap x2 |  |  |
| 5 | id_346361 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | pay_cut | issue_type_primary, text overlap x2 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10771 | ○ ○ ○ 부당해고 구제신청 | workplace_harassment | regular | suspension | baseline_export |  |  |
| 2 | id_10819 | ○ ○ ○ 부당해고 구제신청 | renewal_expectation | renewal_stage | nonrenewal | baseline_export |  |  |
| 3 | id_10861 | ○ ○ ○ 부당해고 구제 재심신청 | disciplinary_severity | regular | suspension | baseline_export |  |  |
| 4 | id_10901 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | disciplinary_dismissal | baseline_export |  |  |
| 5 | id_10913 | ○ ○ ○ 부당해고 구제신청 | disciplinary_severity | regular | suspension, disciplinary_dismissal | baseline_export |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

## Q24 — 여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건

- topic: `dismissal_validity`
- query_type: `natural_language`
- evaluator task: 각 결과에 relevance `2/1/0` 부여

### System A

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_350303 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | rejection_of_regular_employment | issue_type_primary, legal_focus x2, text overlap x4 |  |  |
| 2 | id_12593 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | regular | dismissal | issue_type_primary, legal_focus x2, text overlap x3 |  |  |
| 3 | id_13391 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | dismissal | issue_type_primary, legal_focus x2, text overlap x3 |  |  |
| 4 | id_13415 | ○ ○ ○ 부당해고 구제신청 | dismissal_validity | probation | rejection_of_regular_employment | issue_type_primary, legal_focus x2, text overlap x3 |  |  |
| 5 | id_14079 | ○ ○ ○ 부당해고 구제 재심신청 | dismissal_validity | probation | rejection_of_regular_employment | issue_type_primary, legal_focus x2, text overlap x3 |  |  |

### System B

| rank | case_id | title | primary | stage | disposition | why surfaced | relevance | memo |
|------|---------|-------|---------|-------|-------------|--------------|-----------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | unfair_treatment | regular | dismissal | baseline_export |  |  |
| 2 |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

### Query-level Scorecard

- System A precision@5: 
- System B precision@5: 
- System A weighted relevance score@5: 
- System B weighted relevance score@5: 
- System A first relevant rank: 
- System B first relevant rank: 
- win/loss/tie: 
- memo: 

