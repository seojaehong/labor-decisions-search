# absence_batch_006 Self-Review

## 기본 정보
- 입력: `input/batches/absence_batch_006.jsonl`
- 출력: `output/reviewed/absence_batch_006_reviewed.jsonl`
- 처리 건수: 30건
- 처리 일시: 2026-03-20

## 분류 요약

### 핵심 결근 사건 (결근이 실제 핵심 쟁점) — 7건
| case_id | primary | 비고 |
|---------|---------|------|
| id_15319 | disciplinary_severity | 무단결근 10일, 양정 과다 |
| id_15433 | dismissal_validity | 무단결근 후 고용변동신고 = 해고 아님 |
| id_15687 | absence_without_leave | 규정위반 병가를 무단결근으로 인정, 해고 정당 |
| id_15705 | absence_without_leave | 한 달 무단결근, 해고 정당 |
| id_16057 | disciplinary_severity | 병가 불승인 후 결근 → 해고 양정 과다 |
| id_16101 | absence_without_leave | 무단결근 10일, 감봉 정당 |
| id_16183 | disciplinary_severity | 미승인 휴가 사용 = 무단결근, 정직 양정 과다 |

### 결근이 복합 비위의 일부 — 5건
| case_id | primary | 비고 |
|---------|---------|------|
| id_15519 | misconduct | 무단이탈+용접봉 오사용+근태불량 |
| id_15623 | transfer_validity | 부당전보 불응 → 결근 → 해고 |
| id_16145 | misconduct | 특수경비원 결근+총기방치 등 |
| id_15949 | renewal_expectation | 결근 8일이 갱신거절 평가요소 중 하나 |
| id_15977 | disciplinary_severity | 지각7+결근1에 정직3월 과다 |

### 결근이 배경사실 (not_really_absence_case) — 18건
| case_id | primary | 실질 쟁점 |
|---------|---------|-----------|
| id_15331 | unfair_treatment | 부당노동행위(지배개입) |
| id_15389 | misconduct | 폭행·모욕 등 복합 비위 |
| id_15419 | disciplinary_severity | 욕설·이탈 양정 과다 |
| id_15439 | procedure | 제척기간 도과 각하 |
| id_15627 | dismissal_validity | 해고부존재 |
| id_15763 | dismissal_validity | 사직 의사표시 해석 |
| id_1579 | procedure | 소명기회 미부여 절차 하자 |
| id_15829 | misconduct | 운수업 운행질서 위반 |
| id_15837 | misconduct | 상사 폭행(전치3주) |
| id_15849 | unfair_treatment | 부당노동행위 |
| id_15881 | procedure | 구두해고 절차 부당 |
| id_15945 | disciplinary_severity | 경비 사적사용, 결근 입증 부족 |
| id_16067 | dismissal_validity | 구제이익 소멸 |
| id_16069 | misconduct | 허위민원·협박 등 복합 비위 |
| id_16105 | disciplinary_severity | 이석횟수 징계사유 불인정 |
| id_1611 | workplace_harassment | 괴롭힘·성희롱 |
| id_16121 | dismissal_validity | 수습 해고 부당 |
| id_16177 | disciplinary_severity | 복직 후 재해고 양정 부당 |

## 핵심 판단 근거

### 결근 핵심 vs 배경 구분 기준
1. 결근이 **유일하거나 주된 징계사유**이고 판정에서도 결근을 중심으로 판단 → 핵심
2. 결근이 **다수 비위 중 하나**이고 폭행·성희롱·부당노동행위 등이 결론을 좌우 → 배경
3. 결근이 **입증 부족으로 징계사유 불인정** → 배경 (not_really_absence_case)
4. 결근이 **부당한 처분(전보·병가불승인)에 기인** → 결근 자체가 쟁점이면 핵심

### 특이 사례
- **id_15623**: 부당전보 불응으로 인한 결근 → transfer_validity가 primary이나 결근 검색에도 유의미 (exclusion 미부여)
- **id_16057**: 병가 불승인 후 결근을 무단결근으로 간주 → 결근 검색 핵심 사례
- **id_15433**: 무단결근 자체는 사실이나 고용변동신고의 해고 해당 여부가 쟁점
- **id_16145**: 특수경비원 직무 특성상 결근 자체가 중대 → misconduct primary이나 exclusion 미부여

## 통계

| 항목 | 수 |
|------|---|
| 총 건수 | 30 |
| 결근 핵심 | 7 (23%) |
| 결근 복합 비위 일부 | 5 (17%) |
| 결근 배경 (exclusion 부여) | 18 (60%) |
| confidence high | 30 |
| confidence medium | 0 |

## 품질 체크
- [x] 모든 case_id가 입력과 일치
- [x] exclusion_flags에 not_really_absence_case 적절 부여 (18건)
- [x] 핵심 결근 사건에 unauthorized_absence/repeated_absence fact_marker 부여
- [x] 절차위반 핵심 사건에 procedure primary 부여 (id_15439, id_1579, id_15881)
- [x] 해고부존재 사건 적절 처리 (id_15433, id_15627, id_15763, id_16067)
- [x] tag_version: v1, review_status: pending 전건 확인
