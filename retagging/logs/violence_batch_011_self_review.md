# violence_batch_011_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건 (id_20913 ~ id_21787)
- legacy_reason_category에 "violence" 포함된 사례 모음
- 중점: misconduct vs disciplinary_severity 구분

## 핵심 판단 기준: misconduct vs disciplinary_severity
- **misconduct**: 비위행위 자체가 중하여 징계(해고 포함) 정당성이 인정되는 경우
- **disciplinary_severity**: 비위행위는 인정되나 양정이 과하여 부당한 경우
- 결론이 "양정 과다 → 부당"이면 disciplinary_severity, "사유 정당 + 양정 적정"이면 misconduct

## violence 배치이나 실질 쟁점이 다른 사례 (exclusion 부여)

### 해고부존재/사직 사건 (3건)
- **id_20913**: 사직서 자발성. 본문에 폭행 사실 없음 → dismissal_validity + resignation_dispute
- **id_21239**: 사직서 합의해지. 본문에 폭행 사실 없음 → dismissal_validity + resignation_dispute
- **id_2119**: 차량열쇠 반납=승무정지, 해고 아님 → dismissal_validity + resignation_dispute
- **id_21117**: 수습근로자 폭언·협박 후 사직 → dismissal_validity + resignation_dispute

### 절차 하자가 결론을 가른 사례 (3건)
- **id_21241**: 노인학대 해고 실체 정당이나 해고사유 미기재 → procedure + procedure_dominant
- **id_21393**: 욕설 징계사유 인정이나 재심 소명기회 미부여 → procedure + procedure_dominant
- **id_21619**: 폭행 사유 인정이나 징계위 가부동수 의결요건 미충족 → procedure + procedure_dominant

## misconduct (사유 정당 + 양정 적정) — 13건
| case_id | 처분 | 핵심 |
|---------|------|------|
| id_20925 | 징계해고 | 수습 중 상사 모욕·협박 |
| id_20943 | 정직 1월 | 음주 폭언·폭행 반복 |
| id_20961 | 감봉 | 근무외 폭행·욕설 |
| id_21023 | 정직 | 폭행·재물손괴 형사 유죄 |
| id_21143 | 해고 | 반복 비위(폭행·욕설 전력) |
| id_21165 | 본채용 거부 | 수습 중 폭행+무단결근+평가미달 |
| id_21187 | 해임 | 지위 이용 반인륜적 폭행 |
| id_21399 | 정직 30일 | 인사담당자 폭언 |
| id_21495 | 당연퇴직 | 소주병 폭행 집행유예+전과3회 |
| id_21523 | 징계해고 | 폭행+무단결근 14일 |
| id_21663 | 징계해고 | 선후배 심한 욕설 |
| id_2177 | 해고 | 업무거부+모욕+무단녹취 |
| id_21787 | 해고 | 전치21주 중상해+은폐 |

## disciplinary_severity (양정 과다) — 7건
| case_id | 처분 | 핵심 |
|---------|------|------|
| id_20933 | 징계해고 | 폭행 양정 과다 + 부당노동행위 |
| id_2095 | 해고 | 우발적 폭행, 비교사례 형평성 |
| id_20975 | 해고 | 도구 위협이나 실제 상해 없음 |
| id_21121 | 본채용거부 | 1회 폭언으로 4년 근속자 거부 |
| id_21223 | 해고 | 6개 사유 중 2개만 인정 |
| id_21333 | 징계해고 | 쌍방 폭행 일방만 징계 형평성 |
| id_21471 | 해고 | 쌍방 폭행 형평성 위반 |

## 기타 분류
| case_id | primary | 핵심 |
|---------|---------|------|
| id_21675 | disciplinary_severity | 정직6월 양정 과다 (상사 모욕+업무거부) |
| id_21779 | misconduct | 부하 폭행+경비 비위 정직2월 정당 |
| id_21785 | misconduct | 여성 폭언·권한남용 정직3월 정당 |

## disposition_type 분포
- disciplinary_dismissal: 15건
- dismissal: 5건 (해고부존재 포함)
- suspension: 8건 (정직)
- pay_cut: 1건 (감봉)
- probation_termination/rejection_of_regular_employment: 2건
- no_formal_disposition: 1건

## 산업 맥락 식별
- healthcare: id_21121 (간호사), id_21241 (요양원)
- transport: id_2119 (차량운전), id_21393 (정비), id_21619 (승무)
- service: id_20925 (아파트 관리), id_21143
- manufacturing: id_21675 (공장 설비)
- public: id_21495 (지방자치단체 재단)
- 나머지: unknown

## 신뢰도
- high: 28건 (사실관계·쟁점이 명확)
- medium: 0건
- low: 0건
- 전체적으로 source_text가 상세하여 high 비율 높음

## 특이사항
- id_20913, id_21239: violence 배치이나 본문에 폭행 사실이 전혀 없음 (legacy 태깅 오류 가능성)
- id_21241: 실체 정당+절차 부당의 전형적 사례. 검색 시 "절차 하자 부당해고"와 "노인학대 해고" 양쪽에 노출 필요
- id_21471, id_21333: 쌍방 폭행 형평성 문제가 동일 패턴
