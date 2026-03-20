# violence_batch_014_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, violence 배치
- 중점: misconduct vs disciplinary_severity 구분
- 핵심 판단기준: 비위행위 자체의 존부/중대성이 쟁점이면 misconduct, 비위 인정 후 양정 적정성이 쟁점이면 disciplinary_severity

## 태깅 요약 통계

| issue_type_primary | 건수 |
|---|---|
| disciplinary_severity | 16 |
| misconduct | 5 |
| dismissal_validity | 5 |
| procedure | 2 |
| transfer_validity | 1 |
| unfair_treatment | 1 |
| 총 | 30 |

## violence 배치이나 primary가 폭행/폭언 관련 아닌 사건 (8건)

### id_23731 — primary: dismissal_validity
- 무단결근+배임이 해고사유. 폭행·폭언 쟁점 없음
- 해고사유 전부 불인정 → 부당해고
- exclusion_flags: not_really_absence_case, fact_specific_low_reusability

### id_23733 — primary: dismissal_validity
- 점장과 다툼은 배경사실. 해고 존부(자진사직)가 유일 쟁점
- exclusion_flags: resignation_dispute, unrelated_to_dismissal

### id_23849 — primary: unfair_treatment
- 부당노동행위(지배개입) 사건. 파업 중 급여명세서 발송
- 폭행·폭언 쟁점 전혀 없음
- exclusion_flags: unrelated_to_dismissal

### id_24027 — primary: dismissal_validity
- 캐디 전환 합의해지 유효 여부. 폭행은 전환 과정 중 배경
- exclusion_flags: resignation_dispute, settlement_or_mutual_termination, unrelated_to_dismissal

### id_24121 — primary: transfer_validity
- 대기발령의 징벌성·정당성이 핵심. 협박은 사용자 주장의 사유일 뿐
- exclusion_flags: unrelated_to_dismissal

### id_24223 — primary: dismissal_validity
- 명예퇴직 형태 합의해지 유효 여부. 폭행·폭언 쟁점 없음
- exclusion_flags: resignation_dispute, unrelated_to_dismissal

### id_24375 — primary: dismissal_validity
- 해고 부존재 입증이 쟁점. 폭행도 증거불충분(검찰 혐의없음)
- exclusion_flags: resignation_dispute, unrelated_to_dismissal

### id_2451 — primary: procedure
- 소명기회 미부여가 핵심 절차 하자. 모바일 커뮤니티 글이 비위
- exclusion_flags: procedure_dominant

## misconduct를 primary로 선택한 5건

### id_23691 — misconduct
- 기망(사직약속 불이행)이라는 비위행위 존부가 핵심
- 선행 성희롱·폭언 감경 후 사직 불이행 = 독립적 비위

### id_23699 — misconduct
- 복합 중대 비위(폭행 유죄판결+협박+허위신고+자료삭제)
- 비위 존부·중대성 자체가 핵심, 양정은 부차적

### id_24097 — misconduct
- 장기간 다수 피해자 괴롭힘 + 동료 자살 배경
- 비위의 중대성이 압도적. workplace_harassment를 secondary에 포함

### id_24289 — misconduct
- 4개 유형 복합 비위(예산전용+성희롱+폭언+월권)
- 비위 존부와 중대성이 핵심

### id_24439 — misconduct
- 학력사칭+경력허위+불량반복+폭언+지시불이행
- 다수 비위의 존부와 개전의 정 없음이 핵심

## disposition_type 분포

| 유형 | 건수 |
|---|---|
| disciplinary_dismissal | 18 |
| suspension | 6 |
| no_formal_disposition | 4 |
| pay_cut | 2 |
| reprimand | 1 |
| demotion | 1 |
| transfer | 1 |
| other | 1 |
| (중복 포함: id_24367 suspension+disciplinary_dismissal) | — |

## industry_context 식별된 사건
- transport: id_23617, id_24097, id_24393
- healthcare: id_23699
- manufacturing: id_23945, id_24205
- education: id_24019, id_24367
- retail: id_23733
- it: id_23909
- service: id_24027, id_24289

## 검색 품질 관련 exclusion_flags 부여 사건 (9건)
- id_23731: not_really_absence_case, fact_specific_low_reusability
- id_23733: resignation_dispute, unrelated_to_dismissal
- id_23849: unrelated_to_dismissal
- id_24027: resignation_dispute, settlement_or_mutual_termination, unrelated_to_dismissal
- id_24121: unrelated_to_dismissal
- id_24223: resignation_dispute, unrelated_to_dismissal
- id_24357: procedure_dominant
- id_24367: fact_specific_low_reusability
- id_24375: resignation_dispute, unrelated_to_dismissal
- id_2451: procedure_dominant

## 주의 사항 / 재검토 필요 사건

### id_23849 — confidence: high (but violence 배치 부적합)
- 부당노동행위(지배개입) 사건으로 violence와 무관
- legacy tag에 violence가 있었으나 실질 쟁점 불일치

### id_24367 — 구제이익 부존재 각하 사건
- 본안(해고 정당성) 판단 없음. 직무정지 효력 소멸만 판단
- fact_specific_low_reusability 부여

## misconduct vs disciplinary_severity 판단 근거 요약

| 기준 | misconduct | disciplinary_severity |
|---|---|---|
| 비위 존부 다툼 | O | X (인정됨) |
| 비위 중대성 자체 | 핵심 | 부차적 |
| 양정 적정성 | 부차적 | 핵심 |
| 형평(비교대상) | - | 주요 근거 |
| 이번 배치 건수 | 5 | 16 |
