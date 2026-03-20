# absence_batch_031_reviewed.jsonl 1차 self-review 메모

## 배치 요약
- 총 30건 처리
- 무단결근 핵심(absence_without_leave primary 또는 주요 secondary): 10건
- 무단결근 배경(not_really_absence_case): 16건
- 갱신기대권 중심(renewal_expectation_dominant): 2건 (id_347015, id_347267)
- 해고부존재: 3건 (id_346623, id_346995, id_347027)
- 절차위반 결정적(procedure_dominant): 2건 (id_346441, id_347181)

## 무단결근 핵심 사건 (absence_without_leave가 primary)
| case_id | 요지 | 처분 | 결과 |
|---------|------|------|------|
| id_346413 | 내용증명 후 장기결근 지속 | 정직1월 | 기각 |
| id_346525 | 1일 무계결근(승무원) | 견책 | 기각 |
| id_346583 | 장기 무단결근 직권면직 | 해고 | 기각 |
| id_346911 | 4일 무단결근 | 정직2주 | 기각 |
| id_347 | 28일 무단결근+폭언 | 해고 | 기각 |
| id_34723 | 10일+ 무단결근 직권면직 | 해고 | 기각 |

## 무단결근 배경 사건 (not_really_absence_case)
| case_id | 실질 쟁점 | 변경 이유 |
|---------|-----------|-----------|
| id_346381 | disciplinary_severity | 근무태만만 인정, 양정과다+절차위반이 핵심 |
| id_346479 | dismissal_validity | 산재요양기간 해고금지 위반이 핵심 |
| id_346507 | misconduct | 운수업 복합 비위(무정차·폭언 등) 핵심, 결근은 부수적 |
| id_34657 | misconduct | 노인학대·하극상이 핵심, 근무지이탈은 부수적 |
| id_346623 | dismissal_validity | 해고부존재(자진 기숙사 이탈) |
| id_346687 | misconduct | 근무태만(사건 미보고)이 핵심, 무단결근 무관 |
| id_346707 | misconduct | 향응수수·허위수리비가 핵심, 무단이탈 부수적 |
| id_346749 | disciplinary_severity | 동영상시청 등 근태불량(결근 아님), 양정과다 핵심 |
| id_346797 | disciplinary_severity | 근무태만만 인정, 양정과다 핵심 |
| id_346873 | worker_status | 일용근로자 지위 판단이 핵심 |
| id_346965 | misconduct | 음주 관련 복합 비위 핵심, 근태불량 부수적 |
| id_346995 | dismissal_validity | 해고부존재(사용자가 계속 근로 요청) |
| id_347015 | renewal_expectation | 갱신기대권 불인정이 핵심, 결근계는 부정 근거 중 하나 |
| id_347027 | dismissal_validity | 해고부존재(대기발령 출근명령 불응) |
| id_347147 | misconduct | 작업지시불이행·현장이탈이 핵심(무단결근과 다른 유형) |
| id_347267 | renewal_expectation | 갱신기대권+복합 사유, 근태불량은 일부 |

## 경계 판단 사건 (medium confidence)
| case_id | 이유 |
|---------|------|
| id_346751 | 야간근무거부+건강검진미이행+무단결근 복합. 무단결근 비중 상당하나 misconduct로 분류 |
| id_346845 | 직무태만+명령불복종+무단결근 복합. 무단결근 비중 상당하나 misconduct로 분류 |
| id_347069 | 무단결근+기밀유출. 기밀유출이 더 중대하나 무단결근도 독립 사유 |

## 특이사항
- id_34721: legacy에 absence 포함이나 실질은 "병원치료 위한 업무시간 중 무단외출"로 무단결근과 다름
- id_346873: 결근 자유로움이 일용직 판단의 근거로 사용됨 (역설적)
- id_346995: 근로계약서에 "무단결근 2회 이상 시 사직의사 간주" 조항 존재하나 해고 의사표시 부재
- id_347239: 갱신기대권+무단결근+징계해고까지 진행된 복합 사건
