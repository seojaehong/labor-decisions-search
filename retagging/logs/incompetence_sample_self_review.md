# incompetence_sample_output.jsonl 1차 self-review 메모

## id_10181
- 변경 전 primary/disposition: performance / ['rejection_of_regular_employment']
- 변경 후 primary/disposition: dismissal_validity / ['rejection_of_regular_employment']
- 변경 전 fact_markers: ['probation_period', 'qualitative_evaluation', 'evidence_insufficient', 'short_tenure']
- 변경 후 fact_markers: ['probation_period', 'qualitative_evaluation', 'evidence_insufficient']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: performance는 v1 primary enum 밖이라 dismissal_validity로 보정. 핵심은 객관적 평가·입증 부족에 따른 본채용 거부 부당. short_tenure는 사실관계상 불명확해 제거.

## id_10201
- 변경 전 primary/disposition: disciplinary_severity / ['suspension']
- 변경 후 primary/disposition: disciplinary_severity / ['suspension']
- 변경 전 fact_markers: ['prior_sanction_history', 'disciplinary_committee', 'comparative_employee_case']
- 변경 후 fact_markers: ['prior_sanction_history', 'disciplinary_committee', 'comparative_employee_case']
- 변경 전 exclusion_flags: ['not_really_performance_case']
- 변경 후 exclusion_flags: ['fact_specific_low_reusability']
- 변경 이유: not_really_performance_case는 v1 enum 밖이므로 제거. 레거시 incompetence 노이즈 제어는 notes와 exclude query로 처리.

## id_10293
- 변경 전 primary/disposition: performance / ['rejection_of_regular_employment']
- 변경 후 primary/disposition: work_ability / ['rejection_of_regular_employment']
- 변경 전 fact_markers: ['probation_period', 'quantitative_evaluation', 'qualitative_evaluation', 'evidence_sufficient', 'written_notice']
- 변경 후 fact_markers: ['probation_period', 'quantitative_evaluation', 'qualitative_evaluation', 'evidence_sufficient', 'written_notice']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: performance는 v1 primary enum 밖이므로 work_ability를 primary로, performance를 secondary로 보정.

## id_10419
- 변경 전 primary/disposition: performance / ['rejection_of_regular_employment']
- 변경 후 primary/disposition: work_ability / ['rejection_of_regular_employment']
- 변경 전 fact_markers: ['probation_period', 'quantitative_evaluation', 'evidence_sufficient']
- 변경 후 fact_markers: ['probation_period', 'quantitative_evaluation', 'evidence_sufficient']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: performance는 v1 primary enum 밖이므로 work_ability를 primary로, performance를 secondary로 보정.

## id_10731
- 변경 전 primary/disposition: renewal_expectation / ['nonrenewal']
- 변경 후 primary/disposition: renewal_expectation / ['nonrenewal']
- 변경 전 fact_markers: ['long_tenure', 'evidence_insufficient']
- 변경 후 fact_markers: ['evidence_insufficient']
- 변경 전 exclusion_flags: ['not_really_performance_case', 'renewal_expectation_dominant']
- 변경 후 exclusion_flags: ['renewal_expectation_dominant']
- 변경 이유: long_tenure와 not_really_performance_case는 v1 enum 밖이라 제거. 갱신기대권 중심성은 renewal_expectation_dominant로 충분.

## id_11105
- 변경 전 primary/disposition: transfer_validity / ['demotion', 'transfer']
- 변경 후 primary/disposition: procedure / ['transfer']
- 변경 전 fact_markers: ['procedural_defect', 'evidence_insufficient', 'public_institution']
- 변경 후 fact_markers: ['procedural_defect', 'evidence_insufficient']
- 변경 전 exclusion_flags: ['not_really_performance_case', 'unrelated_to_dismissal']
- 변경 후 exclusion_flags: ['unrelated_to_dismissal']
- 변경 이유: transfer_validity와 demotion은 v1 primary/disposition enum 밖이므로 procedure primary + transfer disposition으로 단순화. 공공기관 fact_marker 제거.

