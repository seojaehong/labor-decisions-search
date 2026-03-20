# incompetence_batch_007_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, legacy_reason_category에 "incompetence" 포함
- 핵심 구분 기준: work_ability(업무능력 자체가 쟁점) vs dismissal_validity(해고 유효성이 쟁점) vs 기타

## 분류 통계

| issue_type_primary | 건수 | case_id 목록 |
|---|---|---|
| work_ability | 20 | id_404325, id_404373, id_40493, id_405407, id_405631, id_405781, id_40647, id_406591, id_407385, id_407443, id_407621, id_407691, id_407897, id_408663, id_409849, id_40993, id_41003, id_410161, id_410631(→low_sales 변경) |
| low_sales | 1 | id_410631 |
| dismissal_validity | 3 | id_406951, id_408529, id_409031 |
| disciplinary_severity | 3 | id_405393, id_408777, id_409397 |
| procedure | 1 | id_40571 |
| harassment_report | 2 | id_408207, id_408599 |
| renewal_expectation | 2 | id_407971, id_410055 |

## 갱신기대권 혼입 사례 (exclusion 처리)

### id_407971
- primary: renewal_expectation
- exclusion_flags: ['renewal_expectation_dominant', 'not_really_performance_case']
- 사유: 시용계약 성격의 기간제 근로계약 만료 → 구제이익 부정. 업무능력 부족은 legacy 태그에만 존재하며 실제 판단 쟁점이 아님.

### id_410055
- primary: renewal_expectation
- exclusion_flags: ['renewal_expectation_dominant', 'not_really_performance_case']
- 사유: 기간제 갱신기대권이 핵심. 사용자가 업무능력 부족을 주장했으나 근무평정 자체를 미실시하여 판단 불가.

## incompetence 배치 부적절 사례 (exclusion 처리)

### id_408207 / id_408599 (동일 사건 초심/재심)
- primary: harassment_report
- exclusion_flags: ['not_really_performance_case', 'unrelated_to_dismissal']
- 사유: 성희롱 신고에 대한 보복적 전보·대기발령 여부가 핵심. 업무능력 부족은 사직 권고 배경의 일부에 불과.

### id_409397
- primary: disciplinary_severity
- exclusion_flags: ['not_really_performance_case']
- 사유: 폭언·욕설이 핵심 징계사유. 근태관리 부적정은 해고사유로도 인정 불가. 인사위원회 구성 하자가 결정적.

## work_ability vs dismissal_validity 구분 판단

### work_ability로 분류한 기준
- 수습/시용 본채용 거부 사례에서 **평가의 합리성·객관성이 중심 쟁점**인 경우 → work_ability
- 업무능력 부족 자체의 존부가 다투어지는 경우 → work_ability

### dismissal_validity로 분류한 기준
- 업무능력 부족이 **복수 해고사유 중 하나**이고 해고 자체의 유효성(사유 종합판단, 절차)이 핵심인 경우 → dismissal_validity
- 기간제 교원 계약해지(id_406951): 업무태만+능력부족+복무위반 종합 → 해고 유효성
- 정규직 전환 후 해고(id_408529): 수습기간 종료 후 정규직인데 수습평가로 해고 → 해고 유효성
- 권고사직 거부 후 해고(id_409031): 사유 추상적+입증 부족 → 해고 유효성

### procedure로 분류한 사례
- id_40571: 시용기간 삭제된 새 계약 체결 → 정규직인데 인사위원회 미경유 해고. 절차 위반이 결정적.

## 특이 사례 메모

### id_405407
- 상시근로자 5인 이상 여부(사업장 동일성) 선결 쟁점 포함. 두 회사를 하나의 사업장으로 인정.

### id_410631
- primary를 low_sales로 변경. 상담실장 경력직 채용, 매출 기준 사전 고지, 다른 상담실장 대비 현저 저조.
- 기존 incompetence 배치는 적절하나 태그 레벨에서는 low_sales가 더 정확.

### id_40993
- 금전보상명령 수용 사례. 원직복직 갈음.

## disposition_type 분포
- rejection_of_regular_employment: 20건 (수습 본채용 거부)
- dismissal: 5건
- disciplinary_dismissal: 2건
- contract_termination: 1건
- nonrenewal: 2건
- transfer: 2건 (차별시정)
- pay_cut: 1건

## 잔여 검토 필요 사항
- id_405631과 id_409849는 동일 사건(재심/초심)으로 추정. 과학실무사, 장애인 채용. 양쪽 모두 유지.
- id_408207과 id_408599는 동일 사건(초심/재심). 양쪽 모두 유지하되 incompetence 배치 부적절 플래그.
