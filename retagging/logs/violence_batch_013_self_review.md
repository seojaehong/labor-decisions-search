# violence_batch_013_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, violence 배치
- 중점: misconduct vs disciplinary_severity 구분
- 핵심 판단기준: 비위행위 자체의 존부가 쟁점이면 misconduct, 비위 인정 후 양정 적정성이 쟁점이면 disciplinary_severity

## 태깅 요약 통계

| issue_type_primary | 건수 |
|---|---|
| disciplinary_severity | 20 |
| misconduct | 5 |
| procedure | 1 |
| dismissal_validity | 1 |
| transfer_validity | 1 |
| redundancy | 1 |
| 총 | 30 |
| (missing: id_23609 = disciplinary_severity) | — |

## violence 배치이나 primary가 violence 외인 사건 (5건)

### id_23043 — primary: procedure
- 징계위 사전통지 기간(7일→1일)·방법(서면→문자) 위반이 핵심
- 양정 과다도 인정되나 절차 하자가 더 비중 큼
- secondary에 disciplinary_severity 포함

### id_23143 — primary: transfer_validity
- 폭언 등 비위 주장이 사실 다툼 단계에서 부정됨
- 실질 쟁점은 징계성 전보의 정당성
- exclusion_flags: not_really_harassment_case, fact_specific_low_reusability

### id_23177 — primary: dismissal_validity
- 폭행 후 사직 권고 → 사직서 제출 → 합의해지 유효 여부가 핵심
- 폭행은 배경 사실일 뿐, 징계양정이 쟁점 아님
- exclusion_flags: resignation_dispute, settlement_or_mutual_termination

### id_23355 — primary: redundancy
- 경영상 해고 요건 불비가 핵심
- 욕설 기재는 개인 다이어리로 공표 의사 無 → 징계사유 불인정
- violence 배치이나 실질적 폭행/폭언 쟁점 아님

### id_23073 — primary: disciplinary_severity (but 실제 폭행 없음)
- 생활지도원의 업무상 발언이 "폭언"으로 분류되었으나 실제 인격모독적 수준 미달
- exclusion_flags: not_really_harassment_case, emotional_conflict_not_harassment

## misconduct를 primary로 선택한 5건

### id_2313 — misconduct
- 5개 복합 비위(공금·예산·사적사용·품위손상·괴롭힘) 중 폭언은 일부
- 비위행위 존부 자체가 핵심 + 양정은 부차적

### id_23179 — misconduct (probation)
- 수습기간 해고. 업무적합성 판단이 핵심
- 쌍방폭행+무단결근이 사유

### id_23427 — misconduct
- 당사자적격·제척기간 등 복합 쟁점
- 무단결근·이중취업(육휴중)·모욕이 인정된 비위

### id_23447 — misconduct (probation)
- 수습기간 해고. 지시감독 거부·컴퓨터 반출이 핵심 사유

### id_23477 — misconduct
- 노인학대(30분간 폭행). 비위의 중대성 자체가 핵심
- 양정이 과한지가 아니라 비위 인정이 초점

### id_23553 — misconduct
- 전치 8주 중대 상해(다발 골절·뇌출혈) + 은폐 시도
- 비위의 중대성 자체로 해고 정당성 판단

## disposition_type 분포

| 유형 | 건수 |
|---|---|
| disciplinary_dismissal | 18 |
| suspension | 8 |
| probation_termination | 2 |
| dismissal | 2 |
| pay_cut | 1 |
| reprimand | 1 |
| transfer | 1 |
| (중복 포함: id_22869 3개) | — |

## 주의 사항 / 재검토 필요 사건

### id_22973 — confidence: medium
- 다수 근로자·다수 사유 복합. 개별 양정 판단이 상이하여 요약에 한계

### id_23143 — confidence: medium
- holding_points가 "초심유지" 한 줄. source_text에서 추론 필요

## industry_context 식별된 사건
- transport: id_22869, id_23177, id_23473
- public: id_22973, id_22999, id_23553
- healthcare: id_23447, id_23477
- education: id_23073
- service: id_2313

## 검색 품질 관련 exclusion_flags 부여 사건 (5건)
- id_23073: not_really_harassment_case, emotional_conflict_not_harassment
- id_23143: not_really_harassment_case, fact_specific_low_reusability
- id_23177: resignation_dispute, settlement_or_mutual_termination
- id_23355: not_really_performance_case, fact_specific_low_reusability
- id_23553: (없음 — 중대 폭행으로 검색 적합)
