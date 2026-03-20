# absence_batch_032 Self-Review

## 배치 개요
- **입력**: 30건 (absence_batch_032.jsonl)
- **출력**: 30건 (absence_batch_032_reviewed.jsonl)
- **작업일**: 2026-03-20

## 무단결근 핵심 vs 배경 분류

### 결근이 핵심 사유 (8건)
| case_id | 요약 | issue_type_primary |
|---------|------|--------------------|
| id_347359 | 무단결근 징계사유 인정되나 근로조건 불이익변경 경위 참작 → 양정과다 | absence_without_leave |
| id_34737 | 무단결근 3회 수습근로자 해고 정당 | absence_without_leave |
| id_347403 | 일방적 휴직신청+무단결근 → 해고 정당 | absence_without_leave |
| id_347553 | 무단결근 징계사유 존재하나 2년 지연 → 양정 과다 | absence_without_leave |
| id_347649 | 3개월 장기 무단결근+폭언 → 해고 정당 | absence_without_leave |
| id_34775 | 무단결근·근무지이탈 → 정직 정당 | absence_without_leave |
| id_347965 | 18일 무단결근+지시불이행 → 해고 정당 | absence_without_leave |
| id_348195 | 2개월간 11일+ 무단결근 → 해고 정당 | absence_without_leave |

### 결근이 복합 사유 중 하나 (5건)
| case_id | 요약 | issue_type_primary |
|---------|------|--------------------|
| id_347641 | 근무태만+지시불이행+허위작성+상습조기퇴근 복합 | misconduct |
| id_348109 | 근태불량+야간겸업+택시비부정+지시불이행 복합 | misconduct |
| id_34819 | 업무방해+복귀명령불이행+17일결근 복합 | misconduct |
| id_347727 | 갱신기대권 인정, 불성실근무(15일결근 포함)로 거절 합리적 | renewal_expectation |
| id_348015 | 근태불량(지각)+허위신고+교육미이수 복합 | misconduct |

### 결근이 배경사실 (not_really_absence_case) (17건)
| case_id | 요약 | 실질 쟁점 |
|---------|------|-----------|
| id_347319 | 갱신기대권, 무단이탈은 거절 사유 중 하나 | renewal_expectation |
| id_347335 | 전보+정직 양정, 본문에 결근 사실 없음 | disciplinary_severity |
| id_347363 | 사직서 합의해지, 무단결근은 배경 | dismissal_validity |
| id_347389 | 괴롭힘·성희롱 양정과다, 본문에 결근 없음 | disciplinary_severity |
| id_347391 | 복직명령 미이행, 무단이탈은 사유 불인정 | disciplinary_severity |
| id_347679 | 제척기간 도과 각하, 결근은 해고 배경 | procedure |
| id_347747 | 해고부존재(자진퇴사), 결근은 배경 정황 | dismissal_validity |
| id_347763 | 근로시간면제 임금산정, 결근 아님 | unfair_treatment |
| id_347769 | 사직 vs 해고 구분, 결근은 발단 | dismissal_validity |
| id_347891 | 괴롭힘+근무태만 양정과다, 실제 결근 아님 | disciplinary_severity |
| id_347949 | 시용근로자 본채용거부, 근무태만 증거 없음 | dismissal_validity |
| id_347975 | 특수경비 임의휴식 정직 양정과다, 결근 아님 | disciplinary_severity |
| id_34757 | 골프장 체류 사적행위 해고, 결근 아님 | misconduct |
| id_348069 | 갱신기대권+평가공정성, 연차=결근 반영 문제 | renewal_expectation |
| id_348087 | 해고부존재, 무단결근→퇴직처리 | dismissal_validity |
| id_348149 | 복합 사유 양정과다, 근태불량은 경미 | disciplinary_severity |
| id_348187 | 권고사직 합의 해고부존재 | dismissal_validity |

## 통계 요약
| 분류 | 건수 | 비율 |
|------|------|------|
| 결근 핵심 | 8 | 26.7% |
| 결근 복합 사유 | 5 | 16.7% |
| 결근 배경 (not_really_absence_case) | 17 | 56.7% |
| **합계** | **30** | **100%** |

## issue_type_primary 분포
| primary | 건수 |
|---------|------|
| absence_without_leave | 8 |
| disciplinary_severity | 6 |
| dismissal_validity | 6 |
| misconduct | 5 |
| renewal_expectation | 3 |
| procedure | 1 |
| unfair_treatment | 1 |

## disposition_type 분포
| disposition | 건수 |
|-------------|------|
| disciplinary_dismissal | 17 |
| no_formal_disposition | 5 |
| suspension | 5 |
| nonrenewal | 3 |
| rejection_of_regular_employment | 1 |
| transfer+suspension | 1 (id_347335 복합) |

## decision_result 분포
| 결과 | 건수 |
|------|------|
| dismissed (기각) | 13 |
| granted (인용) | 6 |
| upheld (초심유지) | 5 |
| overturned (초심취소) | 3 |
| partial (일부인용) | 1 |
| rejected (각하) | 1 |

## 특이사항/주의 건
1. **id_347763**: 부당노동행위 사건으로 결근과 무관. 근로시간면제 활동을 결근으로 본 레거시 태그 오류.
2. **id_347389**: 본문에 결근 관련 징계사유가 전혀 없음. 레거시 absence 태그 명확한 오태깅.
3. **id_347335**: 전보+정직 병행 사례. 본문에 absence 실체 없음.
4. **id_347553**: 무단결근 인지 후 2년 경과 시점 징계 → 비례원칙 위반으로 부당. 지연 징계 참고 사례.
5. **id_347359**: 근로조건 불이익변경으로 결근하게 된 경위 참작 → 양정 과다. 경위 참작 사례.
6. **id_34737**: 수습근로자 해고기준 완화 적용된 무단결근 사례.

## 품질 자기평가
- **confidence high**: 30건 전체
- 레거시 absence 태그가 있으나 실제 결근 사안이 아닌 건이 17건(56.7%)으로 다수 — 기존 태깅의 과잉 분류가 확인됨
- 무단결근이 핵심인 8건은 모두 absence_without_leave로 primary 지정, 양정 판단(정당/과다)에 따라 fact_markers 차별화
