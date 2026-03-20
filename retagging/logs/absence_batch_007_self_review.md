# absence_batch_007 Self-Review

## 기본 정보
- 입력: `input/batches/absence_batch_007.jsonl`
- 출력: `output/reviewed/absence_batch_007_reviewed.jsonl`
- 처리 건수: 30건
- 처리 일시: 2026-03-20

## 분류 요약

### 핵심 결근 사건 (결근이 실제 핵심 쟁점) — 7건
| case_id | primary | 비고 |
|---------|---------|------|
| id_16387 | absence_without_leave | 무단결근 25일+과거 징계전력, 해고 정당 |
| id_16487 | absence_without_leave | 근로시간면제자 무단결근, 근신 정당 |
| id_16515 | absence_without_leave | 파업 참여 무단이탈, 출근정지 정당 |
| id_16633 | absence_without_leave | 산재요양 종결 후 2개월 결근, 해고 정당 |
| id_16659 | absence_without_leave | 영업직 자택체류 근무태만, 해고 정당 |
| id_16667 | absence_without_leave | 경비원 무단결근+투서, 정직 정당 |
| id_16943 | absence_without_leave | 버스 집단 결행, 정직 정당 |

### 결근이 복합 비위의 일부 또는 전보 관련 — 7건
| case_id | primary | 비고 |
|---------|---------|------|
| id_16321 | transfer_validity | 전근발령 거부 → 무단결근 → 해고 정당 |
| id_16351 | dismissal_validity | 무단결근 + 해고부존재 |
| id_16365 | dismissal_validity | 무단결근 + 해고부존재 |
| id_16571 | transfer_validity | 전직발령 불응 → 결근 → 해고 정당 |
| id_16673 | dismissal_validity | 무단결근 + 합의해지(해고부존재) |
| id_16855 | transfer_validity | 부당전보 거부 → 결근 → 정직 부당 |
| id_16921 | transfer_validity | 전보 불응 → 무단이탈 → 해고 정당 |
| id_17001 | dismissal_validity | 무단결근 + 해고부존재 |

### 결근이 배경사실 (not_really_absence_case) — 16건
| case_id | primary | 실질 쟁점 |
|---------|---------|-----------|
| id_1619 | disciplinary_severity | 지각·조기퇴근 양정 과다 (결근 불인정) |
| id_16205 | disciplinary_severity | 쟁의행위 차량사용 양정 과다 |
| id_16229 | disciplinary_severity | 병원 복합 비위 양정 과다 |
| id_16301 | disciplinary_severity | 폭언·비방, 무기정직 양정 과다 |
| id_16389 | dismissal_validity | 사직서 강요, 사실상 해고 |
| id_16401 | misconduct | 운수업 복합 비위(운송수입금 등) |
| id_16541 | dismissal_validity | 수습기간 부적격 해고 |
| id_16621 | disciplinary_severity | 직무태만 무기정직 양정 과다 |
| id_16653 | renewal_expectation | 정규직 전환 기대권 |
| id_16693 | disciplinary_severity | 복합 비위 양정 과다 |
| id_16743 | dismissal_validity | 사직서 강요, 사실상 해고 |
| id_16745 | misconduct | 근무태만·명예훼손 복합 비위 |
| id_16845 | transfer_validity | 강임(인사명령) 정당성 |
| id_16869 | disciplinary_severity | 경미 근태 감봉 양정 과다 |
| id_16905 | misconduct | 업무차량 무단사용 견책 |

## 핵심 판단 근거

### 결근 핵심 vs 배경 구분 기준
1. 결근이 **유일하거나 주된 징계사유**이고 판정에서도 결근을 중심으로 판단 → 핵심
2. 결근이 **다수 비위 중 하나**이고 폭행·명예훼손·부당노동행위 등이 결론을 좌우 → 배경
3. 결근이 **입증 부족으로 징계사유 불인정** → 배경 (not_really_absence_case)
4. 결근이 **부당한 처분(전보)에 기인** → 전보 정당성이 선결문제이면 transfer_validity primary, exclusion 미부여
5. 결근 사실은 있으나 **해고 존부가 핵심 쟁점** → dismissal_validity primary, exclusion 미부여

### 특이 사례
- **id_16487**: 근로시간면제자(타임오프)의 무단결근 — 면제시간 기산점 미합의 상황에서도 출퇴근 사규는 적용된다는 특수 판정
- **id_16515**: 불법파업 참여를 위한 무단이탈이 직접 징계사유 — 쟁의행위 적법성과 별개로 절차 미준수(휴가계 미제출)가 핵심
- **id_16659**: 영업직 자택 체류를 근로제공의무 해태(실질적 무단결근)로 인정한 사례
- **id_16943**: 공익사업(시내버스) 집단 결행 — 시민불편·과징금·영업손실 고려, 징계시기 미확정도 불가피
- **id_16855 vs id_16321/id_16571/id_16921**: 전보 거부 결근 사례 4건 중 id_16855만 전보 부당 → 결근도 징계사유 불인정

## 통계

| 항목 | 수 |
|------|---|
| 총 건수 | 30 |
| 결근 핵심 | 7 (23%) |
| 결근 복합/해고부존재 (exclusion 미부여) | 8 (27%) |
| 결근 배경 (exclusion 부여) | 15 (50%) |
| confidence high | 30 |
| confidence medium | 0 |

### primary 분포
| issue_type_primary | 수 |
|---|---|
| absence_without_leave | 7 |
| disciplinary_severity | 7 |
| dismissal_validity | 6 |
| transfer_validity | 5 |
| misconduct | 3 |
| renewal_expectation | 1 |
| unfair_treatment | 0 |
| procedure | 0 |

### disposition_type 분포
| disposition | 수 |
|---|---|
| disciplinary_dismissal | 10 |
| suspension | 8 |
| no_formal_disposition | 4 |
| dismissal | 2 |
| reprimand | 2 |
| pay_cut | 1 |
| demotion | 1 |
| probation_termination | 1 |
| rejection_of_regular_employment | 1 |

## 품질 체크
- [x] 모든 case_id가 입력과 일치 (30건)
- [x] exclusion_flags에 not_really_absence_case 적절 부여 (15건)
- [x] 핵심 결근 사건에 unauthorized_absence fact_marker 부여
- [x] 전보 관련 결근 사건에 transfer_validity primary 부여 (4건)
- [x] 해고부존재 사건 적절 처리 (id_16351, id_16365, id_16673, id_17001)
- [x] 사직서 강요 사건 resignation_dispute exclusion 부여 (id_16389, id_16743)
- [x] tag_version: v1, review_status: pending 전건 확인
