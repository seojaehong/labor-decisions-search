# probation_batch_006 Self Review

## 처리 요약
- **입력**: 30건 (id_18137 ~ id_1951)
- **출력**: 30건 전량 태깅 완료
- **태깅 버전**: v1
- **review_status**: 전건 pending

## Confidence 분포
| confidence | 건수 |
|-----------|------|
| high      | 30   |
| medium    | 0    |
| low       | 0    |

이번 배치는 판정문 텍스트가 비교적 상세하여 전건 high 판정.

## employment_stage 분포
| stage         | 건수 | case_id 예시 |
|--------------|------|-------------|
| probation    | 21   | id_18167, id_18257, id_18493 등 |
| regular      | 4    | id_18137, id_18475, id_18593, id_19139 |
| fixed_term   | 1    | id_19143 |
| renewal_stage| 2    | id_1843, id_19187 |

## disposition_type 분포
| type                            | 건수 |
|--------------------------------|------|
| rejection_of_regular_employment | 13   |
| probation_termination           | 7    |
| dismissal                       | 5    |
| nonrenewal                      | 3    |
| no_formal_disposition           | 2    |
| contract_termination            | 1    |
| disciplinary_dismissal          | 1    |

## exclusion_flags 부여 현황
| flag                          | 건수 | case_id |
|------------------------------|------|---------|
| unrelated_to_probation       | 6    | id_18137, id_18321, id_18475, id_18593, id_19139, id_19143 |
| renewal_expectation_dominant | 3    | id_18321, id_1843, id_19187 |
| resignation_dispute          | 2    | id_1841, id_18683 |
| procedure_dominant           | 1    | id_18593 |

## 대표 보정 사례

### 1. id_18321: probation → fixed_term / renewal_expectation
- **레거시**: `contract_expiry, probation` → 수습 사건으로 분류
- **보정**: `employment_stage=fixed_term`, `issue_type_primary=renewal_expectation`, `exclusion=unrelated_to_probation`
- **사유**: 1년 기간제 계약의 갱신기대권이 실질 쟁점. 시용기간 규정이 있으나 판정의 프레임은 갱신거절의 합리성이므로 수습 검색에서 상위 노출 방지 필요.

### 2. id_19187: probation → renewal_stage / renewal_expectation
- **레거시**: `contract_expiry, worker_status, probation` → 수습 사건으로 분류
- **보정**: `employment_stage=renewal_stage`, `issue_type_primary=renewal_expectation`, `exclusion=unrelated_to_probation`
- **사유**: 근로계약서의 수습기간 조항이 "갱신 취지"로 해석되어 기대권의 근거가 됨. 판정의 실질 프레임은 갱신기대권 존부와 재계약 거절의 합리성이므로 수습 검색 배제 대상.

### 3. id_18137: probation → regular (수습기간 이미 만료)
- **레거시**: `worker_status, probation, misconduct` → 수습 사건으로 분류
- **보정**: `employment_stage=regular`, `exclusion=unrelated_to_probation`
- **사유**: 최초 입사일 기준 수습기간 3개월이 이미 경과하여 정식 직원 지위. 해고 정당성은 일반 해고 프레임으로 판단됨.

## rejection_of_regular_employment vs probation_termination 구분

| 구분 | 기준 | 적용 건수 |
|------|------|----------|
| rejection_of_regular_employment | 수습기간 **만료 시점**에 본채용 거부 | 13건 |
| probation_termination | 수습기간 **도중**에 해약권 행사로 중도 해고 | 7건 |

- **만료 시 거부**: id_18257, id_18713, id_18761, id_18841, id_18945, id_19041, id_19061, id_19235, id_19373, id_18493, id_19179, id_1951, id_18493
- **중도 해고**: id_18167, id_18423, id_18717, id_1893, id_19205, id_19329, id_19497

## 새 규칙 이슈 메모

1. **기간제+수습 결합 사건의 엄격 기준** (id_18841): "기간제 근로계약에서 수습기간을 정한 경우 본채용 거부는 통상 수습보다 엄격하게 해석해야 한다"는 법리가 포함됨. 이 유형이 반복되면 별도 fact_marker (예: `fixed_term_plus_probation`) 신설 검토 필요.

2. **수습기간 연장의 합리성** (id_18493): 시용기간 연장 자체의 합리성이 쟁점이 된 사건. 현재 스키마에 `probation_extension` 같은 fact_marker가 없음. 빈도에 따라 추가 검토.

3. **극초기 해고** (id_19329): 채용 후 2~3일 내 비위에 의한 해고. `short_tenure`로 커버되나, 극초기(1주 이내)를 별도로 구분할 필요성은 낮음.
