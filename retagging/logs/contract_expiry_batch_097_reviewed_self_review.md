# contract_expiry_batch_097_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_097_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_48665` [discrimination]
  - 변경: notes
  - notes: 정년 연장 기대권은 인정되지 않으나, 계약직(촉탁직) 재고용 기대권이 인정됨에도 불구하고 합리적 이유가 없으므로 부당하고, 부당노동행위에 해당하
- `id_48677` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로자로 볼 수 없고 기간제 근로계약에 따른 근로계약 갱신기대권도 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및
- `id_48703` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자에 해당하나 근로계약의 갱신기대권이 존재한다고 보기 어려워 계약기간 만료로 고용관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대
- `id_48705` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['dismissal_validity', 'workplace_harassment']
  - notes: 근로자들에게 근로계약 갱신기대권이 인정되고, 근로자1에 대한 근로관계 종료는 갱신거절에 합리적인 이유가 있어 근로계약기간 만료로 정당하게 종료되
- `id_48709` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되나 갱신 거절에 합리적 이유가 인정되므로 계약기간 만료에 따른 근로계약 종료는 정당하다고 판정한 사례 — 갱신기대권

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
