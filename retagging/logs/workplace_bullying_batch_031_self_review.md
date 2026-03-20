# workplace_bullying_batch_031 self-review

## 배치 개요
- 총 30건 (id_44079 ~ id_44931)
- 괴롭힘 배치이나 실질 쟁점 분포가 다양함

## 분류 통계

### issue_type_primary 분포
| primary | 건수 | 비고 |
|---------|------|------|
| workplace_harassment | 8 | 괴롭힘 성립/불성립이 핵심 쟁점 |
| disciplinary_severity | 13 | 양정 과다/적정 여부가 핵심 |
| transfer_validity | 5 | 전보/대기발령/인사명령 정당성 |
| dismissal_validity | 3 | 해고사유 부존재/해고 정당성 |
| renewal_expectation | 1 | 고용승계 기대권이 실질 |

### not_really_harassment_case 플래그 부여 (7건)
| case_id | 사유 |
|---------|------|
| id_44089 | 전보 사건, 괴롭힘은 배경사실(가해자 근무지로 전보) |
| id_44311 | 동료 간 다툼, 우위성 불인정으로 괴롭힘 명시적 배척 |
| id_44599 | 괴롭힘은 일방 주장만 있고 판단 없음, 사유 전반 불인정 |
| id_44751 | 성희롱·괴롭힘 모두 불인정, 양정 과다가 핵심 |
| id_44783 | 괴롭힘 갈등이 전보 배경, 전보 정당성이 실질 |
| id_44799 | 괴롭힘은 과거 정직 사유로만 간접 언급, 시용해고가 핵심 |
| id_44859 | 교통사고 징계 사건, 본문에 괴롭힘 관련 내용 전무 |
| id_44905 | 괴롭힘 불인정, 성희롱 1회만 인정, 양정 과다가 핵심 |
| id_44931 | 괴롭힘 조사 자체 미실시, 해고사유 부존재가 핵심 |

### 괴롭힘 성립 vs 불성립 판단 사례
| 유형 | 건수 | 대표 case_id |
|------|------|-------------|
| 괴롭힘 성립 인정 | 13 | id_44079, id_44205, id_44351, id_4457, id_44769, id_44803, id_44917 등 |
| 괴롭힘 불성립 | 4 | id_44311(우위성 불인정), id_44485(작업갈등), id_44693(업무지도), id_44751(불인정) |
| 괴롭힘 판단 자체 없음/배경 | 9 | id_44089, id_44599, id_44783, id_44799, id_44859 등 |
| 입증 부족으로 불인정 | 4 | id_44513(일부), id_44599, id_44905, id_44931 |

### 양정 판단 분포
| 양정 판단 | 건수 |
|-----------|------|
| 양정 정당 | 14 |
| 양정 과다 (부당) | 9 |
| 양정 미판단 (사유 불인정 등) | 7 |

### disposition_type 분포
| 처분유형 | 건수 |
|----------|------|
| disciplinary_dismissal | 12 |
| transfer | 5 |
| suspension | 5 |
| pay_cut | 3 |
| reprimand | 3 |
| demotion | 1 |
| rejection_of_regular_employment | 1 |
| dismissal | 1 |
| nonrenewal | 1 |

### employment_stage 분포
| 단계 | 건수 |
|------|------|
| regular | 27 |
| probation | 2 |
| renewal_stage | 1 |

### industry_context 분포
| 산업 | 건수 |
|------|------|
| unknown | 23 |
| public | 4 |
| healthcare | 2 |
| transport | 1 |
| finance | 1 |
| sales | 1 |
| it | 1 |

### decision_result 분포
| 결과 | 건수 |
|------|------|
| dismissed (기각) | 14 |
| granted (인용) | 9 |
| upheld (초심유지, 재심) | 7 |

## 특이사항 및 판단 근거

1. **id_44311**: 동료 간 다툼에서 '직장 내 괴롭힘' 신고가 있었으나 '지위 또는 관계상 우위'가 인정되지 않아 명시적으로 괴롭힘이 배척됨. emotional_conflict_not_harassment 플래그 부여.

2. **id_44485**: 작업속도 차이에서 비롯된 불편함은 괴롭힘이 아니라는 판단. 괴롭힘 성립 요건(업무관련성, 적정범위 일탈) 불충족 사례로 참고가치 높음.

3. **id_44693**: 수습 기자에 대한 업무 지도가 괴롭힘인지 여부를 판단. '업무상 적정범위'의 경계를 보여주는 사례.

4. **id_44859**: 레거시 태그에 workplace_bullying이 있으나 본문에 괴롭힘 관련 내용이 전무. 교통사고 징계+부당노동행위 사건으로 unrelated_to_harassment 플래그 추가.

5. **id_44877**: 근로기준법 제76조의3 제5항(분리조치 의무)을 명시적으로 인용하여 가해자 전보의 업무상 필요성을 인정한 드문 사례.

6. **id_44351**: 자필확인서 작성 지시를 괴롭힘으로 인정하고, 동시에 피해자 보호를 위한 가해자 배치전환도 정당하다고 판단한 복합 사례.

7. **id_44755**: 시용근로자의 괴롭힘+근무태도 불량→본채용 거부. probation과 harassment의 교차 사례.

## 자기검증 체크리스트

- [x] 모든 case_id가 입력과 일치 (30건)
- [x] issue_type_primary가 스키마 허용값 내
- [x] disposition_type이 source_text의 실제 처분과 일치
- [x] not_really_harassment_case는 괴롭힘 판단이 배경이거나 부재한 경우에만 부여
- [x] confidence는 source_text 분량·판단 명확성 기준으로 설정
- [x] include_for_queries가 실제 검색 시나리오 반영
- [x] exclude_for_queries가 오검색 방지에 유효
- [x] review_status = "pending", tag_version = "v1" 일관
