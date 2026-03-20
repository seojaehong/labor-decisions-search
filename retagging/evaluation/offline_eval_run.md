# Offline Eval Run

## Q01 — 반복 무단결근으로 해고된 사건

- query_type: `single_axis`
- topic: `absence`
- baseline_reason_categories: `absence`
- candidate_profile: `{"issue_type_primary": ["absence_without_leave"], "fact_markers": ["repeated_absence", "unauthorized_absence"], "disposition_type": ["dismissal", "disciplinary_dismissal"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10561 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10563 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10757 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10815 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10845 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_27267 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, fact_markers x2, include_for_queries x1 |  |  |
| 2 | id_15705 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, fact_markers x2 |  |  |
| 3 | id_16387 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, fact_markers x2 |  |  |
| 4 | id_16633 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, fact_markers x2 |  |  |
| 5 | id_16659 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x1, fact_markers x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q02 — 무단결근이 언급되지만 실제 핵심은 절차 위반인 사건

- query_type: `composite`
- topic: `absence`
- baseline_reason_categories: `absence`
- candidate_profile: `{"issue_type_primary": ["procedure", "dismissal_validity"], "fact_markers": ["unauthorized_absence"], "exclusion_flags": ["not_really_absence_case", "procedure_dominant"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10561 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10563 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10757 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10815 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10845 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10907 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1 |  |  |
| 2 | id_11339 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x1 |  |  |
| 3 | id_11401 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1 |  |  |
| 4 | id_11577 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x1 |  |  |
| 5 | id_11715 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q03 — 택시나 버스 기사 무단결근 징계해고

- query_type: `natural_language`
- topic: `absence`
- baseline_reason_categories: `absence`
- candidate_profile: `{"issue_type_primary": ["absence_without_leave", "disciplinary_severity"], "industry_context": ["transport"], "fact_markers": ["unauthorized_absence"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10561 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10563 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10757 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10815 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10845 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_34245 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x1, industry_context, include_for_queries x1 |  |  |
| 2 | id_24667 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x1, industry_context, include_for_queries x1 |  |  |
| 3 | id_31545 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1, industry_context, include_for_queries x1 |  |  |
| 4 | id_31961 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x1, industry_context, include_for_queries x1 |  |  |
| 5 | id_31989 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1, industry_context, include_for_queries x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q04 — 직장내괴롭힘이 실제로 성립하는지 다툰 사건

- query_type: `single_axis`
- topic: `workplace_bullying`
- baseline_reason_categories: `workplace_bullying`
- candidate_profile: `{"issue_type_primary": ["workplace_harassment"], "legal_focus": ["evidentiary_sufficiency", "duty_of_investigation"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10771 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10819 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10861 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10901 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10913 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_255 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2 |  |  |
| 2 | id_349227 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, legal_focus x2 |  |  |
| 3 | id_349905 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2 |  |  |
| 4 | id_40297 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2 |  |  |
| 5 | id_406201 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q05 — 직장내괴롭힘 신고 후 불이익이나 보복이 문제 된 사건

- query_type: `single_axis`
- topic: `workplace_bullying`
- baseline_reason_categories: `workplace_bullying, union_activity`
- candidate_profile: `{"issue_type_primary": ["retaliation", "unfair_treatment"], "fact_markers": ["harassment_report_filed"], "legal_focus": ["protection_against_retaliation"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 | id_10607 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10727 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 4 | id_10771 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10819 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10995 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |
| 2 | id_11565 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |
| 3 | id_11929 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |
| 4 | id_12583 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |
| 5 | id_12679 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q06 — 괴롭힘은 인정되는데 징계 수위가 과한지 보는 사건

- query_type: `composite`
- topic: `workplace_bullying`
- baseline_reason_categories: `workplace_bullying, violence`
- candidate_profile: `{"issue_type_primary": ["disciplinary_severity"], "issue_type_secondary": ["workplace_harassment"], "legal_focus": ["proportionality", "appropriateness_of_discipline"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 3 | id_10607 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 4 | id_10613 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10677 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_21087 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, issue_type_secondary x1, legal_focus x2 |  |  |
| 2 | id_21941 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, issue_type_secondary x1, legal_focus x2 |  |  |
| 3 | id_22773 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, issue_type_secondary x1, legal_focus x2 |  |  |
| 4 | id_23551 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, issue_type_secondary x1, legal_focus x2 |  |  |
| 5 | id_24285 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, issue_type_secondary x1, legal_focus x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q07 — 수습기간 중 본채용 거부가 정당한지

- query_type: `single_axis`
- topic: `probation`
- baseline_reason_categories: `probation`
- candidate_profile: `{"employment_stage": ["probation"], "issue_type_primary": ["dismissal_validity"], "disposition_type": ["rejection_of_regular_employment"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10575 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10597 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10603 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10621 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10633 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_20753 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x2 |  |  |
| 2 | id_343439 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x2 |  |  |
| 3 | id_343669 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x2 |  |  |
| 4 | id_344265 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x2 |  |  |
| 5 | id_349243 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q08 — 수습기간 중 업무능력 부족으로 해고하거나 본채용 거부한 사건

- query_type: `composite`
- topic: `probation`
- baseline_reason_categories: `probation, incompetence`
- candidate_profile: `{"employment_stage": ["probation"], "issue_type_primary": ["dismissal_validity", "work_ability"], "disposition_type": ["probation_termination", "rejection_of_regular_employment"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10575 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10597 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10603 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10621 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10633 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_348399 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, disposition_type x2, include_for_queries x3 |  |  |
| 2 | id_38289 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x4 |  |  |
| 3 | id_20753 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x3 |  |  |
| 4 | id_23631 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x2 |  |  |
| 5 | id_343439 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x1, include_for_queries x3 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q09 — 수습인데 서면통지나 절차 문제가 있는 사건

- query_type: `composite`
- topic: `probation`
- baseline_reason_categories: `probation`
- candidate_profile: `{"employment_stage": ["probation"], "issue_type_primary": ["dismissal_validity", "procedure"], "fact_markers": ["written_notice_missing"], "legal_focus": ["procedural_due_process"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10575 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10597 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10603 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10621 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10633 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_30811 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x2 |  |  |
| 2 | id_348735 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |
| 3 | id_37879 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |
| 4 | id_38001 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |
| 5 | id_38095 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, fact_markers x1, legal_focus x1, include_for_queries x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q10 — 정규직 저성과나 업무능력 부족으로 해고된 사건

- query_type: `single_axis`
- topic: `incompetence`
- baseline_reason_categories: `incompetence`
- candidate_profile: `{"employment_stage": ["regular"], "issue_type_primary": ["work_ability"], "fact_markers": ["qualitative_evaluation", "quantitative_evaluation"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_13295 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_13323 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_14007 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 4 | id_14077 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 5 | id_14241 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_22323 | ○ ○ ○ 부당노동행위 구제신청 | employment_stage, issue_type_primary, fact_markers x1, include_for_queries x1 |  |  |
| 2 | id_17059 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, fact_markers x1 |  |  |
| 3 | id_43869 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, fact_markers x1 |  |  |
| 4 | id_46597 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, fact_markers x1 |  |  |
| 5 | id_14077 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, include_for_queries x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q11 — 개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건

- query_type: `composite`
- topic: `incompetence`
- baseline_reason_categories: `incompetence`
- candidate_profile: `{"issue_type_primary": ["work_ability", "dismissal_validity"], "fact_markers": ["warning_given", "improvement_opportunity_given", "training_provided"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_13295 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_13323 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_14007 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 4 | id_14077 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 5 | id_14241 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_348399 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x3, include_for_queries x1 |  |  |
| 2 | id_22799 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x3 |  |  |
| 3 | id_51313 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x3 |  |  |
| 4 | id_33547 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x2, include_for_queries x1 |  |  |
| 5 | id_20989 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q12 — 징계사유는 인정되지만 해고가 너무 과하다고 본 사건

- query_type: `single_axis`
- topic: `disciplinary_severity`
- baseline_reason_categories: `violence, misconduct, absence`
- candidate_profile: `{"issue_type_primary": ["disciplinary_severity"], "legal_focus": ["proportionality", "appropriateness_of_discipline"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_37529 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, legal_focus x2, include_for_queries x1 |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, legal_focus x2 |  |  |
| 3 | id_10561 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2 |  |  |
| 4 | id_10563 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2 |  |  |
| 5 | id_10607 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q13 — 정직 처분 양정이 적정한지 본 사건

- query_type: `single_axis`
- topic: `disciplinary_severity`
- baseline_reason_categories: `violence, misconduct`
- candidate_profile: `{"issue_type_primary": ["disciplinary_severity"], "disposition_type": ["suspension"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_23551 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 2 | id_36525 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 3 | id_39431 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 4 | id_39689 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 5 | id_401981 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q14 — 감봉 처분이 과한지 본 사건

- query_type: `single_axis`
- topic: `disciplinary_severity`
- baseline_reason_categories: `violence, misconduct`
- candidate_profile: `{"issue_type_primary": ["disciplinary_severity"], "disposition_type": ["pay_cut"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_11029 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1 |  |  |
| 2 | id_11055 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1 |  |  |
| 3 | id_11755 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1 |  |  |
| 4 | id_11871 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1 |  |  |
| 5 | id_12331 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q15 — 기간제 근로자의 갱신기대권이 인정되는지

- query_type: `single_axis`
- topic: `contract_expiry`
- baseline_reason_categories: `contract_expiry`
- candidate_profile: `{"employment_stage": ["renewal_stage", "fixed_term"], "issue_type_primary": ["renewal_expectation"], "legal_focus": ["expectation_of_renewal"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10621 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10737 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 3 | id_1079 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 4 | id_10819 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_1083 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_14007 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |
| 2 | id_14739 | ○ ○ ○ 부당해고 구제 재심신청 | employment_stage, issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |
| 3 | id_15527 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |
| 4 | id_15993 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |
| 5 | id_17591 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q16 — 계약기간 만료인데 사실상 해고처럼 다퉈진 사건

- query_type: `composite`
- topic: `contract_expiry`
- baseline_reason_categories: `contract_expiry, no_dismissal`
- candidate_profile: `{"employment_stage": ["renewal_stage", "fixed_term"], "issue_type_primary": ["renewal_expectation", "dismissal_validity"], "disposition_type": ["contract_termination", "nonrenewal"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_20657 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x2 |  |  |
| 2 | id_28955 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x2 |  |  |
| 3 | id_28965 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x2 |  |  |
| 4 | id_350961 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x2 |  |  |
| 5 | id_37709 | ○ ○ ○ 부당해고 구제신청 | employment_stage, issue_type_primary, disposition_type x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q17 — 전보나 인사발령이 정당한지 다툰 사건

- query_type: `single_axis`
- topic: `transfer`
- baseline_reason_categories: `transfer`
- candidate_profile: `{"issue_type_primary": ["transfer_validity"], "disposition_type": ["transfer"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10613 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10989 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_3219 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 2 | id_347971 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 3 | id_36001 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 4 | id_37669 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, include_for_queries x1 |  |  |
| 5 | id_15623 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q18 — 대기발령이나 배치전환이 징계인지 인사권 행사인지 다툰 사건

- query_type: `natural_language`
- topic: `transfer`
- baseline_reason_categories: `transfer, misconduct`
- candidate_profile: `{"issue_type_primary": ["transfer_validity", "disciplinary_severity"], "disposition_type": ["transfer", "suspension"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_37669 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x2, include_for_queries x1 |  |  |
| 2 | id_12649 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x2 |  |  |
| 3 | id_14653 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x2 |  |  |
| 4 | id_25245 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x2 |  |  |
| 5 | id_26797 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q19 — 폭행이나 욕설 같은 비위 사실 자체가 인정되는지가 핵심인 사건

- query_type: `single_axis`
- topic: `violence`
- baseline_reason_categories: `violence, misconduct`
- candidate_profile: `{"issue_type_primary": ["misconduct"], "fact_markers": ["evidence_sufficient", "investigation_conducted"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_17439 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x2 |  |  |
| 2 | id_18019 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x2 |  |  |
| 3 | id_24289 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x2 |  |  |
| 4 | id_26477 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, fact_markers x2 |  |  |
| 5 | id_27091 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, fact_markers x2 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q20 — 폭행은 있었지만 해고까지는 과하다고 본 사건

- query_type: `composite`
- topic: `violence`
- baseline_reason_categories: `violence`
- candidate_profile: `{"issue_type_primary": ["disciplinary_severity"], "issue_type_secondary": ["misconduct"], "legal_focus": ["proportionality"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 3 | id_10607 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 4 | id_10613 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10677 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_37529 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, issue_type_secondary x1, legal_focus x1, include_for_queries x1 |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, issue_type_secondary x1, legal_focus x1 |  |  |
| 3 | id_10561 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, issue_type_secondary x1, legal_focus x1 |  |  |
| 4 | id_10607 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, issue_type_secondary x1, legal_focus x1 |  |  |
| 5 | id_10613 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, issue_type_secondary x1, legal_focus x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q21 — 욕설이나 직장질서 문란이 반복되어 징계해고된 사건

- query_type: `natural_language`
- topic: `violence`
- baseline_reason_categories: `violence, misconduct`
- candidate_profile: `{"issue_type_primary": ["misconduct", "disciplinary_severity"], "disposition_type": ["disciplinary_dismissal"], "fact_markers": ["prior_sanction_history"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_24671 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x1, fact_markers x1, include_for_queries x1 |  |  |
| 2 | id_10509 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, disposition_type x1, fact_markers x1 |  |  |
| 3 | id_10901 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, fact_markers x1 |  |  |
| 4 | id_12017 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, fact_markers x1 |  |  |
| 5 | id_14291 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, disposition_type x1, fact_markers x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q22 — 근로자성이 실제 핵심 쟁점인 사건

- query_type: `single_axis`
- topic: `worker_status`
- baseline_reason_categories: `worker_status`
- candidate_profile: `{"issue_type_primary": ["worker_status"], "legal_focus": ["worker_status_determination"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_32287 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |
| 2 | id_32489 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |
| 3 | id_3801 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x1, include_for_queries x1 |  |  |
| 4 | id_18475 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x1 |  |  |
| 5 | id_19165 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q23 — 괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건

- query_type: `natural_language`
- topic: `workplace_bullying`
- baseline_reason_categories: `workplace_bullying`
- candidate_profile: `{"issue_type_primary": ["unfair_treatment", "disciplinary_severity", "procedure"], "exclusion_flags": ["not_really_harassment_case", "emotional_conflict_not_harassment"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10771 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 2 | id_10819 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 3 | id_10861 | ○ ○ ○ 부당해고 구제 재심신청 | baseline_export |  |  |
| 4 | id_10901 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |
| 5 | id_10913 | ○ ○ ○ 부당해고 구제신청 | baseline_export |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10561 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary |  |  |
| 2 | id_10563 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary |  |  |
| 3 | id_10613 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary |  |  |
| 4 | id_10679 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary |  |  |
| 5 | id_10815 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

## Q24 — 여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건

- query_type: `natural_language`
- topic: `dismissal_validity`
- baseline_reason_categories: `violence, absence, misconduct`
- candidate_profile: `{"issue_type_primary": ["dismissal_validity"], "legal_focus": ["just_cause", "social_norm_reasonableness"]}`

### Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_10479 | ○ ○ ○ 부당노동행위 구제신청 | baseline_export |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

### Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 | id_349749 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2, include_for_queries x1 |  |  |
| 2 | id_349845 | ○ ○ ○ 부당해고 구제 재심신청 | issue_type_primary, legal_focus x2, include_for_queries x1 |  |  |
| 3 | id_350133 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2, include_for_queries x1 |  |  |
| 4 | id_350193 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2, include_for_queries x1 |  |  |
| 5 | id_350223 | ○ ○ ○ 부당해고 구제신청 | issue_type_primary, legal_focus x2, include_for_queries x1 |  |  |

### Query Summary

- baseline precision@5: 
- candidate precision@5: 
- baseline weighted relevance score@5: 
- candidate weighted relevance score@5: 
- baseline first relevant rank: 
- candidate first relevant rank: 
- win/loss/tie: 
- memo: 

