# violence_sample_output.jsonl 1차 self-review 메모

## 2022부노OOO
- 변경 전 disposition_type: ['other']
- 변경 후 disposition_type: ['other']
- 변경 전 fact_markers: ['evidence_insufficient', 'emotional_conflict_only']
- 변경 후 fact_markers: ['evidence_insufficient']
- 변경 이유: v1 enum 외 fact_marker(emotional_conflict_only) 제거.

## id_10165
- 변경 전 disposition_type: ['dismissal']
- 변경 후 disposition_type: ['no_formal_disposition']
- 변경 전 fact_markers: ['resignation_dispute']
- 변경 후 fact_markers: ['resignation_dispute']
- 변경 이유: 해고 부존재 사건이므로 disposition_type을 dismissal에서 no_formal_disposition으로 보정.

## id_10191
- 변경 전 disposition_type: ['rejection_of_regular_employment']
- 변경 후 disposition_type: ['rejection_of_regular_employment']
- 변경 전 fact_markers: ['probation_period', 'qualitative_evaluation', 'repeated_absence']
- 변경 후 fact_markers: ['probation_period', 'qualitative_evaluation', 'evidence_sufficient']
- 변경 이유: v1 enum 외 fact_marker(repeated_absence) 제거, 판정 요지상 입증 충분으로 보정.

## id_10465
- 변경 전 disposition_type: ['rejection_of_regular_employment']
- 변경 후 disposition_type: ['probation_termination']
- 변경 전 fact_markers: ['probation_period', 'qualitative_evaluation']
- 변경 후 fact_markers: ['probation_period', 'qualitative_evaluation', 'evidence_sufficient']
- 변경 이유: 시용기간 내 해고 사건이므로 disposition_type을 rejection_of_regular_employment에서 probation_termination으로 보정.

