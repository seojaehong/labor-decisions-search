# contract_expiry_batch_108_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_108_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_54693` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 갱신기대권이 인정되지 않고 계약기간 만료에 따라 근로관계가 종료된 것이므로 부당해고가 아니라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_54697` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않고, 근로관계 종료는 불이익 취급 및 지배？개입의 부당노동행위가 아니다고 판정한 사례 — 갱신기대권 성립 여부
- `id_54715` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity'], conf:high→medium
  - notes: 근로자들에게 징계사유가 모두 인정되지 않아 징계는 부당하고, 근로자1에게 근로계약의 갱신기대권이 인정되며 갱신거절에 합리적 이유가 없어 부당한 
- `id_54751` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 체결에 대한 정당한 갱신기대권이 인정되지만 갱신거절의 합리적 사유가 있어 근로계약 만료는 부당해고에 해당하지 않는다고 판정한 사례 — 
- `id_54753` [dismissal_validity]
  - 변경: notes
  - notes: 당사자 간 고용관계는 2022. 12. 31. 근로계약기간 만료로 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
