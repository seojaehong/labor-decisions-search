# probation_batch_007 Self Review

## 처리 요약
- **입력**: 30건 (id_19541 ~ id_20925)
- **출력**: 30건 전량 태깅 완료
- **태깅 버전**: v1
- **review_status**: 전건 pending

## Confidence 분포
| confidence | 건수 |
|-----------|------|
| high      | 29   |
| medium    | 1    |
| low       | 0    |

medium 1건(id_20797): 구제의사 포기로 각하되어 본안 판단 없음. 선례가치 제한적.

## employment_stage 분포
| stage         | 건수 | case_id 예시 |
|--------------|------|-------------|
| probation    | 22   | id_19541, id_19597, id_19605, id_19995 등 |
| regular      | 5    | id_19569, id_19671, id_20365, id_20419, id_20873 |
| fixed_term   | 2    | id_19859, id_2083 |
| renewal_stage| 0    | - |

## disposition_type 분포
| type                            | 건수 |
|--------------------------------|------|
| rejection_of_regular_employment | 14   |
| probation_termination           | 5    |
| dismissal                       | 5    |
| disciplinary_dismissal          | 3    |
| nonrenewal                      | 1    |
| contract_termination            | 1    |
| suspension                      | 1    |

## exclusion_flags 부여 현황
| flag                          | 건수 | case_id |
|------------------------------|------|---------|
| unrelated_to_probation       | 3    | id_19569, id_19859, id_2083 |
| renewal_expectation_dominant | 2    | id_19859, id_2083 |
| fact_specific_low_reusability| 1    | id_20797 |

## rejection_of_regular_employment vs probation_termination 구분

| 구분 | 기준 | 적용 건수 |
|------|------|----------|
| rejection_of_regular_employment | 수습기간 **만료 시점**에 본채용 거부 | 14건 |
| probation_termination | 수습기간 **도중**에 해약권 행사로 중도 해고 | 5건 |

- **만료 시 거부(rejection)**: id_19541, id_19597, id_19605, id_19817, id_19995, id_20159, id_20289, id_20505, id_20555, id_20601, id_20689, id_20753, id_20815, id_20917
- **중도 해고(termination)**: id_19769, id_20019, id_20035, id_20339, id_20355

## 대표 보정 사례

### 1. id_19569: probation → regular / disciplinary_severity
- **레거시**: `probation, absence, misconduct` → 수습 사건으로 분류
- **보정**: `employment_stage=regular`, `issue_type_primary=disciplinary_severity`, `exclusion=unrelated_to_probation`
- **사유**: 본문에 수습/시용 관련 쟁점이 전혀 없음. 의용소방대 봉사활동 자료 누락, 업무지시 불이행, 무단결근 등 일반 징계양정 사건. 레거시 태그의 probation은 오분류.

### 2. id_19859: probation → fixed_term / renewal_expectation
- **레거시**: `contract_expiry, probation` → 수습 사건으로 분류
- **보정**: `employment_stage=fixed_term`, `issue_type_primary=renewal_expectation`, `exclusion=unrelated_to_probation`
- **사유**: 시용기간(3개월)은 이미 종료되었고, 이후 기간제 근로계약(9개월)의 만료에 따른 당연퇴직 여부가 쟁점. 갱신기대권 부정 사건.

### 3. id_20365: probation → regular (수습기간 취업규칙 초과로 무효)
- **레거시**: `worker_status, probation, absence` → 수습 사건으로 분류
- **보정**: `employment_stage=regular`, `issue_type_primary=procedure`
- **사유**: 취업규칙상 수습기간 최대 3개월인데 근로계약서에 5개월로 설정 → 근기법 제97조에 의해 무효. 해고 시점(5개월차)에는 이미 정규직 지위. 인사위원회 미개최로 절차위반.

### 4. id_20873: probation → regular (수습 부정)
- **레거시**: `no_dismissal, probation` → 수습 사건으로 분류
- **보정**: `employment_stage=regular`, `issue_type_primary=dismissal_validity`
- **사유**: 월정급여 100% 지급, 수습기간 별도 합의 근거 없음 → 수습근로자로 보기 어렵다고 판정. 해고 존부(사직 vs 해고) + 해고사유 부존재 + 서면통지 미비.

### 5. id_2083: probation → fixed_term / renewal_expectation
- **레거시**: `contract_expiry, worker_status, probation, no_dismissal` → 수습 사건으로 분류
- **보정**: `employment_stage=fixed_term`, `issue_type_primary=renewal_expectation`, `exclusion=unrelated_to_probation`
- **사유**: 용역계약기간에 연동된 기간제 근로계약. 갱신기대권 존부가 핵심. 수습기간 규정은 있으나 판정 프레임과 무관.

## 수습 여부 부정 사건 정리 (3건)

| case_id | 부정 사유 | employment_stage |
|---------|----------|-----------------|
| id_19671 | 수습기간 합의 사실 불인정 | regular |
| id_20419 | 동일 사업장 기존 근무경력 | regular |
| id_20873 | 급여 100% 지급, 별도 합의 근거 없음 | regular |

이들은 수습 프레임이 다투어졌으나 부정된 사건으로, "수습 여부 판단" 검색 시 관련성이 높아 exclusion 미부여.

## id_20159 vs id_20601 중복 여부
- 두 건 모두 봉제가공업 시용 본채용 거부 사건이나 case_id가 다르므로 별개 사건으로 태깅. 추후 중복 확인 권장.

## 새 규칙 이슈 메모

1. **수습 급여 감액 여부에 의한 수습 인정 기준** (id_20873): "급여 100% 지급 → 수습 부정" 논리가 적용됨. 현재 스키마에 `wage_reduction_during_probation` 같은 fact_marker가 없음. 빈도에 따라 추가 검토.

2. **취업규칙 대비 불리한 수습기간 설정** (id_20365): 근기법 제97조에 의한 수습기간 무효 판단. 이 유형이 반복되면 별도 fact_marker (예: `probation_period_invalid`) 신설 검토.

3. **해고제한 회피 목적 형식적 시용계약** (id_20917): 시용계약이 실질이 아닌 해고회피 수단으로 판단됨. 현재 exclusion_flags나 fact_markers로 커버 가능하나, 빈도 증가 시 별도 마커 검토.
