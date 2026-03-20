# workplace_bullying_batch_008 Self-Review

## 배치 개요
- **입력**: 30건 (id_346711 ~ id_347391)
- **출력**: 30건 전량 태깅 완료
- **태그 버전**: v1
- **review_status**: 모두 pending

## 분류 통계

### issue_type_primary 분포
| primary | 건수 | 비고 |
|---------|------|------|
| disciplinary_severity | 14 | 양정 적정성이 핵심 쟁점 |
| transfer_validity | 6 | 괴롭힘 분리 전보의 정당성 |
| workplace_harassment | 3 | 괴롭힘 성립 자체가 핵심 |
| dismissal_validity | 3 | 본채용 거부/구제이익 소멸 |
| unfair_treatment | 2 | 직위해제 부당성 |
| harassment_investigation | 1 | 후속조치 불이행 |
| renewal_expectation | 1 | 갱신기대권 |

### exclusion_flags 분포
| flag | 건수 |
|------|------|
| not_really_harassment_case | 17 |
| unrelated_to_harassment | 4 |
| renewal_expectation_dominant | 1 |
| (없음) | 10 |

### 핵심 판단: 괴롭힘 vs 양정 vs 보복 분류

**괴롭힘 성립이 핵심 쟁점 (workplace_harassment)**: 3건
- id_346765: 업무 배제 주체가 팀장이어서 괴롭힘 불인정 → 견책 부당
- id_346939: 문서 유출→따돌림 유발이 괴롭힘으로 인정 → 견책 정당
- id_346885: 괴롭힘 인정 + 견책 정당, 전보는 불이익 과다로 부당 (일부인용)

**양정이 핵심 쟁점 (disciplinary_severity)**: 14건
- 해고 양정 적정: id_34673, id_346923, id_346931, id_347131, id_347167, id_347173 (6건)
- 해고 양정 과다: id_347389, id_347391 (2건)
- 감봉/정직 양정 과다: id_347045, id_347185 (2건)
- 견책 양정 적정: id_346833, id_346845, id_346845 (3건)
- 초심유지/취소: id_346845 (1건)

**보복(retaliation) 주장 포함**: 3건
- id_346727: 시용 평가 보복 주장 → 증거 부족 부인
- id_346851: 괴롭힘 신고→재임용 거부 보복 주장 → 상관관계 부인
- id_347233: 괴롭힘 가해자의 보복적 저평가 주장 → 가해자 제외 점수도 미달
- id_347391: 진정 제기를 징계사유로 삼는 것의 부적절성 (보복 금지 취지)

**배경으로서의 괴롭힘 (not_really_harassment_case)**: 17건
- 전보 분리조치 관련: 6건 (괴롭힘 신고 후 분리 전보의 정당성이 쟁점)
- 직위해제/구제이익: 4건
- 무단결근/직무태만의 배경: 2건
- 본채용 거부의 배경: 2건
- 폭행이 실질 비위: 2건
- 양정 비교 대상: 1건

## 판단 근거 요약

### 분류 판단 기준
1. **workplace_harassment**: 괴롭힘 성립/불성립 자체가 결론에 직접 영향을 미치는 경우
2. **disciplinary_severity**: 괴롭힘 성립은 전제이고, 해고/감봉 등 양정의 적정성이 핵심인 경우
3. **transfer_validity**: 괴롭힘 관련 분리 조치로서의 전보 정당성이 핵심인 경우
4. **not_really_harassment_case**: 괴롭힘이 배경 사실·방어논리·비교 대상에 불과한 경우

### 특이 사건
- **id_346885**: 견책(정당) + 전보(부당) 일부인용. primary를 workplace_harassment로 분류 (괴롭힘 성립이 견책의 전제)
- **id_347141**: 괴롭힘 '후속조치 불이행'이 징계사유. harassment_investigation으로 분류
- **id_347391**: 진정 제기를 징계사유로 삼는 것의 보복 금지 법리 포함. retaliation을 secondary에 추가

## confidence 분포
- high: 30건 (전량)

## 주의사항
- 성희롱+괴롭힘 복합 사건(id_346923, id_347167, id_347173, id_347389 등)은 성희롱 검색에서도 노출되도록 include_for_queries에 반영
- 전보 사건은 전보 3요소(업무상필요성, 생활상불이익, 협의절차) 충족 여부를 retrieval_note에 명시
