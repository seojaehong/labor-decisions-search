# absence_batch_010_reviewed.jsonl 1차 self-review 메모

## 통계 요약
- 총 건수: 30건
- 진정한 무단결근/결근 사례 (exclusion_flags 없음): 9건
- not_really_absence_case 플래그 부여: 18건
- resignation_dispute만 부여 (결근 배경이나 퇴직 존부 쟁점): 2건
- 양정 과다이나 결근이 인정 사유인 경우 (exclusion_flags 없음): 1건

## 진정한 무단결근 핵심 사례 (9건)

### id_18465
- primary: absence_without_leave / disposition: ['dismissal']
- 출근명령 거부 + 무단결근 → 해고 정당
- 본부장 직책의 높은 책임이 양정 판단에 반영

### id_18483
- primary: absence_without_leave / disposition: ['suspension']
- 승인 없는 결근 → 정직 5일 정당, 부당노동행위 아님

### id_18509
- primary: absence_without_leave / disposition: ['suspension']
- 보고 없이 3일 결근 → 정직 양정 과다 + 절차 하자

### id_18613
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 상병유급결근 요건 미충족 80일 무단결근 → 해고 정당
- 장기 무단결근 대표 사례

### id_18637
- primary: absence_without_leave / disposition: ['dismissal']
- 질병 장기결근으로 근로제공의무 미이행 → 해고 정당
- 병가 5일 한도 초과, 의료기관 특성

### id_18933
- primary: absence_without_leave / disposition: ['suspension', 'dismissal']
- 전직발령 불응 → 무단결근 → 정직 → 계속 불응 → 해고
- 단계적 징계 진행의 모범 사례

### id_18915
- primary: disciplinary_severity / disposition: ['dismissal']
- 배차시간 미준수·무단결근·수입금 지연입금 등 복합 사유, 양정 과다
- 예비기사 복무관리 부재가 참작

### id_19037
- primary: disciplinary_severity / disposition: ['suspension', 'demotion']
- 무단결근 3회 인정, 정직 4월 양정 과다 / 강등은 정당

### id_19063
- primary: attendance / disposition: ['suspension']
- 근무지 무단이탈 7차례·경고 6회 → 정직 30일 정당

## resignation_dispute 플래그 사례 (2건)

### id_18893 — 무단결근 반복 후 사직서 제출, 강요 아닌 합의해지
### id_18753 — 결근 후 기숙사 퇴거·타사 이직, 자발적 퇴직 인정

## not_really_absence_case 부여 사례 (18건)

### id_18409 — 차량사고 은폐·업무지시 불이행이 핵심, 무단결근은 명시적 불인정
### id_18429 — 지각·절차위반 휴가가 핵심, 무단결근이 아님
### id_18473 — 결근 배경이나 해고 존부 + 서면통지 절차위반이 핵심
### id_18519 — 무단결근 주장 배척, 전직발령 정당성이 핵심
### id_18541 — 허위민원·동료 협박이 핵심, 배차결행은 부수 사유
### id_18567 — 이력서 허위기재·수입금 미납·폭언이 핵심, 결근일 영업은 부수
### id_1861 — 품위유지 위반(부적절한 관계)이 주된 핵심, 무단결근은 부수
### id_18619 — 해고 존부 + 서면통지 절차위반이 핵심
### id_18667 — 사직의사 진정성(해고 존부)이 핵심, 결근은 배경
### id_1867 — 무단결근 불인정, 휴대전화·지각의 양정 과다가 핵심
### id_18685 — 징계절차(단체협약) 위반이 핵심, 결근은 징계사유이나 절차가 지배
### id_18697 — 해고사유 입증 부족, 결근은 입증되지 않은 해고 명목
### id_18811 — 상사 언쟁 양정 과다가 핵심, 근무태만 불인정
### id_18817 — 단체협약 해석 견해제시 사건, 결근은 비교 개념
### id_1887 — 근로시간면제 무단결근 '처리'의 법적 성격이 쟁점
### id_18939 — 사용자 귀책 무계결근에 대한 반복 과잉징계 + 부당노동행위
### id_18983 — 성희롱 발언이 핵심, 근무태만 불인정
### id_18995 — 양정 과다 + 징계위원장 제척 위반이 핵심

## 판단 근거 정리

| 구분 | 기준 |
|------|------|
| 진정한 결근 사례 | 무단결근/출근거부 자체가 징계사유의 핵심이거나 유일한 인정 사유 |
| not_really_absence_case | 무단결근이 (1) 배경사실에 불과, (2) 징계사유로 불인정, (3) 다른 쟁점이 결론을 지배 |
| resignation_dispute | 결근 상태가 사직/해고 존부 판단의 배경이나 결근 '징계'가 아닌 경우 |

## 주의 사항
- id_18465: 출근명령 거부가 수반된 무단결근이므로 misconduct와 결합하나, 결근 자체가 핵심이므로 primary=absence_without_leave
- id_18933: 전직발령 정당성이 선결 쟁점이나, 전직발령이 정당하다고 인정된 이상 무단결근이 직접 징계사유이므로 primary=absence_without_leave
- id_18637: 질병에 의한 결근이지만 업무상 질병이 아니고 병가 한도 초과이므로 absence_without_leave로 태깅
- id_18817: 유일한 비해고 사건(단체협약 해석 견해제시). unrelated_to_dismissal 플래그 부여
- id_18939: 무계결근 원인이 사용자 귀책이므로 not_really_absence_case 부여. 반복 보복징계·부당노동행위가 핵심
- id_19037: 정직 4월 vs 강등의 이분 판정. 무단결근이 인정 사유이므로 exclusion_flags 미부여
- id_18915: confidence=medium — 무단결근이 사유 중 하나이나 예비기사 복무관리 미비 등 참작사유 다수
