# violence_batch_022 manual recheck

- 작성시각: 2026-03-21 00:35
- 원칙: 자동 드래프트를 최종본으로 두지 않고, 케이스별 실제 판단 구조를 다시 확인
- 범위: `violence_batch_022`만 수동 재검토
- 검증: JSONL 파싱 확인 완료

| case_id | primary | secondary | disposition | exclusion_flags | confidence | rationale |
|---|---|---|---|---|---|---|
| id_30895 | disciplinary_severity | misconduct, procedure | dismissal | - | high | 상급자 지시거부와 폭언, 불성실 근무, 징계전력이 함께 인정되어 제재 수위와 절차 적정성이 결론을 좌우한다. |
| id_30903 | disciplinary_severity | misconduct, procedure, transfer_validity | suspension, demotion | unrelated_to_dismissal | high | 욕설 1건만 인정되고 나머지 징계사유는 입증이 약하며, 정직 3월과 직위해제 모두 과중한지 여부가 핵심이다. |
| id_30907 | disciplinary_severity | absence_without_leave, misconduct, procedure, training_opportunity, dismissal_validity | dismissal | - | high | 배치전환 수용 여부와 무단이탈이 섞여 있으나, 최종적으로는 폭언과 무단이탈에 대한 징계양정 판단이 중심이다. |
| id_30935 | disciplinary_severity | misconduct, procedure | dismissal | - | high | 동료 폭행은 인정되지만 우발성, 반성, 피해 정도를 함께 봐야 해서 해고 또는 정직의 상당성이 핵심이다. |
| id_30967 | disciplinary_severity | misconduct, procedure | dismissal | evidence_too_thin | medium | 미화직원 폭언과 일부 성적·폭력적 행위가 문제되지만, 인정 범위가 갈리고 징계수위가 결론을 좌우한다. |
| id_30995 | disciplinary_severity | misconduct, procedure, transfer_validity | suspension | unrelated_to_dismissal | high | 대기발령 중 출근, 외부 메일 발송 등 일부 비위만 인정되므로 징계사유의 범위와 징계양정이 중심이다. |
| id_3103 | disciplinary_severity | misconduct, procedure | disciplinary_dismissal | - | high | 강제추행·상해 유죄와 출입제한 위반, 피켓시위 등 복합 비위의 존재와 그에 대한 제재 적정성이 핵심이다. |
| id_31031 | disciplinary_severity | misconduct, procedure, transfer_validity, dismissal_validity | suspension | evidence_too_thin, unrelated_to_dismissal | medium | 대기발령 및 후행 정직이 연결된 사건으로, 일부 사유만 인정되는 상황에서 제재의 상당성과 실익이 쟁점이다. |
| id_31083 | procedure | misconduct, dismissal_validity | dismissal | unrelated_to_dismissal | high | 폭행 사유는 인정되지만 소명기회 부여와 해고 서면통지 의무 위반이 결론을 좌우한다. |
| id_3109 | workplace_harassment | disciplinary_severity, procedure | pay_cut | unrelated_to_dismissal | high | 직장 내 괴롭힘이 핵심이고, 감봉 2개월은 과도하지 않으며 절차도 적법한지 판단하는 사건이다. |
| id_31095 | disciplinary_severity | misconduct, procedure, retaliation | suspension | not_really_harassment_case, evidence_too_thin, unrelated_to_dismissal | medium | 회의방해와 상사 폭언은 징계사유로 보기 어렵고, 남은 업무지시거부에 대한 정직 3개월이 과한지 여부가 핵심이다. |
| id_31167 | disciplinary_severity | misconduct | dismissal | - | high | 노조활동, 업무거부, 무단이탈, 폭력성 언행이 혼재하지만 실제로는 징계사유 인정과 수위 판단이 중심이다. |
| id_31173 | dismissal_validity | - | no_formal_disposition | - | high | 해고 자체가 존재하지 않고, 설령 해고가 있었더라도 복귀명령으로 구제이익이 소멸하는지 보는 사건이다. |
| id_31195 | disciplinary_severity | misconduct, dismissal_validity | dismissal | not_really_harassment_case | high | 폭행 사건은 인정되나 해고가 과중한지, 그리고 부당노동행위가 성립하는지 여부가 핵심이다. |
| id_31231 | disciplinary_severity | absence_without_leave, misconduct, procedure | suspension, reprimand | unrelated_to_dismissal | high | 무단이탈과 폭행, 쌍방 충돌이 인정되는 가운데 정직과 견책의 조합이 적정한지 판단하는 사건이다. |
| id_31235 | disciplinary_severity | misconduct | dismissal | - | high | 반말, 불화, 업무불이행, 폭행 주장 등이 섞여 있어 각 징계사유의 인정 범위와 징계수위가 핵심이다. |
| id_31285 | dismissal_validity | misconduct | no_formal_disposition | not_really_harassment_case, resignation_dispute, unrelated_to_dismissal | high | 사직서 제출로 근로관계가 종료되어 해고가 존재하지 않는지 여부가 결론을 좌우한다. |
| id_31289 | disciplinary_severity | misconduct, training_opportunity | dismissal | - | high | 규정 위반 식재료 판매, 인건비 반환, 포인트 수령, 욕설 등 복합 비위의 인정 범위와 징계수위가 중심이다. |
| id_3129 | disciplinary_severity | misconduct, procedure | suspension | unrelated_to_dismissal | high | 욕설, 금고 관련 보고절차 위반, 외부 누설, 무단이석 등 일부 인정 사유의 비위 정도와 제재 수위가 쟁점이다. |
| id_31293 | disciplinary_severity | misconduct | dismissal | - | high | 성희롱 전부는 아니더라도 인격모독성 발언 등 일부 징계사유가 인정되며, 해고 또는 중징계의 상당성이 핵심이다. |
| id_31317 | disciplinary_severity | misconduct, procedure | dismissal | - | high | 업무지시 불이행, 폭력적 언동, 협박, 갈등 유발이 복합적으로 인정되며 제재 수위가 핵심이다. |
| id_31357 | workplace_harassment | misconduct, evaluation, procedure, training_opportunity, disciplinary_severity | demotion | - | high | 직장 내 성희롱과 괴롭힘이 인정되고, 강직(降職) 징계가 과하지 않은지와 절차 적법성이 핵심이다. |
| id_31393 | disciplinary_severity | misconduct, procedure | suspension | unrelated_to_dismissal | high | 상호 폭행 사건에서 피해 정도, 경위서 제출 거부, 징계형평이 함께 문제되어 양정이 핵심이다. |
| id_31445 | disciplinary_severity | misconduct, procedure, dismissal_validity, retaliation | dismissal | not_really_harassment_case | high | 위협적 언행, 선물 요구·수령, 폭행이 인정되고 해고 정당성과 부당노동행위 부존재가 쟁점이다. |
| id_31517 | dismissal_validity | misconduct, work_ability, evaluation | probation_termination | - | high | 수습기간 중 폭행과 조직 내 불화가 시용 해지 사유가 되는지, 그리고 수습평가 구조가 핵심이다. |
| id_31521 | disciplinary_severity | performance, procedure, dismissal_validity | suspension | unrelated_to_dismissal | high | 경영진을 향한 모욕적 발언에 대해 정직 7일이 적정한지와 절차상 하자가 없는지가 핵심이다. |
| id_3155 | renewal_expectation | misconduct, procedure, disciplinary_severity | dismissal | not_really_harassment_case, renewal_expectation_dominant | high | 기간제 근로계약에서 갱신기대권이 인정되지 않아 계약기간 만료 종료로 보는지 판단하는 사건이다. |
| id_3157 | dismissal_validity | misconduct, procedure | no_formal_disposition | not_really_harassment_case, resignation_dispute, unrelated_to_dismissal | high | 사직서 제출과 수리로 임의퇴직이 성립하여 해고가 존재하지 않는지 보는 사건이다. |
| id_31629 | dismissal_validity | misconduct | dismissal | - | high | 우발적인 반말과 욕설만으로는 해고에 이를 정도의 정당한 사유가 되지 않는지가 핵심이다. |
| id_31635 | disciplinary_severity | absence_without_leave, misconduct, procedure, transfer_validity | suspension | evidence_too_thin, unrelated_to_dismissal | medium | 인정되는 징계사유와 무단결근 등이 혼재하고, 정직·대기발령의 실익과 비례성이 문제되는 사건이다. |
