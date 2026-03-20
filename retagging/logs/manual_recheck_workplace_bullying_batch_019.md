# workplace_bullying_batch_019 manual recheck

- 작성시각: 2026-03-20 22:21
- 목적: 자동 초안을 기준으로 삼지 않고, 사용자 프롬프트 기준으로 케이스별 수동 판정을 확정
- 원칙: 실제 위원회 판단구조를 우선하고, `workplace_harassment`는 핵심일 때만 primary로 둠

| case_id | primary | secondary | disposition | exclusion_flags | confidence | rationale |
|---|---|---|---|---|---|---|
| id_405489 | transfer_validity | procedure, workplace_harassment, harassment_report | suspension | unrelated_to_dismissal | high | 괴롭힘 신고 조사와 연동된 대기발령의 업무상 필요성과 생활상 불이익을 비교한 인사명령 사건. |
| id_405499 | disciplinary_severity | procedure, workplace_harassment | suspension | unrelated_to_dismissal | high | 직장 내 괴롭힘 사실은 전제되지만 결론은 정직 1개월의 양정과 절차 적정성에 있음. |
| id_4055 | disciplinary_severity | workplace_harassment | suspension | unrelated_to_dismissal | high | 사실이 아닌 게시와 괴롭힘 행위가 징계사유이지만 핵심은 3월 정직의 양정 과다 여부에 있음. |
| id_405513 | disciplinary_severity | procedure, workplace_harassment | suspension | unrelated_to_dismissal | high | 괴롭힘과 기타 비위가 모두 인정되며 중징계와 절차 적법성이 함께 확인된 사건. |
| id_405553 | disciplinary_severity | workplace_harassment | reprimand | unrelated_to_dismissal | high | 공개적 모욕 발언이 괴롭힘으로 인정되지만 견책은 가장 경한 징계라 과도하지 않음. |
| id_405555 | disciplinary_severity | workplace_harassment | disciplinary_dismissal | - | high | 성희롱과 괴롭힘 재발, 과거 징계 이력을 고려해 징계해고가 유지된 사건. |
| id_405569 | disciplinary_severity | workplace_harassment | pay_cut | unrelated_to_dismissal | high | 직장 내 괴롭힘이 인정되고 감봉처분이 정당한지 판단한 사건. |
| id_405601 | disciplinary_severity | procedure, workplace_harassment | suspension | unrelated_to_dismissal | high | 관계의 우위성을 이용한 괴롭힘과 업무지시 불이행의 반복이 모두 인정된 사건. |
| id_405643 | transfer_validity | disciplinary_severity, workplace_harassment, procedure | pay_cut, transfer | unrelated_to_dismissal | high | 괴롭힘 피해자 분리조치와 별도 감봉의 양정 적정성을 함께 본 복합 인사명령 사건. |
| id_405659 | transfer_validity | procedure, workplace_harassment, harassment_report | transfer | unrelated_to_dismissal | high | 괴롭힘 신고를 계기로 한 인사배치의 업무상 필요성과 협의절차를 본 사건. |
| id_405819 | dismissal_validity | procedure, workplace_harassment | dismissal | - | high | 사직 수용 여부와 해고통지의 적법성이 함께 다뤄진 사건. |
| id_405847 | disciplinary_severity | procedure, workplace_harassment | disciplinary_dismissal | - | high | 반복적 괴롭힘이 근무질서를 심각하게 훼손하여 징계해고가 정당한 사건. |
| id_405851 | absence_without_leave | procedure | disciplinary_dismissal | not_really_harassment_case | high | 병가 증빙 없이 장기간 출근하지 않은 무단결근이 핵심이고 괴롭힘은 배경. |
| id_405901 | dismissal_validity | workplace_harassment | no_formal_disposition | resignation_dispute, unrelated_to_dismissal | high | 사직의사 제출 후 3개월이 지나 구제신청이 도과한 사건. |
| id_405915 | disciplinary_severity | procedure, workplace_harassment | disciplinary_dismissal | - | high | 성희롱과 괴롭힘 재발이 중징계 정당성을 뒷받침한 사건. |
| id_405921 | dismissal_validity | procedure, disciplinary_severity, workplace_harassment | disciplinary_dismissal | - | high | 괴롭힘 상태에서의 사직 철회와 징계해고, 그리고 징계절차 위법이 함께 문제된 사건. |
| id_405943 | transfer_validity | procedure, workplace_harassment | transfer | unrelated_to_dismissal | high | 괴롭힘 피해자 분리 목적의 인사발령이 생활상 불이익보다 정당하다고 본 사건. |
| id_406043 | dismissal_validity | misconduct, procedure, workplace_harassment | disciplinary_dismissal | - | high | 여러 징계사유 중 일부만 인정되더라도 남은 사유로 해고가 충분하다고 본 사건. |
| id_406049 | disciplinary_severity | evaluation, workplace_harassment, retaliation, unfair_treatment | pay_cut | unrelated_to_dismissal | medium | 직장 내 괴롭힘 관련 다자 징계 중 일부는 과다하고 일부는 정당한 복합 사건. |
| id_406075 | disciplinary_severity | procedure, workplace_harassment | suspension | unrelated_to_dismissal | high | 삿대질·고성·지시위반 등 괴롭힘 사안에서 정직 3개월이 정당한 사건. |
| id_406141 | disciplinary_severity | procedure, workplace_harassment | reprimand | unrelated_to_dismissal | high | 공연 배제와 지휘불복종이 괴롭힘과 징계사유로 인정된 사건. |
| id_406179 | work_ability | worker_status, evaluation, procedure, workplace_harassment, dismissal_validity | rejection_of_regular_employment | not_really_harassment_case, unrelated_to_dismissal, unrelated_to_harassment | high | 시용 평가의 공정성에 하자가 있어 본채용 거부가 부당하다고 본 사건. |
| id_406201 | workplace_harassment | - | reprimand | unrelated_to_dismissal | high | 언성 제고만으로는 직장 내 괴롭힘에 이르지 않아 견책 사유가 부정된 사건. |
| id_406271 | disciplinary_severity | procedure, workplace_harassment | suspension | unrelated_to_dismissal | high | 직장 내 성희롱과 괴롭힘 사안에서 징계사유와 절차가 모두 정당한 사건. |
| id_406273 | worker_status | - | no_formal_disposition | not_really_harassment_case, unrelated_to_dismissal, unrelated_to_harassment | high | 종속적 근로관계가 인정되지 않아 직장내괴롭힘 진정이 심리 대상이 되지 않은 사건. |
| id_40629 | disciplinary_severity | procedure | disciplinary_dismissal | not_really_harassment_case | high | 괴롭힘이나 왕따 기인으로 보기 어려운 비위에 대해 해고가 과중하다고 본 사건. |
| id_406305 | dismissal_validity | workplace_harassment | no_formal_disposition | resignation_dispute, unrelated_to_dismissal | high | 괴롭힘이 사직의 배경이지만 사직 철회가 없어 해고는 존재하지 않는 사건. |
| id_40633 | disciplinary_severity | misconduct, procedure, workplace_harassment | disciplinary_dismissal | - | high | 우울증과 갈등 상황이 배경이나 해고는 징계사유에 비해 과도하다고 본 사건. |
| id_406341 | procedure | workplace_harassment | reprimand | procedure_dominant, unrelated_to_dismissal | high | 직장 내 괴롭힘 일부와 경고의 절차 하자가 결론을 좌우한 사건. |
| id_406381 | disciplinary_severity | procedure, workplace_harassment | suspension | unrelated_to_dismissal | high | 직장 내 괴롭힘이 인정되고 정직의 양정과 절차가 모두 적정한 사건. |

## 메모

- 초안에서 `retaliation`과 `procedure`가 과잉으로 잡힌 몇 건을 `transfer_validity`, `disciplinary_severity`, `work_ability`로 재정렬했다.
- `405851`은 무단결근이 핵심이고 괴롭힘은 배경이라 `absence_without_leave`로 복원했다.
- `406179`는 시용 평가 공정성 문제이므로 `work_ability`와 `rejection_of_regular_employment`로 정리했다.
- `406273`는 근로자성 부정이 핵심이므로 `worker_status`로 재분류했다.