## id_11439
- 변경 전 primary/disposition: work_ability / ['dismissal']
- 변경 후 primary/disposition: work_ability / ['dismissal']
- 변경 전 fact_markers: ['evidence_insufficient', 'written_notice']
- 변경 후 fact_markers: ['evidence_insufficient', 'written_notice']
- 변경 전 exclusion_flags: ['not_really_performance_case']
- 변경 후 exclusion_flags: []
- 변경 이유: not_really_performance_case는 v1 enum 밖이라 제거. 질병 해고와 저성과 구별은 notes와 query로 관리.

## id_11527
- 변경 전 primary/disposition: renewal_expectation / ['nonrenewal']
- 변경 후 primary/disposition: renewal_expectation / ['nonrenewal']
- 변경 전 fact_markers: ['quantitative_evaluation', 'evidence_insufficient']
- 변경 후 fact_markers: ['quantitative_evaluation', 'evidence_insufficient']
- 변경 전 exclusion_flags: ['renewal_expectation_dominant']
- 변경 후 exclusion_flags: ['renewal_expectation_dominant']
- 변경 이유: performance 쟁점처럼 보여도 primary는 renewal_expectation 유지가 적절함을 재확인.

## id_11659
- 변경 전 primary/disposition: dismissal_validity / ['dismissal']
- 변경 후 primary/disposition: dismissal_validity / ['dismissal']
- 변경 전 fact_markers: ['written_notice_missing', 'evidence_insufficient', 'resignation_dispute', 'short_tenure']
- 변경 후 fact_markers: ['written_notice_missing', 'evidence_insufficient', 'resignation_dispute', 'short_tenure']
- 변경 전 exclusion_flags: ['not_really_performance_case', 'procedure_dominant']
- 변경 후 exclusion_flags: ['procedure_dominant']
- 변경 이유: not_really_performance_case는 v1 enum 밖이라 제거. 실질 쟁점은 해고 존부 및 서면통지 위반으로 유지.

