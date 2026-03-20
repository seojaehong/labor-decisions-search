# incompetence_batch_008 Self-Review

## 배치 개요
- **입력**: 30건 (id_411379 ~ id_4429)
- **출력**: 30건 전량 태깅 완료
- **작업일**: 2026-03-20

## 분류 통계

### issue_type_primary 분포
| primary | 건수 | 비고 |
|---------|------|------|
| work_ability | 19 | 수습 본채용 거부 + 통상해고 |
| disciplinary_severity | 5 | 징계해고/감봉, 업무실적 불량은 보조 |
| renewal_expectation | 4 | 갱신기대권 혼입 사례 |
| dismissal_validity | 2 | 해고 부존재/구제이익 부정 |

### employment_stage 분포
| stage | 건수 |
|-------|------|
| probation | 17 |
| regular | 7 |
| renewal_stage | 4 |
| fixed_term | 1 |
| unknown | 0 |

### decision_result 분포
| result | 건수 |
|--------|------|
| dismissed (기각) | 17 |
| granted (인용) | 6 |
| upheld (재심 초심유지) | 5 |
| overturned (재심 초심취소) | 2 |

## work_ability vs dismissal_validity 판단 기준

본 배치의 핵심 분류 기준:

1. **work_ability를 primary로 부여한 경우 (19건)**: 업무능력 부족/업무부적격이 실질적 해고사유이고, 위원회가 그 정당성을 직접 판단한 사례
2. **dismissal_validity를 primary로 부여한 경우 (2건)**:
   - id_411941: 해고 자체의 존재 여부가 쟁점 (업무능력 부족은 배경 사실)
   - id_43475: 구제이익 존부가 쟁점 (업무능력 부족은 후속 정직의 사유)
3. **disciplinary_severity를 primary로 부여한 경우 (5건)**: 복합 비위에 대한 징계 양정이 핵심이고, 업무실적/능력 부족은 징계사유의 일부이거나 부인된 경우

## 갱신기대권 혼입 처리 (4건)

| case_id | 갱신기대권 | 갱신거절 합리성 | primary | exclusion |
|---------|-----------|---------------|---------|-----------|
| id_412327 | 인정 | 합리적 (58점) | renewal_expectation | renewal_expectation_dominant |
| id_43637 | 인정 | 불합리 | renewal_expectation | renewal_expectation_dominant |
| id_43703 | 인정 | 불합리 (평가 급락) | renewal_expectation | renewal_expectation_dominant |
| id_44123 | 인정 | 불합리 (민원 불명확) | renewal_expectation | renewal_expectation_dominant |

추가로 id_44145는 갱신기대권 자체가 부정되어 fixed_term + renewal_expectation primary + renewal_expectation_dominant exclusion으로 처리.

**원칙**: 갱신기대권이 쟁점의 전제조건인 경우 renewal_expectation을 primary로, work_ability는 secondary로. exclusion_flags에 renewal_expectation_dominant를 부여하여 "업무능력 부족 해고" 검색 시 상위 노출 방지.

## 주요 판단 메모

### 업무능력 부족이 징계사유로 불인정된 사례
- id_411379: "업무실적 및 근무성적 불량" 입증 부족으로 징계사유 불인정 (나머지 비위는 인정)
- id_412461: "업무미숙"은 징계사유가 아닌 업무배제 사유로 재분류
- id_413549: "3년 연속 업무실적 최하위"는 징계사유로 불인정

### 특이 사례
- id_412075: 해고 철회 후 재해고 구조. 매출 부진이 근로자 귀책이 아니라는 판단.
- id_43869: 연구기관 저성과자 해고에서 최후수단 원칙(교육·직무재배치) 강조.
- id_43873: 결근 원인이 사용자의 직장 내 괴롭힘이라는 이례적 인과관계 인정.
- id_429: 상시근로자 5인 산정이 선결 쟁점(사용자 배우자·처제 근로자성).

## 신뢰도 분포
- high: 30건 / medium: 0건 / low: 0건
- 전건 source_text가 충분하여 high 부여.

## 검수 필요 사항
- 없음. 전건 태깅 스키마 준수 확인 완료.
