# incompetence_batch_005 Self-Review

## 배치 개요
- **입력**: 30건 (id_347233 ~ id_36875)
- **출력**: 30건 전량 태깅 완료
- **배치 특성**: 수습 본채용 거부(16건), 정규직 해고(7건), 갱신기대권(2건), 전보/직위해제(3건), 징계양정(2건) 혼합

## 핵심 판단 기준 적용

### 1. work_ability vs dismissal_validity 구분
| 판정 | 건수 | 대표 case_id |
|------|------|-------------|
| work_ability (primary) | 19건 | id_347233, id_348573, id_348635 등 |
| dismissal_validity (primary) | 2건 | id_349563, id_351553 |
| 기타 primary | 9건 | - |

- **work_ability**: 업무능력·근무태도가 판정의 핵심 쟁점인 경우
- **dismissal_validity**: 업무능력 부족이 주장되었으나 해고 자체의 정당성(사유 복합·근로자성 등)이 핵심인 경우
- id_349563: 경력허위기재 + 업무능력 부족이 모두 불인정 → dismissal_validity
- id_351553: 이사 직급 근로자성 + 업무능력 부족 + 경영상 사유가 결합 → dismissal_validity

### 2. 갱신기대권 혼입 처리
| case_id | 처리 | exclusion_flags |
|---------|------|----------------|
| id_3545 | renewal_expectation (primary) | renewal_expectation_dominant |
| id_36349 | renewal_expectation (primary) | renewal_expectation_dominant |

- 2건 모두 갱신기대권이 판정의 핵심이고, incompetence는 갱신거절 사유로 주장만 된 수준
- exclude_for_queries에 "정규직 저성과 해고" 추가

### 3. 수습 vs 정규직 구분
| employment_stage | 건수 |
|-----------------|------|
| probation | 16건 |
| regular | 8건 |
| renewal_stage | 2건 |
| fixed_term | 1건 |

- 수습: 시용근로자 인정 + 본채용 거부/수습기간 해고
- id_349243: 기간제 주장 배척 → 시용근로계약 인정 (probation)
- id_35963: 1개월 계약이나 시용계약으로 인정 (probation)
- id_351561: 계약제교원 → fixed_term

### 4. 전보/직위해제 사례 (incompetence 레거시 태그이나 실제 다른 쟁점)
| case_id | 실제 쟁점 | primary |
|---------|----------|---------|
| id_347971 | 대기발령 정당성 | transfer_validity |
| id_36001 | 전보 부당 | transfer_validity |
| id_35689 | 직위해제 부당 | unfair_treatment |

- 3건 모두 exclusion_flags에 not_really_performance_case 부여

### 5. 징계양정 중심 사례
| case_id | 처분 | primary |
|---------|------|---------|
| id_350053 | 직위해제+해고 | disciplinary_severity |
| id_36525 | 정직 3월 | disciplinary_severity |
| id_36875 | 징계해고 | disciplinary_severity |

- 업무능력 부족은 징계사유 중 하나이나, 양정 적정성이 핵심 판단 기준

## disposition_type 분포
| 유형 | 건수 |
|------|------|
| rejection_of_regular_employment | 13건 |
| dismissal | 5건 |
| probation_termination | 2건 |
| disciplinary_dismissal | 4건 |
| suspension | 3건 |
| transfer | 2건 |
| contract_termination | 1건 |
| nonrenewal | 2건 |

## decision_result 분포
| 결과 | 건수 |
|------|------|
| dismissed (기각) | 14건 |
| granted (인용) | 9건 |
| upheld (재심 초심유지) | 5건 |
| overturned (재심 초심취소) | 2건 |
| partial (일부 인용) | 0건 |

## 특이사항 및 주의점

1. **id_348735**: 실체 사유(40점/80점) 인정되나 서면통지 40일 지연으로 부당 → procedure primary, procedure_dominant 플래그
2. **id_349669**: 6개 징계사유 전부 인정된 드문 사례. 비위행위가 주이므로 misconduct primary
3. **id_3501**: 폐업 사업장이나 임금상당액에 대한 구제이익 인정
4. **id_350209**: 근로자가 해고통지서를 먼저 요청하고 이의 없이 수용한 정황 존재
5. **id_349243**: 평가기간 8일(2.13~2.20)은 사회통념상 지나치게 단기로 판단

## 신뢰도 분포
- high: 30건 (100%)
- medium: 0건
- low: 0건

모든 건이 source_text에서 쟁점 구조가 명확하게 확인되어 high 부여.
