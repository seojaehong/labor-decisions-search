# probation_batch_008_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, 모두 legacy_reason_category에 "probation" 포함
- rejection_of_regular_employment (본채용 거부): 23건
- unrelated_to_probation (수습은 배경일 뿐): 5건
- 기타(구제이익 소멸 등): 2건

## 핵심 분류 기준: rejection_of_regular_employment vs unrelated_to_probation

| 판단 | 기준 | 해당 건 |
|------|------|---------|
| rejection_of_regular_employment | 수습/시용기간 중 또는 만료 시 본채용 거부가 핵심 쟁점 | 23건 (대다수) |
| unrelated_to_probation | 수습이 배경이나 실질 쟁점이 해고 존부, 사직, 인원감축 등 | id_21117, id_21607, id_21855, id_21979, id_21985 |

## unrelated_to_probation 판정 건 상세

### id_21117
- 수습기간 중이나 핵심은 해고 존부(근로자 폭언·협박 후 자진퇴직)
- disposition: no_formal_disposition
- exclusion_flags: resignation_dispute, unrelated_to_probation

### id_21607
- 수습기간 중이나 핵심은 해고 존부(사직 권고에 이의 없이 응한 묵시적 합의해지)
- disposition: no_formal_disposition
- exclusion_flags: resignation_dispute, unrelated_to_probation

### id_21855
- 수습평가 면담 중이나 핵심은 사용자 적격 + 해고 존부(출근 불응)
- disposition: no_formal_disposition
- exclusion_flags: resignation_dispute, unrelated_to_probation

### id_21979
- 수습근로계약이 존재하나 실제 해고 사유는 도급회사 인원감축 지시
- disposition: dismissal (본채용 거부가 아닌 일반 해고)
- exclusion_flags: unrelated_to_probation

### id_21985
- 수습기간 중간평가 불량 통보가 계기이나 해고 존부(자진퇴직)가 핵심
- disposition: no_formal_disposition
- exclusion_flags: resignation_dispute, unrelated_to_probation

## id_21775 — 구제이익 소멸 (특수)
- 수습 본채용 거부가 배경이나, 판단 핵심은 복직명령 후 구제이익 존부
- issue_type_primary: other
- exclusion_flags: unrelated_to_probation, fact_specific_low_reusability

## 절차 우위 사례 (procedure_dominant)
- id_21037: 실체적 사유 인정되나 서면통지 추상적 기재로 부당
- id_21253: 구체적 본채용 거부 사유 서면 미통지로 부당

## 주목할 사례

### id_21915 — 입사 3일 본채용 거부
- 극단적으로 짧은 근무기간(3일)에서의 본채용 거부
- 업무능력 판단 불가능한 기간임을 명시

### id_21729 — 장애인 차별적 수습평가
- 장애인 전형 채용자를 일반인과 동일 기준으로 평가
- 인사위원회 재투표 등 절차 하자 복합

### id_22147 — 수습평가 객관성·공정성 기준 상세 제시
- 평가규정 부재, 비계량 지표, 1인 평가, 기준 미고지 등 구체적 판단 기준

### id_22035 — 시용기간 도과 후 본채용 거부
- 시용기간 만료 후 본채용 거부의 위법성 판단 (2인 병합, 상반 결론)

## 산업 분포
- unknown: 14건
- service: 6건
- healthcare: 2건
- education: 2건
- finance: 1건
- transport: 2건
- public: 1건
- construction: 1건
- manufacturing: 1건

## 결과 분포
- 구제 인용(granted/upheld): 16건
- 기각(dismissed): 9건
- 각하(rejected): 1건
- 초심취소(overturned): 2건
- 기타: 2건
