# absence_batch_008 Self-Review

## 기본 정보
- 입력: `input/batches/absence_batch_008.jsonl`
- 출력: `output/reviewed/absence_batch_008_reviewed.jsonl`
- 처리 건수: 30건
- 처리 일시: 2026-03-20

## 분류 요약

### 핵심 결근 사건 (결근이 실제 핵심 쟁점) -- 7건
| case_id | primary | 비고 |
|---------|---------|------|
| id_17081 | absence_without_leave | 산재요양 종결 후 3개월 무단결근, 해고 정당 |
| id_17201 | absence_without_leave | 버스운전기사 무단결근+과속, 해고 정당 |
| id_17329 | absence_without_leave | 외국인근로자 무단이탈 부인, 해고 부당 |
| id_17617 | absence_without_leave | 무단결근 인정되나 양정 과다+절차 위반, 해고 부당 |
| id_17653 | absence_without_leave | 결근 40일+조퇴 73회, 양정 과다로 해고 부당 |
| id_17703 | absence_without_leave | 무단결근 6일+횡령, 양정 과다로 해고 부당 |
| id_17735 | absence_without_leave | 직책자 무단조퇴+이탈 10회 이상, 해고 정당 |

### 결근이 복합 비위의 일부 또는 해고 존부 관련 -- 5건
| case_id | primary | 비고 |
|---------|---------|------|
| id_17679 | dismissal_validity | 외국인근로자 무단이탈 + 고용변동 신고=해고 아님 |
| id_17809 | misconduct | 무단결근+폭행+노트북 반출 병렬 사유, 해고 정당 |
| id_17407 | misconduct | 승무거부가 핵심, 과거 결근은 징계전력으로 고려 |
| id_17343 | dismissal_validity | 근태불량 입증 부족, 해고사유 불인정 |
| id_17647 | dismissal_validity | 무단외출 입증 부족, 해고사유 불인정 |

### 결근이 배경사실 (not_really_absence_case) -- 18건
| case_id | primary | 실질 쟁점 |
|---------|---------|-----------|
| id_17003 | performance | 영업실적 저조 징계 부당 (결근 무관) |
| id_17097 | disciplinary_severity | 지각 등 일부 인정, 양정 과다+절차 하자 |
| id_17117 | dismissal_validity | 해고부존재 (사직 권유, 결근 무관) |
| id_17247 | disciplinary_severity | 무단이탈 6회 포함 복합 비위, 양정 과다 |
| id_17275 | dismissal_validity | 수습기간 본채용 거부 (복합 비위) |
| id_17297 | dismissal_validity | 수습기간 근태불량 해고 (복합 비위) |
| id_17303 | misconduct | 직무태만+허위신고 (결근 무관) |
| id_17341 | disciplinary_severity | 법인카드 부정사용, 양정 과다 |
| id_17367 | disciplinary_severity | 사용자 폭행 후 입원 결근, 양정 과다 |
| id_17375 | unfair_treatment | 부당노동행위 (출근정지 후 결근 처리) |
| id_17433 | dismissal_validity | 사직서 자유의사 합의해지 (결근 무관) |
| id_17439 | misconduct | 성희롱 징계해고 (피해자 결근은 간접증거) |
| id_175 | misconduct | 예술단원 복무규정 위반 견책 |
| id_17501 | dismissal_validity | 수습 본채용 거부+지배개입 |
| id_17557 | misconduct | 폭언+업무지시 거부 해고 정당 |
| id_17631 | disciplinary_severity | 합창단 복합 비위, 해촉 양정 과다 |
| id_17709 | dismissal_validity | 사실상 해고, 서면통보 미비 |
| id_17837 | disciplinary_severity | 폭행+협박 복합 비위, 양정 과다 |

## 핵심 판단 근거

### 결근 핵심 vs 배경 구분 기준
1. 결근이 **유일하거나 주된 징계사유**이고 판정에서도 결근을 중심으로 판단 -> 핵심
2. 결근이 **다수 비위 중 하나**이고 폭행/명예훼손/성희롱 등이 결론을 좌우 -> 배경
3. 결근이 **입증 부족으로 징계사유 불인정** -> 배경 (not_really_absence_case)
4. 결근이 **사용자의 부당한 처분에 기인** (폭행으로 입원, 출근정지 명령 등) -> 배경
5. 결근 사실은 있으나 **해고 존부가 핵심 쟁점** -> dismissal_validity primary
6. source_text에 **결근 관련 내용 자체가 없는 경우** -> 완전 배경

### 특이 사례
- **id_17003**: holding_points에는 결근 관련 없고 source_text에도 없음. legacy 태그 오분류.
- **id_17117**: holding_points에 "장기간 결근"이 언급되나 source_text에서는 임금체불/사직 문제만 다룸. holding_points가 source_text와 불일치.
- **id_17329**: 무단이탈 존부 자체가 핵심 쟁점. 결근이 아님을 판정하여 해고 부당. 결근 검색에 핵심적.
- **id_17375**: 출근정지를 명령해놓고 무단결근으로 해고. 결근의 원인이 사용자에게 있으므로 배경.
- **id_17439**: 피해주장자의 다음 날 결근은 성희롱 피해 개연성의 간접증거로만 사용됨.
- **id_17653**: 결근 40일+조퇴 73회로 수치적으로 상당하나, 외부 업무 특성/관리 소홀로 양정 과다 판정.

### 통계
- 결근 핵심 사건: 7건 (23.3%)
- 결근 복합/해고존부 관련: 5건 (16.7%)
- 결근 배경(not_really_absence_case): 18건 (60.0%)
- 해고 정당(기각): 14건 / 해고 부당(인용): 14건 / 해고부존재: 2건
