# workplace_bullying_batch_010 Self-Review

## 배치 개요
- **입력**: 30건 (id_348551 ~ id_349945)
- **출력**: 30건 전량 처리
- **일시**: 2026-03-20

## issue_type_primary 분포

| primary | 건수 | 비고 |
|---------|------|------|
| workplace_harassment | 10 | 순수 괴롭힘 성립이 다투어진 사례 |
| disciplinary_severity | 14 | 괴롭힘은 전제/배경, 양정이 핵심 |
| misconduct | 1 | 업무지시 거부 (괴롭힘 주장 배척) |
| harassment_investigation | 1 | 괴롭힘 조사 목적 직위해제 |
| discrimination | 1 | 차별시정(성희롱 신고 후 불이익) |
| worker_status | 1 | 근로자성 판단 |
| dismissal_validity | 2 | 징계사유 부존재 |

## exclusion_flags 분포

| flag | 건수 |
|------|------|
| not_really_harassment_case | 16 |
| unrelated_to_harassment | 7 |
| fact_specific_low_reusability | 1 |
| emotional_conflict_not_harassment | 1 |
| resignation_dispute | 1 |
| evidence_too_thin | 1 |
| (없음 = 순수 괴롭힘 관련) | 10 |

## 순수 괴롭힘(workplace_harassment primary) 10건 상세

1. **id_348861** - 지위 우위 이용 불법행위 강요+폭언 → 정직 3월 정당
2. **id_349035** - 개선기회 후 재발, 피해자 전원 퇴사 → 해고 정당
3. **id_349177** - 괴롭힘 불성립 ('엄살 떨지마' 업무 범위 내) → 감봉 부당
4. **id_349193** - 센터장 관리자의 괴롭힘 가담+성희롱 → 해고 정당
5. **id_349227** - '우위' 요건 불충족으로 괴롭힘 불성립 → 징계+전보 부당
6. **id_349459** - 외부조사 불인정, 우발적 발언만 인정 → 양정 과다
7. **id_349463** - 시용근로자 비하발언 괴롭힘 → 의료기관 특수성 → 해고 정당
8. **id_349693** - 다수 약자 대상 장기 반복 → 해고 정당
9. **id_349757** - 6가지 구체적 행위 모두 인정+전력 재발 → 감봉 3월 정당
10. **id_349891** - 임신 피해자+육아휴직 부담 → 출근정지+직책면 정당

그 외 순수 괴롭힘 성립 인정(primary는 disciplinary_severity이나 괴롭힘 직접 인정):
- **id_349773** - 폭언+보복 암시 → 정직 2월 정당
- **id_349895** - 동료 과반수 신고 → 해고 정당
- **id_349905** - 외부 법률사무소 조사 5건 인정 → 감봉 3월 정당
- **id_349929** - 생산팀 12명 진정+퇴사자 → 감봉 정당

## 괴롭힘 검색에서 배제해야 할 사건 (7건)

| case_id | 이유 |
|---------|------|
| id_348571 | 차별시정(성희롱) 사건, 괴롭힘은 역전 구조 |
| id_348877 | 괴롭힘 명시적 불인정, 보조금 부정이 핵심 |
| id_34905 | 괴롭힘(가혹행위) 증거 부족 불인정 |
| id_34915 | 사용자 주장 사유 전부 부존재 |
| id_349273 | 근로자성 판단 사건, 괴롭힘은 배경 |
| id_349297 | 성희롱 양정 사건, 괴롭힘은 배경 |
| id_349945 | 업무지시 거부, 괴롭힘 주장 배척 |

## 판단이 어려웠던 사건

### id_349177 (confidence: high이나 주의)
- '엄살 떨지마' 발언의 업무상 적정범위 판단이 핵심
- 괴롭힘 불성립 사례로서 검색 가치 높음
- primary를 workplace_harassment로 분류 (성립 여부 자체가 다투어졌으므로)

### id_349339 (confidence: low)
- source_text가 holding_points와 동일 (요약만 존재)
- 상세 사실관계 없어 태깅 신뢰도 낮음
- fact_specific_low_reusability 부여

### id_349655 (괴롭힘 vs 양정 경계)
- 괴롭힘(사적 업무지시)은 인정되었으나 "중대한 징계사유라는 입증 부족"
- 예산 부정집행이 주된 비위이므로 disciplinary_severity로 분류
- 다만 괴롭힘 관련 exclusion_flag는 미부여 (괴롭힘 자체는 인정되었으므로)

## confidence 분포

| level | 건수 |
|-------|------|
| high | 29 |
| low | 1 (id_349339) |

## 품질 체크리스트
- [x] 모든 case_id 매칭 확인
- [x] issue_type_primary 단일값 확인
- [x] disposition_type이 schema 허용값 내 확인
- [x] 괴롭힘 성립 vs 양정 vs 보복 구분 완료
- [x] not_really_harassment_case 배경 사건 식별 완료
- [x] include/exclude 쿼리 한국어 작성
- [x] review_status: "pending", tag_version: "v1" 전건 확인
