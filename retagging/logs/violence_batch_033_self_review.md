# violence_batch_033 Self-Review

## 배치 개요
- 입력: `violence_batch_033.jsonl` (17건)
- 출력: `violence_batch_033_reviewed.jsonl`
- 작업일: 2026-03-20

## 통계 요약

| 항목 | 값 |
|------|-----|
| 총 건수 | 17 |
| confidence high | 16 |
| confidence medium | 1 (id_351665) |
| issue_type_primary: misconduct | 10 |
| issue_type_primary: disciplinary_severity | 4 |
| issue_type_primary: transfer_validity | 2 |
| issue_type_primary: procedure | 1 |
| issue_type_primary: renewal_expectation | 1 |
| issue_type_primary: unfair_treatment | 1 |

## misconduct vs disciplinary_severity 판단 근거

| case_id | primary | 판단 근거 |
|---------|---------|-----------|
| id_35135 | transfer_validity | 전보(조장해임) 사안. 비위가 전보 필요성의 배경이나 핵심은 전보 정당성 |
| id_351365 | renewal_expectation | 갱신기대권 존부가 1차 쟁점. 비위는 갱신거절 합리적 사유 근거 |
| id_351381 | misconduct | 음주측정 양성이라는 비위 존부가 핵심. 양정은 운수업 특수성으로 자연 적정 |
| id_351443 | disciplinary_severity | 비위(폭행) 자체는 인정. 우발성·피해자 처벌불원으로 양정 과다가 핵심 |
| id_351527 | misconduct | 괴롭힘 의도 존부가 핵심. 비위 자체가 불인정 → misconduct |
| id_351559 | transfer_validity | 전보 사안. 업무상 필요성 vs 생활상 불이익이 핵심 |
| id_351649 | misconduct | 성희롱 동영상 반복배포 등 비위 존부가 핵심. 반성 거부로 신뢰파탄 |
| id_351665 | unfair_treatment | 부당노동행위(지배개입) 사안. 비위·징계와 무관 |
| id_351669 | disciplinary_severity | 4개 사유 중 1개만 인정 → 인정된 사유 대비 양정 과다가 핵심 |
| id_351757 | misconduct | 수습 중 폭행+허위제보 등 비위 존부가 핵심. 양정은 비위 중대성으로 적정 |
| id_351861 | misconduct | 욕설·몸싸움 비위 존부가 핵심. 정직(해고 아님)으로 양정 적정 |
| id_3521 | misconduct | 개인정보 무단수집·임직원 비방 등 비위 존부가 핵심 |
| id_35217 | misconduct | 사문서 변조·전산 부정조작 등 고의적 업무 부정이 핵심 비위 |
| id_35221 | disciplinary_severity | 6개 사유 중 2개만 인정. 인정된 사유 대비 정직 3월 양정 과다 |
| id_35227 | procedure | 비위·양정 모두 정당하나 절차(소명기회 미부여)가 결정적 하자 |
| id_353 | misconduct | 작업지시 거부·폭언 등 비위 존부가 핵심 |
| id_35305 | disciplinary_severity | 욕설 비위 인정. 경위·경력·무징계이력 대비 강등은 양정 과다 |

## 레거시 violence 태그 검증

- **실제 폭행/폭력 관련**: id_351365(폭행 기소유예), id_351381(음주), id_351443(폭행·골절), id_351757(폭언폭행), id_351861(욕설몸싸움), id_353(폭언), id_35305(욕설)
- **폭언/협박/위협적 언행**: id_35135(협박문자), id_351527(모욕), id_351559(폭언), id_351649(폭언협박), id_3521(위협적 언행), id_35217(상관모욕), id_35221(욕설), id_35227(욕설모욕협박)
- **violence 태그 부적절**: id_351665(부당노동행위 사안, 폭행/폭언 없음)

## 주의 건

1. **id_351665**: 부당노동행위(지배개입) 사안으로 violence 레거시 태그 자체가 오분류. confidence medium 부여.
2. **id_35135, id_351559**: 해고가 아닌 전보(인사명령) 사안. exclusion_flag에 `unrelated_to_dismissal` 추가.
3. **id_351861**: 정직 3개월(해고 아님). `unrelated_to_dismissal` 추가.
4. **id_35227**: 비위·양정 정당하나 절차만으로 부당 판정. `procedure_dominant` exclusion flag 추가.
5. **id_351443 vs id_351381**: 유사 폭행 사안이나 결론 반대. 351443은 우발성+피해자 처벌불원으로 양정 과다, 351381은 운수업 특수성+과거 전력으로 양정 적정.

## 품질 체크리스트

- [x] 모든 필드 스키마 준수
- [x] misconduct vs disciplinary_severity 구분 일관성
- [x] 전보/정직 사안에 unrelated_to_dismissal 플래그
- [x] 부당노동행위 사안 별도 처리
- [x] include_for_queries에 검색 유용 키워드 4개 이상
- [x] summary_short와 holding_summary 차별화
- [x] retrieval_note에 핵심 사실관계 + 결론 논리 압축
