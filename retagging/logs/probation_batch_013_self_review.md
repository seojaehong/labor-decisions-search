# probation_batch_013 Self-Review

## 배치 개요
- **입력**: `retagging/input/batches/probation_batch_013.jsonl` (30건)
- **출력**: `retagging/output/reviewed/probation_batch_013_reviewed.jsonl` (30건)
- **작업일**: 2026-03-20

## 수습 vs 비수습 분류

### 수습(probation) 관련 사건 (24건)
| case_id | employment_stage | 분류 근거 |
|---------|-----------------|----------|
| id_27867 | probation | 수습해제평가 합격기준 미달 본채용 거부 |
| id_27897 | probation | 시용근로관계 여부 판단 전 구제이익 소멸 |
| id_27987 | probation | 수습기간 중 징계 — 절차위반으로 부당 |
| id_28133 | probation | 수습기간 도과 후 본채용 거부 → 부당 |
| id_28141 | probation | 시용근로자 2회 평가 미달 → 본채용 거부 정당 |
| id_2817 | probation | 시용기간 중 적대행위로 해고 정당 |
| id_28345 | probation | 시용관계 인정, 평가 미실시 거부 부당 |
| id_28367 | probation | 수습기간 중 복합 부적격 → 해고 정당 |
| id_28423 | probation | 시용기간 중 평가 미실시·입증 부족 → 부당 |
| id_28425 | probation | 수습기간 1개월 조기종료 후 정식채용 상태 해고 → 부당 |
| id_28455 | probation | 시용 중 업무부적합 본채용 거절 정당 |
| id_28511 | probation | 경력직 시용 3주 만에 능력미달 본채용 거부 정당 |
| id_28559 | probation | 수습기간 도과(4개월) → 해고 → 서면통지 위반 부당 |
| id_28623 | probation | 수습평가 합격점수 미달 본채용 거부 정당 |
| id_28679 | probation | 수습 중 핵심업무 부실 매출손실 → 해고 정당 |
| id_28713 | probation | 인턴평가 미달 본채용 거부 정당 |
| id_28825 | probation | 시용 중 조리실력 부족 해고 정당 |
| id_29041 | probation | 시용 업무평가 미달 + 근무태도 불량 → 거부 정당 |
| id_29137 | probation | 시용 운전원 교통사고 본채용 거절 정당 |
| id_29165 | probation | 1인 주관적 평가 + 경미한 비위 → 거절 부당 |
| id_29311 | probation | 본채용 기준 미비 등 6중 결함 → 거부 부당 |
| id_29367 | probation | 수습평가 적정 → 본채용 거부 정당 |
| id_29459 | probation | 파견→정규직 전환자 동일기준 수습평가 부당 |
| id_29461 | probation | 인사평가 미달 + 서면통지 → 거부 정당 |

### 비수습(unrelated_to_probation) 사건 (6건)
| case_id | employment_stage | 분류 근거 |
|---------|-----------------|----------|
| id_28331 | regular | 이사 직함이나 실질 근로자. 수습평가는 근로자성 보조 징표일 뿐 |
| id_28917 | regular | 수습기간 미기재·임금전액지급 → 시용관계 부인. 통상해고 사건 |
| id_28955 | fixed_term | 수습3개월+계약9개월의 기간제. 실질은 갱신기대권 사건 |
| id_28965 | fixed_term | 수습=계약기간이나 형식 아님. 갱신기대권 불인정 |
| id_29027 | probation (stage) | 시용 법리 언급 있으나 실질은 유니온숍+면직사유. unrelated_to_probation 플래그 |
| id_29501 | probation | 산재 해고금지기간 쟁점 포함하나 수습 본채용 거부가 주된 쟁점 |

## rejection vs termination 구분

### 본채용 거부(rejection_of_regular_employment) — 19건
id_27867, id_27897, id_28133, id_28141, id_28345, id_28423, id_28455, id_28511, id_28623, id_28713, id_29041, id_29137, id_29165, id_29311, id_29367, id_29459, id_29461, id_29501, id_28559(도과→dismissal로 재분류)

### 시용기간 중 해고/해지(probation_termination/dismissal) — 7건
| case_id | disposition_type | 사유 |
|---------|-----------------|------|
| id_2817 | probation_termination | 시용기간 중 해고(근무태도) |
| id_28367 | probation_termination | 수습기간 중 해고(복합부적격) |
| id_28679 | probation_termination | 수습기간 중 해고(업무부실) |
| id_28825 | probation_termination | 시용기간 중 해고(조리실력) |
| id_28425 | dismissal | 수습 종료 후 정식채용 상태에서 해고 |
| id_28559 | dismissal | 수습 도과 후 해고(본채용 거부 아님) |
| id_28331 | dismissal | 위촉해지=해고(수습 무관) |

### 기타
| case_id | disposition_type | 사유 |
|---------|-----------------|------|
| id_27987 | disciplinary_dismissal | 수습기간 중 징계해고 |
| id_29027 | dismissal | 면직(유니온숍 관련) |
| id_28955, id_28965 | contract_termination, nonrenewal | 계약만료 |

## 주요 판단 포인트

1. **수습기간 도과 사건 (id_28133, id_28559, id_28425)**: 수습기간 도과 후에는 통상근로자와 동일 해고절차 적용. rejection이 아닌 dismissal로 분류.

2. **시용관계 부인 사건 (id_28917)**: 수습기간 미기재 + 임금전액지급 → 시용관계 불인정. employment_stage를 regular로, unrelated_to_probation 플래그.

3. **갱신기대권 사건 (id_28955, id_28965)**: 수습기간이 계약기간의 일부이거나 동일해도 실질 쟁점은 갱신기대권. fixed_term + unrelated_to_probation.

4. **1인 주관적 평가 패턴 (id_29165, id_29311)**: 관리소장 등 1인이 주관적으로 평가한 경우 객관성·공정성 부인 → 본채용 거부 부당.

5. **파견→정규직 전환 (id_29459)**: 기존 파견근무 실적이 있는 자에게 신규채용 동일기준 적용은 부적정.

## 신뢰도 분포
- high: 28건
- medium: 2건 (id_27897 구제이익 소멸로 실질 판단 없음, id_29027 수습 법리 부수적)

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 "pending"
- tag_version: 전건 "v1"
