# violence_batch_032_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, legacy_reason_category에 "violence" 포함 사건
- 중점 판단: misconduct vs disciplinary_severity 구분

## misconduct vs disciplinary_severity 판단 기준
- **misconduct**: 비위행위 사실 자체의 인정/불인정이 핵심 쟁점이거나, 비위사실이 중대하여 그 자체로 해고를 정당화하는 경우
- **disciplinary_severity**: 비위사실은 인정되나 양정(처분 수위)의 과다 여부가 핵심 쟁점인 경우

## violence 배치이나 실질 쟁점이 다른 사건 (6건)

### id_350315
- primary: dismissal_validity (해고부존재)
- 변경 이유: 폭행·폭언이 쟁점이 아니라 자발적 사직 여부가 핵심. 사용자의 폭행·폭언·사직 종용이 확인되지 않음.

### id_350961
- primary: renewal_expectation
- 변경 이유: 폭행과 전혀 무관한 기간제 갱신기대권 부정 사건. violence 태그는 legacy 오류.

### id_351101
- primary: dismissal_validity (해고부존재)
- 변경 이유: 성희롱 해임 회피 목적 자발적 사직, 폭행과 무관.

### id_351219
- primary: unfair_treatment (부당노동행위)
- 변경 이유: 피케팅·옥외집회에 대한 보복소송이 핵심. 폭력 행사 사실 없음.

### id_350829
- primary: procedure
- 변경 이유: 대기발령 전 인사위원회 의결 누락이 핵심 절차 쟁점.

### id_350887
- primary: procedure
- 변경 이유: 시용기간 해고의 서면통지 하자(구체적 사유 미기재)가 핵심.

## misconduct로 분류 (6건)

### id_350431
- primary: misconduct / disposition: disciplinary_dismissal
- 사유: 사내 폭행 사실 인정이 핵심, 양정은 부수적

### id_350709
- primary: misconduct / disposition: disciplinary_dismissal
- 사유: 자료 무단열람+위력행사+폭언 복합 비위, 사실 인정이 핵심

### id_350751
- primary: misconduct / disposition: disciplinary_dismissal
- 사유: 성희롱+폭언+음주 복합 비위, 반복성으로 misconduct 자체가 중대

### id_350789
- primary: misconduct / disposition: dismissal
- 사유: 비위행위 입증 부족이 핵심(사실 인정 문제)

### id_351021
- primary: misconduct / disposition: disciplinary_dismissal
- 사유: 폭행 사실 인정이 핵심, 단체협약상 사유불문 해고 규정

### id_35131
- primary: misconduct / disposition: disciplinary_dismissal
- 사유: 성희롱+폭행+경비부정 복합 비위, 사안 중대성이 핵심

### id_351147
- primary: misconduct / disposition: dismissal
- 사유: 폭행·위협 입증 부족이 핵심(사실 인정 문제)

### id_350625
- primary: misconduct / disposition: suspension
- 사유: 공금 횡령이 핵심, 괴롭힘은 불인정. violence 배치이나 실질은 횡령.

## disciplinary_severity로 분류 (12건)

### id_350349
- primary: disciplinary_severity / disposition: dismissal
- 사유: 괴롭힘 징계에서 양정 적정성이 주된 판단

### id_350469
- primary: disciplinary_severity / disposition: pay_cut
- 사유: 폭행 인정되나 감봉 양정 적정성이 핵심

### id_350497
- primary: disciplinary_severity / disposition: disciplinary_dismissal
- 사유: 전력 가중징계 여부가 양정 판단의 핵심

### id_35081
- primary: disciplinary_severity / disposition: suspension
- 사유: 택시기사 폭행 인정되나 정직 50일 양정 과다

### id_350869
- primary: disciplinary_severity / disposition: demotion
- 사유: 폭행 불인정→우발적 접촉만 인정, 강격 양정 과다

### id_350935
- primary: disciplinary_severity / disposition: demotion
- 사유: 폭행 인정되나 선행 괴롭힘 피해 고려 시 강등 과다

### id_350971
- primary: disciplinary_severity / disposition: disciplinary_dismissal
- 사유: 혼잣말 욕설+개발 지연, 해고 양정 과다

### id_351113
- primary: disciplinary_severity / disposition: pay_cut
- 사유: 반복 폭언 인정, 전력 감안 감봉 적정

### id_351169
- primary: disciplinary_severity / disposition: suspension
- 사유: 폭행·욕설 인정, 해고→정직 감경의 양정 적정성

### id_351221
- primary: disciplinary_severity / disposition: suspension
- 사유: 폭행 유죄확정이나 정직 양정 과다

### id_351301
- primary: disciplinary_severity / disposition: suspension
- 사유: 욕설+자산 무단반출, 유사사례 형평성 검토

### id_351303
- primary: disciplinary_severity / disposition: suspension, pay_cut
- 사유: 피켓·구호 징계, 정직 과다/감봉 적정(일부 인용)

### id_35133
- primary: disciplinary_severity / disposition: disciplinary_dismissal
- 사유: 비위 인정되나 해고 양정 과다

## workplace_harassment로 분류 (2건)

### id_350459
- primary: workplace_harassment / disposition: suspension
- 사유: 팀장의 직장내 괴롭힘(폭언·업무전가) 자체가 핵심 쟁점

### id_350985
- primary: workplace_harassment / disposition: disciplinary_dismissal
- 사유: 센터장의 다수 피해자·장기 괴롭힘이 핵심 쟁점

## 기타 분류 (2건)

### id_35107
- primary: disciplinary_severity / disposition: suspension
- 사유: 폭언+성희롱 복합, 양정 적정성이 핵심

## 통계 요약
| primary | 건수 |
|---------|------|
| disciplinary_severity | 12 |
| misconduct | 8 |
| workplace_harassment | 2 |
| dismissal_validity | 2 |
| procedure | 2 |
| renewal_expectation | 1 |
| unfair_treatment | 1 |
| **합계** | **30** (중복: id_35107은 disciplinary_severity에 포함) |

## 주의사항
- violence 배치에서 6건(20%)은 폭행·폭언이 실질 쟁점이 아닌 사건 → exclusion_flags 적용
- misconduct vs disciplinary_severity 경계 사건: 폭행 사실이 인정되면서 양정도 쟁점인 경우, "양정이 핵심 판단"이면 disciplinary_severity, "비위사실 자체가 중대하여 양정은 부수적"이면 misconduct로 분류
