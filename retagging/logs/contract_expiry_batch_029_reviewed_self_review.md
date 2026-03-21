# contract_expiry_batch_029_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_029_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_2749` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들의 고용승계 기대권이 인정되고, 고용승계 거절에 합리적인 이유가 없다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_27517` [renewal_expectation]
  - 변경: notes
  - notes: 사용자가 근로자에게 해고를 통보한 것이 아니라 근로계약기간 만료 시점에 이르러 근로관계가 자동으로 종료됨을 통지한 것이며, 근로계약서나 취업규칙
- `id_27527` [renewal_expectation]
  - 변경: notes
  - notes: 계약기간의 정함이 있는 근로자의 갱신기대권이 인정되지 않아 당연히 근로관계가 종료된다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성
- `id_27531` [dismissal_validity]
  - 변경: notes
  - notes: 비등기이사라도 임금을 목적으로 근로를 제공하였다면 「근로기준법」상 근로자로 인정하고 계약만료에 따른 해고가 정당하지 않다고 판정한 사례 — 해고
- `id_27539` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되지 아니하므로 계약기간 만료에 따라 근로계약이 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
