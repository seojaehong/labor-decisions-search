# probation_batch_012_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, 모두 legacy_reason_category에 "probation" 포함
- 핵심 분류 기준: rejection_of_regular_employment(본채용 거부) vs probation_termination(수습 중 해고) vs unrelated_to_probation(수습 무관)

## 분류 통계

### disposition_type 분포
| disposition_type | 건수 | case_id |
|---|---|---|
| rejection_of_regular_employment | 16 | id_26409, id_26463, id_26587, id_26635, id_26665, id_26679, id_26715, id_26871, id_26881(→dismissal로 변경), id_27229, id_27237, id_27371, id_27495, id_27571, id_27665, id_27827 |
| probation_termination | 3 | id_26481, id_27339, id_27715 |
| dismissal (수습 도과 후 정규직 해고) | 4 | id_26881, id_27117, id_27337, id_27803 |
| nonrenewal (기간제 갱신기대권) | 4 | id_26631, id_26901, id_2723, id_27719 |
| no_formal_disposition (합의해지/해고부존재) | 3 | id_26401, id_26819, id_27069 |

### exclusion_flags: unrelated_to_probation 부여 건 (7건)
| case_id | 실질 쟁점 | 이유 |
|---|---|---|
| id_26401 | 근로자성 + 합의해지 | 수습 약정은 근로자성 보조징표일 뿐 |
| id_26631 | 기간제 갱신기대권 | 수습규정 언급되나 실질은 갱신기대권 |
| id_26881 | 수습기간 해석 → 정규직 해고 | 시용기간 도과 후 정규직 지위에서의 해고 |
| id_26901 | 기간제 갱신기대권 | 최초 3개월 시용이나 실질은 갱신기대권 |
| id_2723 | 기간제 갱신기대권 | 수습평가 언급되나 실질은 갱신기대권 |
| id_27117 | 정규직 전환 후 해고 | 수습 1개월 후 정규직, 이후 해고 |
| id_27719 | 기간제 갱신기대권 + 산재 | 수습기간은 배경적 요소 |
| id_27803 | 시용근로자 아님 → 통상 해고 | 취업규칙상 채용확정 + 급여100% |

### employment_stage 분포
| stage | 건수 |
|---|---|
| probation | 18 |
| regular | 5 (id_26401, id_26881, id_27117, id_27803, + id_27337은 probation 유지) |
| fixed_term | 4 (id_26631, id_26901, id_2723, id_27719) |

## 개별 검토 메모

### id_26401 — 학원강사 근로자성 + 합의해지
- employment_stage: regular (수습 도과 여부 불명이나 수습이 쟁점이 아님)
- issue_type_primary: worker_status
- exclusion_flags: unrelated_to_probation, settlement_or_mutual_termination
- 변경 이유: 수습기간 약정은 근로자성 인정의 보조 징표. 본채용 거부 사건이 아님.

### id_26409 — 수습기간 도과 후 본채용 거부
- disposition_type: rejection_of_regular_employment
- issue_type_primary: procedure (도과 후 거부 → 절차 위반이 핵심)
- 변경 이유: 수습기간 도과 시 통상 해고절차 필요라는 판시. 절차 위반이 핵심.

### id_26481 — 경영상 이유 시용 해고
- disposition_type: probation_termination (수습기간 중 해고)
- issue_type_primary: redundancy (실질 사유가 콜센터 구축 무산)
- 변경 이유: 명목은 업무능력 부족이나 실질은 경영상 이유. 수습 중 해고 형태.

### id_26595 — 노조활동 본채용 거부
- issue_type_primary: unfair_treatment (부당노동행위가 핵심)
- disposition_type: rejection_of_regular_employment
- 변경 이유: 표면적 본채용 거부이나 실질은 노조활동 이유 불이익취급.

### id_26631 — 기간제 갱신기대권 (수습 배경)
- employment_stage: fixed_term
- issue_type_primary: renewal_expectation
- exclusion_flags: unrelated_to_probation, renewal_expectation_dominant
- 변경 이유: 취업규칙 수습기간 규정 존재하나 실질은 기간제 갱신 사건.

