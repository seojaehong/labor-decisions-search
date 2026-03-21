# contract_expiry_batch_068_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_068_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_403691` [dismissal_validity]
  - 변경: notes
  - notes: 사용자가 일방적으로 근로관계를 종료하였다고 볼 수 없어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_403693` [dismissal_validity]
  - 변경: notes
  - notes: 일용근로자로서 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_4037` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 있고, 근로계약 갱신거절의 합리적인 이유가 없어 부당해고라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_403701` [renewal_expectation]
  - 변경: notes
  - notes: 이 사건 근로자에 대하여는 기간제 근로계약의 갱신기대권을 인정하기 어려울 뿐만 아니라 갱신거절의 합리적 이유도 존재하는 것으로 보이므로 부당해고
- `id_403721` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 수탁기관 변경에 따른 고용승계 관행이 존재하지 않고, 고용승계에 관한 신뢰관계가 형성되어 있다고 볼 만한 증거도 없어, 고용승계 기대권이 인정되

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