## id_1181
- 변경 전 primary/disposition: workplace_harassment / ['disciplinary_dismissal']
- 변경 후 primary/disposition: workplace_harassment / ['disciplinary_dismissal']
- 변경 전 fact_markers: ['investigation_conducted', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['disciplinary_committee', 'evidence_sufficient']
- 변경 전 exclusion_flags: ['not_really_performance_case']
- 변경 후 exclusion_flags: []
- 변경 이유: investigation_conducted와 not_really_performance_case는 v1 enum 밖이라 제거.

## id_11825
- 변경 전 primary/disposition: renewal_expectation / ['nonrenewal']
- 변경 후 primary/disposition: renewal_expectation / ['nonrenewal']
- 변경 전 fact_markers: ['evidence_insufficient']
- 변경 후 fact_markers: ['evidence_insufficient']
- 변경 전 exclusion_flags: ['not_really_performance_case', 'renewal_expectation_dominant']
- 변경 후 exclusion_flags: ['renewal_expectation_dominant']
- 변경 이유: not_really_performance_case는 v1 enum 밖이라 제거.

## id_11931
- 변경 전 primary/disposition: performance / ['probation_termination']
- 변경 후 primary/disposition: work_ability / ['probation_termination']
- 변경 전 fact_markers: ['probation_period', 'qualitative_evaluation', 'warning_given', 'short_tenure', 'written_notice', 'public_institution']
- 변경 후 fact_markers: ['probation_period', 'qualitative_evaluation', 'short_tenure', 'written_notice']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: performance/attendance는 보조 요소이고 중심은 수습 적격성 판단이므로 work_ability로 보정. enum 밖 fact_marker 제거.

## id_12169
- 변경 전 primary/disposition: renewal_expectation / ['contract_termination']
- 변경 후 primary/disposition: renewal_expectation / ['contract_termination']
- 변경 전 fact_markers: []
- 변경 후 fact_markers: []
- 변경 전 exclusion_flags: ['not_really_performance_case', 'renewal_expectation_dominant']
- 변경 후 exclusion_flags: ['renewal_expectation_dominant']
- 변경 이유: 갱신기대권 부정 사건이므로 employment_stage를 fixed_term보다 renewal_stage로 보정. not_really_performance_case 제거.

## id_12197
- 변경 전 primary/disposition: dismissal_validity / ['dismissal']
- 변경 후 primary/disposition: dismissal_validity / ['dismissal']
- 변경 전 fact_markers: ['procedural_defect', 'evidence_insufficient']
- 변경 후 fact_markers: ['procedural_defect', 'evidence_insufficient']
- 변경 전 exclusion_flags: ['not_really_performance_case']
- 변경 후 exclusion_flags: []
- 변경 이유: not_really_performance_case는 v1 enum 밖이라 제거.

## id_1221
- 변경 전 primary/disposition: misconduct / ['rejection_of_regular_employment']
- 변경 후 primary/disposition: misconduct / ['rejection_of_regular_employment']
- 변경 전 fact_markers: ['probation_period', 'investigation_conducted', 'evidence_sufficient']
- 변경 후 fact_markers: ['probation_period', 'evidence_sufficient']
- 변경 전 exclusion_flags: ['not_really_performance_case']
- 변경 후 exclusion_flags: []
- 변경 이유: 본채용 거부 사유가 성희롱인 misconduct 사건으로 유지. not_really_performance_case 제거.

## id_12275
- 변경 전 primary/disposition: performance / ['rejection_of_regular_employment']
- 변경 후 primary/disposition: work_ability / ['rejection_of_regular_employment']
- 변경 전 fact_markers: ['probation_period', 'quantitative_evaluation', 'evidence_sufficient']
- 변경 후 fact_markers: ['probation_period', 'quantitative_evaluation', 'evidence_sufficient']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: 평가점수 미달과 적격성 판단이 결합된 수습 사건이므로 work_ability primary로 보정.

## id_12477
- 변경 전 primary/disposition: disciplinary_severity / ['suspension']
- 변경 후 primary/disposition: disciplinary_severity / ['suspension']
- 변경 전 fact_markers: ['prior_sanction_history', 'comparative_employee_case']
- 변경 후 fact_markers: ['prior_sanction_history', 'comparative_employee_case']
- 변경 전 exclusion_flags: ['not_really_performance_case']
- 변경 후 exclusion_flags: []
- 변경 이유: not_really_performance_case는 v1 enum 밖이라 제거.

## id_12727
- 변경 전 primary/disposition: procedure / ['probation_termination']
- 변경 후 primary/disposition: procedure / ['probation_termination']
- 변경 전 fact_markers: ['probation_period', 'procedural_defect', 'evidence_insufficient']
- 변경 후 fact_markers: ['probation_period', 'procedural_defect', 'evidence_insufficient']
- 변경 전 exclusion_flags: ['procedure_dominant']
- 변경 후 exclusion_flags: ['procedure_dominant']
- 변경 이유: performance 요소가 있으나 절차 미이행이 결론을 좌우하므로 procedure primary 유지가 적절함을 재확인.

## id_13013
- 변경 전 primary/disposition: attendance / ['rejection_of_regular_employment']
- 변경 후 primary/disposition: work_ability / ['rejection_of_regular_employment']
- 변경 전 fact_markers: ['probation_period', 'repeated_absence', 'warning_given', 'improvement_opportunity_given', 'quantitative_evaluation', 'short_tenure']
- 변경 후 fact_markers: ['probation_period', 'improvement_opportunity_given', 'quantitative_evaluation', 'short_tenure']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: attendance는 v1 primary enum 밖이고, 수습 적격성 판단 사건이므로 work_ability primary로 보정. enum 밖 fact_marker 제거.

