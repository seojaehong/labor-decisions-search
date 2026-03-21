# contract_expiry_batch_016_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_016_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_19887` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'training_opportunity', 'dismissal_validity']
  - notes: 기간의 정함이 있는 근로계약을 체결하였고, 갱신기대권이 인정되지 않아 근로계약기간 만료로 근로관계가 정당하게 종료되었다고 판정한 사례 — 갱신기
- `id_19911` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되나 갱신 거절에 합리적인 이유가 있어 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_19913` [unfair_treatment]
  - 변경: notes, secondary:['dismissal_validity']→['renewal_expectation', 'dismissal_validity']
  - notes: 단체협약의 규정에 따라 적격심사를 거쳐 정년이 도래한 근로자를 촉탁직으로 재고용하지 않은 것은 정당하고, 부당노동행위에 해당하지 않는다고 판정한
- `id_19921` [dismissal_validity]
  - 변경: notes
  - notes: 기간제법 사용기간 제한의 예외에 해당하지 않는 기간의 정함이 없는 근로자에게 행한 근로계약기간 만료 통지는 부당해고라고 판정한 사례 — 해고 사
- `id_19925` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity'], conf:high→medium
  - notes: 기간제근로자로서 갱신기대권이 인정되고 갱신 거절의 합리적 이유가 없어 위촉기간 만료로 고용관계를 종료한 것은 부당해고라고 판정한 사례 — dis

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
