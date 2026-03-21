# contract_expiry_batch_084_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_084_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_41553` [dismissal_validity]
  - 변경: notes, secondary:[]→['disciplinary_severity']
  - notes: 정년도달로 근로관계가 종료되었고, 촉탁직 고용에 대한 기대권은 있으나 촉탁직 고용 거절에 합리적인 이유가 있다고 판정한 사례 — 해고 사실 자체
- `id_41583` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 해고의 증거로 제시한 자료만으로는 이 사건 해고가 존재한다는 단정을 할 수 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유
- `id_41593` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로자이며, 근로계약 갱신기대권이 인정되지 않아 근로계약 기간 만료로 근로관계가 종료되었다고 판단한 사례 — 갱신기대권 성립
- `id_41623` [dismissal_validity]
  - 변경: notes
  - notes: 취업규칙상 근로계약기간은 2년이므로 근로계약서상 근로계약기간 1년 만료를 이유로 근로관계를 종료한 것은 부당하다고 판정한 사례 — 해고 사실 자
- `id_41633` [dismissal_validity]
  - 변경: notes
  - notes: 근로자의 근로계약은 기간만료로 종료되었고 근로계약이 갱신되었다거나 근로계약이 갱신된다는 신뢰관계가 형성되었다고 보기 어렵다고 판정한 사례 — 해

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
