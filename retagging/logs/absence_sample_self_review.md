# absence_sample_output.jsonl 1차 self-review 메모

## id_10071
- 변경 전 primary/disposition: dismissal_validity / ['dismissal']
- 변경 후 primary/disposition: dismissal_validity / ['no_formal_disposition']
- 변경 전 fact_markers: ['resignation_dispute', 'mutual_agreement']
- 변경 후 fact_markers: ['resignation_dispute', 'mutual_agreement']
- 변경 전 exclusion_flags: ['not_really_absence_case', 'resignation_dispute']
- 변경 후 exclusion_flags: ['not_really_absence_case', 'resignation_dispute']
- 변경 이유: 해고가 아니라 자발적 사직/합의해지 판단 사건이므로 disposition_type을 no_formal_disposition으로 보정.

## id_1013
- 변경 전 primary/disposition: misconduct / ['reprimand']
- 변경 후 primary/disposition: disciplinary_severity / ['other']
- 변경 전 fact_markers: []
- 변경 후 fact_markers: []
- 변경 전 exclusion_flags: ['not_really_absence_case', 'unrelated_to_dismissal']
- 변경 후 exclusion_flags: ['not_really_absence_case', 'unrelated_to_dismissal']
- 변경 이유: 견책은 v1 disposition enum에 없어 other로 처리. 판정 핵심도 비위 존재 자체보다 경징계 양정의 정당성에 가까워 primary를 disciplinary_severity로 보정.

## id_10237
- 변경 전 primary/disposition: misconduct / ['suspension']
- 변경 후 primary/disposition: disciplinary_severity / ['suspension']
- 변경 전 fact_markers: ['prior_sanction_history', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['prior_sanction_history', 'disciplinary_committee', 'evidence_sufficient']
- 변경 전 exclusion_flags: ['not_really_absence_case']
- 변경 후 exclusion_flags: ['not_really_absence_case']
- 변경 이유: 정직 3개월의 상당성이 결론 중심이므로 primary를 misconduct에서 disciplinary_severity로 보정.

## id_10249
- 변경 전 primary/disposition: absence_without_leave / ['dismissal']
- 변경 후 primary/disposition: misconduct / ['dismissal']
- 변경 전 fact_markers: ['unauthorized_absence', 'repeated_absence', 'written_notice']
- 변경 후 fact_markers: ['unauthorized_absence', 'written_notice']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: v1에는 absence_without_leave가 primary enum으로 없으므로 misconduct를 primary로 두고 absence_without_leave를 secondary로 유지. enum 밖 fact_marker(repeated_absence) 제거.

## id_10357
- 변경 전 primary/disposition: misconduct / ['disciplinary_dismissal']
- 변경 후 primary/disposition: misconduct / ['disciplinary_dismissal']
- 변경 전 fact_markers: ['prior_sanction_history', 'evidence_sufficient', 'repeated_absence', 'disciplinary_committee']
- 변경 후 fact_markers: ['prior_sanction_history', 'evidence_sufficient', 'disciplinary_committee']
- 변경 전 exclusion_flags: ['not_really_absence_case']
- 변경 후 exclusion_flags: ['not_really_absence_case']
- 변경 이유: v1 enum 밖 fact_marker(repeated_absence) 제거.

## id_10411
- 변경 전 primary/disposition: absence_without_leave / ['dismissal']
- 변경 후 primary/disposition: misconduct / ['dismissal']
- 변경 전 fact_markers: ['unauthorized_absence', 'repeated_absence', 'disciplinary_committee', 'written_notice']
- 변경 후 fact_markers: ['unauthorized_absence', 'disciplinary_committee', 'written_notice']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: v1에는 absence_without_leave가 primary enum으로 없어 misconduct primary + absence_without_leave secondary로 보정. enum 밖 fact_marker(repeated_absence) 제거.

## id_10487
- 변경 전 primary/disposition: misconduct / ['reprimand']
- 변경 후 primary/disposition: misconduct / ['other']
- 변경 전 fact_markers: ['warning_given', 'disciplinary_committee', 'written_notice']
- 변경 후 fact_markers: ['disciplinary_committee', 'written_notice']
- 변경 전 exclusion_flags: ['not_really_absence_case', 'unrelated_to_dismissal']
- 변경 후 exclusion_flags: ['not_really_absence_case', 'unrelated_to_dismissal']
- 변경 이유: 견책은 v1 disposition enum에 없어 other로 처리. enum 밖 fact_marker(warning_given) 제거.

## id_10543
- 변경 전 primary/disposition: misconduct / ['suspension']
- 변경 후 primary/disposition: misconduct / ['suspension']
- 변경 전 fact_markers: ['evidence_sufficient', 'public_institution']
- 변경 후 fact_markers: ['evidence_sufficient']
- 변경 전 exclusion_flags: ['not_really_absence_case']
- 변경 후 exclusion_flags: ['not_really_absence_case']
- 변경 이유: v1 enum 밖 fact_marker(public_institution) 제거. 공공부문 맥락은 industry_context=public으로 충분.

## id_10555
- 변경 전 primary/disposition: workplace_harassment / ['dismissal']
- 변경 후 primary/disposition: workplace_harassment / ['dismissal']
- 변경 전 fact_markers: ['unauthorized_absence', 'repeated_absence', 'disciplinary_committee', 'written_notice', 'evidence_sufficient']
- 변경 후 fact_markers: ['unauthorized_absence', 'disciplinary_committee', 'written_notice', 'evidence_sufficient']
- 변경 전 exclusion_flags: []
- 변경 후 exclusion_flags: []
- 변경 이유: industry_context=education은 v1 enum 밖이므로 service로 보정. enum 밖 fact_marker(repeated_absence) 제거.

