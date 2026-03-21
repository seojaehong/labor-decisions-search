# contract_expiry_batch_103_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_103_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_5169` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 근로계약이 갱신되리라는 신뢰관계가 형성되어 근로자에게 갱신기대권이 인정되며, 근로계약 갱신 거절에 합리적 이유가 없다고 판정한 사례 — disc
- `id_51703` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 기간제 근로자이고, 근로계약의 갱신기대권이 인정되지 않으므로 사용자가 근로자에 대하여 계약 기간 만료로 근로계약을 종료한 것은 정당하다
- `id_51727` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계가 근로계약 기간 만료로 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_51733` [renewal_expectation]
  - 변경: notes
  - notes: 갱신(전환)기대권이 인정되지 않아 근로계약기간 만료로 인한 근로관계 종료는 정당하고, 불이익 취급 및 지배·개입의 부당노동행위에 해당하지 않는다
- `id_51745` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 만 60세 정년 도달에 따른 근로관계 종료는 해고 및 불이익 취급의 부당노동행위에 해당하지 않으며, 같은 취지의 확정된 판정이 있음에도 다시 부

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