### id_26819 — 수습평가 후 사직 합의해지
- disposition_type: no_formal_disposition
- exclusion_flags: settlement_or_mutual_termination, resignation_dispute
- 변경 이유: 수습평가 부적합이 배경이나 쟁점은 사직의사 진의 여부.

### id_26881 — 수습기간 해석 (3개월 이내 → 1개월)
- employment_stage: regular (이미 본채용됨)
- disposition_type: dismissal (본채용 거부가 아닌 통상 해고)
- exclusion_flags: unrelated_to_probation
- 변경 이유: 시용기간 도과로 정규직 전환 완료 상태에서 해고.

### id_26901 — 기간제 갱신기대권 (시용기간 배경)
- employment_stage: fixed_term
- exclusion_flags: unrelated_to_probation, renewal_expectation_dominant
- 변경 이유: 최초 3개월 기간제 = 시용이나 실질 쟁점은 갱신기대권.

### id_27069 — 시용기간 종료 시점 사직 합의해지
- disposition_type: no_formal_disposition
- exclusion_flags: settlement_or_mutual_termination, resignation_dispute
- 변경 이유: 시용기간 종료 시점이지만 자발적 사직으로 해고 부존재.

### id_27117 — 수습 후 정규직 전환 → 해고
- employment_stage: regular
- exclusion_flags: unrelated_to_probation
- 변경 이유: 수습 1개월 후 정규직 전환 완료, 이후 1개월 만에 해고. 수습과 무관.

### id_27337 — 유니온숍 + 시용 복합
- issue_type_primary: unfair_treatment
- 변경 이유: 유니온숍 미가입 면직 + 다른 노조 가입 후 면직 복합. 수습은 일부 배경.

### id_27339 — 수습 중 해고 (1개월)
- disposition_type: probation_termination
- 변경 이유: 수습기간 만료 전 해고. 개선기회 미부여 + 서면통지 위반.

### id_27495 — 본채용 거부 사유 사후 추가 불가
- disposition_type: rejection_of_regular_employment
- 변경 이유: 본채용 거부 당시 미제시 사유의 사후 추가 불가라는 중요 판시.

### id_27803 — 시용근로자 아님 (취업규칙 채용확정)
- employment_stage: regular
- exclusion_flags: unrelated_to_probation
- 변경 이유: 취업규칙상 근로계약서 작성 = 채용확정, 급여 100% → 시용 아님.

### id_2723 — 기간제 갱신기대권 (수습평가 배경)
- employment_stage: fixed_term
- exclusion_flags: unrelated_to_probation, renewal_expectation_dominant
- 변경 이유: 1개월 기간제 갱신기대권 사건. 수습평가 언급되나 실질은 갱신.

### id_27719 — 기간제 재계약 + 산재 요양
- employment_stage: fixed_term
- exclusion_flags: unrelated_to_probation, renewal_expectation_dominant
- 변경 이유: 수습 3개월 경과 후 무기계약 전환 관행. 실질은 갱신기대권.

## confidence 분포
| 수준 | 건수 |
|---|---|
| high | 29 |
| medium | 1 (id_27337 — 6명 복합 판정으로 분류 난이도 높음) |

## 주요 판단 패턴 정리

### 본채용 거부 정당 인정 요건 (기각 사례에서 추출)
1. 취업규칙·근로계약서에 수습기간·평가기준 명시
2. 객관적·정량적 평가 실시 (점수 기준 설정)
3. 평가 결과 기준 미달
4. 서면통지 이행
5. (가점) 소명기회 부여, 징계위원회 심의

### 본채용 거부 부당 인정 패턴 (인용 사례에서 추출)
1. 주관적·추상적 평가
2. 객관적 평가 미실시
3. 비교대상 근로자와 형평성 결여
4. 서면통지 미이행
5. 실질 사유와 명목 사유 불일치 (경영상 이유, 노조활동)
6. 사후 사유 추가
7. 개선기회 미부여 (특히 단기 근무 시)
