# violence_batch_012_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건 (id_21795 ~ id_22713)
- legacy_reason_category에 "violence" 포함된 사례 모음
- 중점: misconduct vs disciplinary_severity 구분

## 핵심 판단 기준: misconduct vs disciplinary_severity
- **misconduct**: 비위행위 자체가 중하여 징계(해고 포함) 정당성이 인정되는 경우
- **disciplinary_severity**: 비위행위는 인정되나 양정이 과하여 부당한 경우
- 결론이 "양정 과다 -> 부당"이면 disciplinary_severity, "사유 정당 + 양정 적정"이면 misconduct

## violence 배치이나 실질 쟁점이 다른 사례 (exclusion 부여)

### 해고부존재/사직 사건 (4건)
- **id_22091**: 사직 의사표시 자발성. 본문에 폭행 사실 없음 -> dismissal_validity + resignation_dispute
- **id_22595**: 자필 사직서 합의해지. 본문에 폭행 사실 없음 -> dismissal_validity + resignation_dispute
- **id_2239**: 사직서 수리 합의해지. 본문에 폭행 사실 없음 -> dismissal_validity + resignation_dispute
- **id_21897**: 부당노동행위(지배개입). 본문에 폭행 사실 없음 -> unfair_treatment

### 폭행이 배경사실에 불과한 사례 (3건)
- **id_22003**: 고용보장 확약 위반 해고 + 부당노동행위. 폭행 사실 없음 -> dismissal_validity
- **id_22017**: 질병휴직 후 미복직 면직. 동료 폭행 주장은 혐의없음 처분 -> absence_without_leave
- **id_2223**: CCTV 무단 열람 강등. 모욕 주장 불인정, 폭행 없음 -> disciplinary_severity

### 절차 하자가 결론을 가른 사례 (1건)
- **id_22213**: 녹화자료 손괴 징계사유 인정이나 징계위원회 미개최 -> procedure + procedure_dominant

## misconduct (사유 정당 + 양정 적정) -- 12건
| case_id | 처분 | 핵심 |
|---------|------|------|
| id_21925 | 징계해고 | 소규모 재단 5가지 비위(기밀누설+폭언+형사고발) |
| id_22031 | 해고 | 반말+업무방해+무단결근+욕설 복합 비위 |
| id_22069 | 정직3월 | 법원 확정판결 반영 재징계 적정 |
| id_22107 | 징계해고 | 성희롱+무고+협박 복합 비위 |
| id_22153 | 정직 | 상습적 폭언·위협+반복 징계전력 |
| id_22165 | 징계해고 | 소규모 사업장 관리자 모욕+험담 |
| id_22373 | 해고 | 무단결근+노조위원장 폭행 |
| id_22463 | 징계해고 | 하급자 폭언+보상금유용+허위기록 |
| id_22485 | 직무정지2월 | 장애인 거주인 폭언+동료 상해 |
| id_22513 | 정직7일 | 상급자 욕설·폭언 |
| id_22691 | 정직6월 | 특수폭행 벌금+교통사고 반복 |
| id_22713 | 해고 | 9개월 17회 반복 비위+상사 욕설+기물훼손 |

## disciplinary_severity (양정 과다) -- 9건
| case_id | 처분 | 핵심 |
|---------|------|------|
| id_21795 | 감봉2월 | 폭행 사유 인정이나 유사 전례 대비 형평성 위반 |
| id_21941 | 해고 | 업무능력 부족, 사용자 교육 노력 없음 |
| id_22025 | 해고 | 대표이사 모욕 형사유죄이나 해고는 과다 |
| id_22071 | 해고 | 단체대화방 임원 비방, 해고는 과다 |
| id_22215 | 해고 | 쌍방 폭행 일방만 징계 형평성 |
| id_22257 | 해고 | 폭행 피해자 해고 vs 가해자 감봉 형평성 |
| id_2253 | 해고 | 아동학대(정서적) 고의성 낮음+혐의없음 |
| id_22671 | 정직1월 | 가해자(유죄확정)와 동일 처분 형평성 |
| id_22685 | 해고 | 사업장 외부 우발적 폭행, 22년 무징계 근속 |

## 기타 분류
| case_id | primary | 핵심 |
|---------|---------|------|
| id_21897 | unfair_treatment | 지배개입 부당노동행위(급여명세서 발송) |
| id_21991 | unfair_treatment | 사용자 해당성 부정, 부당노동행위 불성립 |
| id_22003 | dismissal_validity | 고용보장 확약 위반 해고+부당노동행위 |
| id_22017 | absence_without_leave | 질병휴직 후 미복직 면직 |
| id_22091 | dismissal_validity | 사직 의사표시 해고부존재 |
| id_22213 | procedure | 징계위원회 미개최 절차위반 |
| id_22595 | dismissal_validity | 사직서 합의해지 |
| id_2223 | disciplinary_severity | CCTV 무단 열람 강등 양정 과다 |
| id_2239 | dismissal_validity | 사직서 수리 합의해지 |

## disposition_type 분포
- disciplinary_dismissal: 16건
- dismissal: 5건 (해고부존재 포함)
- suspension: 6건 (정직/직무정지)
- pay_cut: 1건 (감봉)
- demotion: 1건 (강등)
- no_formal_disposition: 1건
- other: 1건

## 산업 맥락 식별
- education: id_21925 (재단법인), id_22107 (교육), id_2253 (아동)
- healthcare: id_22485 (장애인 시설), id_22671 (병원)
- transport: id_21991 (운전원), id_22691 (운전원)
- manufacturing: id_22215 (공장), id_22257 (제조), id_22513 (절삭유 공장)
- it: id_21897 (IT), id_22165 (IT)
- public: id_22017 (공공기관), id_22069 (공공기관), id_2223 (수련원)
- 나머지: unknown

## 신뢰도
- high: 30건 (전건)
- source_text가 상세하여 전건 high 부여

## 특이사항
1. **legacy 태깅 오류 다수**: id_21897, id_22003, id_22091, id_22595, id_2239 등 5건은 본문에 폭행 사실이 전혀 없음
2. **형평성(comparative_fairness) 패턴 빈출**: id_21795, id_22215, id_22257, id_22671 등 4건이 비교 사례 대비 형평성 위반 논거
3. **쌍방 폭행 형평성**: id_22215(폭행), id_22257(가해자 감봉 vs 피해자 해고)이 동일 패턴
4. **사직서 자발성 3건 클러스터**: id_22091, id_22595, id_2239 모두 사직서 철회 불가 판정
5. **성희롱 사건 1건**: id_22107 - violence 배치이나 실질은 강제추행 징계해고
6. **비해고 징계 7건**: 정직(5)+직무정지(1)+강등(1)+감봉(1) - unrelated_to_dismissal 플래그 부여

## misconduct vs disciplinary_severity 판단 요약
- 이 배치에서 양정 과다(disciplinary_severity)로 분류한 9건 중 형평성 위반이 4건으로 가장 빈번한 패턴
- misconduct 12건 중 복합 비위(3가지 이상 사유)가 7건으로 다수
- violence 배치임에도 직접 폭행이 핵심인 사례는 약 절반(15건 내외), 나머지는 폭언·모욕·험담 또는 배경사실에 불과
