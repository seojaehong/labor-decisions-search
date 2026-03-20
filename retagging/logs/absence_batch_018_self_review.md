# absence_batch_018 Self-Review

## 배치 개요
- **입력**: 30건 (id_25349 ~ id_26221)
- **출력**: 30건 전량 태깅 완료
- **작업일**: 2026-03-20

## 무단결근 핵심 vs 배경 분류

### 핵심 결근 사례 (absence_without_leave / attendance가 primary) — 8건
| case_id | 요약 | primary |
|---------|------|---------|
| id_25375 | 9개월 83회 상습 지각, 해고 정당 | attendance |
| id_25605 | 장기 무단결근이나 폭행 피해 배경, 양정 과다 | absence_without_leave |
| id_25633 | 근무지 무단이탈+5부제 위반, 강직 양정 과다 | absence_without_leave |
| id_25777 | 임신 중 휴직 불승인 후 무단결근, 양정 과다 | absence_without_leave |
| id_25789 | 질병(급성 현기증) 결근, 무단결근 불인정 | absence_without_leave |
| id_25993 | 100일 이상 무단결근, 직권면직 정당 | absence_without_leave |
| id_26221 | 5일 이상 무단결근, 징계해고 정당 | absence_without_leave |

### 배경 결근 사례 (not_really_absence_case) — 23건
| case_id | 실질 primary | 배경 판단 근거 |
|---------|-------------|---------------|
| id_25349 | misconduct | 업무지시 불이행이 주, 무단이탈은 복합 비위 중 일부 |
| id_25399 | dismissal_validity | 당사자 적격+서면통지 위반이 핵심, 무단이탈은 정황 |
| id_25417 | disciplinary_severity | 인사규정 적용 오류가 핵심, 무단이탈은 경미한 새 비위 |
| id_25423 | dismissal_validity | 시용해고 정당성이 핵심, 무단결근은 다수 사유 중 하나 |
| id_25445 | dismissal_validity | 해고 철회+구제이익 소멸이 핵심, 결근은 자발적 미출근 |
| id_25457 | dismissal_validity | 파견근로 해고 존부가 핵심, 결근은 자발적 출근거부 |
| id_25485 | dismissal_validity | 사직 vs 해고 구분이 핵심, 사직서 제출 후 미출근 |
| id_25503 | dismissal_validity | 해고 즉시 철회 후 자발적 미출근, 해고 부존재 |
| id_25517 | disciplinary_severity | 무단결근은 업무상 부상 기인으로 불인정, 양정 과다 |
| id_25565 | procedure | 구두 해고 서면통지 위반이 핵심, 결근은 해고 후 미출근 |
| id_25573 | dismissal_validity | 숙소 불만으로 자발적 미출근, 해고 부존재 |
| id_2559 | procedure | 임금체불·장비미제공 원인 결근, 징계절차 하자 핵심 |
| id_25603 | disciplinary_severity | 지각 4회는 부수, 양정 과다가 핵심 |
| id_2563 | disciplinary_severity | 조기퇴근 1회만 인정, 산재 배경·초범 양정 과다 |
| id_25651 | misconduct | 성희롱 사건 조작·허위보고가 핵심, 결근은 불인정 |
| id_25655 | dismissal_validity | 무단결근+배임 모두 입증 부족 |
| id_25689 | dismissal_validity | 사직권고 수용 합의해지, 결근 전력은 정황 |
| id_25727 | dismissal_validity | 무단결근 후 퇴직 의사 추정, 해고 부존재 |
| id_25883 | dismissal_validity | 수습 본채용 거부 정당성 핵심, 무단결근 5일은 사유이나 불인정 |
| id_2591 | misconduct | 성희롱+괴롭힘이 핵심, 근태불량은 복합 비위 일부 |
| id_2599 | disciplinary_severity | 배차 지시 불이행이 주, 근무태만은 입증 안됨 |
| id_25991 | disciplinary_severity | 업무지시 거부가 주, 무단지각 3회는 부수 |
| id_2621 | disciplinary_severity | 배차지시 불이행이 주, 지각 1회 결행은 부수 |

## 통계
- **핵심 결근**: 8건 (26.7%)
- **배경 결근**: 23건 (73.3%) — 전체에 not_really_absence_case 부여 (id_25375 제외, attendance primary)
- **해고 부존재/사직 쟁점**: 8건 (id_25445, id_25457, id_25485, id_25503, id_25573, id_25689, id_25727, id_25883 일부)
- **양정 과다**: 10건
- **절차 위반**: 3건 (id_25399, id_25565, id_2559)

## 판단 난이도 높았던 건
| case_id | 쟁점 | 판단 |
|---------|------|------|
| id_25605 | 무단결근이 핵심이나 폭행 피해 배경 — absence vs disciplinary_severity | absence primary 유지: 무단결근 자체의 정당성이 핵심 쟁점이고 양정 과다는 결론 |
| id_25789 | 무단결근 해당 여부 자체가 쟁점 — absence vs dismissal_validity | absence primary 유지: 무단결근 해당 여부 판단이 직접 쟁점 |
| id_25883 | 무단결근 5일이 사유이나 수습해고 맥락 — absence vs dismissal_validity | dismissal_validity: 수습해고 사회통념 상당성이 상위 쟁점 |
| id_25655 | 무단결근이 해고사유이나 입증 부족 — absence vs dismissal_validity | dismissal_validity: 사용자 입증 실패가 핵심 |

## 품질 체크
- [x] 전 건 confidence 부여
- [x] exclusion_flags 일관성 확인
- [x] include/exclude_for_queries 작성
- [x] industry_context 추론 가능한 건 반영 (healthcare, transport, finance, service, construction, public)
- [x] disposition_type 정확성 확인 (직권면직→disciplinary_dismissal, 강직→demotion, 감봉→pay_cut)
