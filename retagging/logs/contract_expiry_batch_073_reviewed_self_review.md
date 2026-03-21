# contract_expiry_batch_073_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_073_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_406393` [renewal_expectation]
  - 변경: notes
  - notes: 사업장에 근로계약을 반복 갱신하는 관행이 정립된 것으로 보아 근로자에게 근로계약이 갱신될 수 있으리라는 정당한 기대권이 인정되며, 사용자가 근로
- `id_406405` [renewal_expectation]
  - 변경: notes
  - notes: 기각: 갱신기대권 인정안됨 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_406417` [dismissal_validity]
  - 변경: notes
  - notes: 시용기간에 대하여 업무 적격성 여부를 평가한 후 본채용 거부를 하면서 구체적？실질적 거부 사유를 서면으로 통지하지 않아 절차적으로 위법하여 부당
- `id_406427` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 근로계약의 갱신기대권이 인정되고, 사용자의 갱신 거절에는 합리적인 이유가 없다고 판정한 사례 — discrimination 판단이 핵심
- `id_406441` [dismissal_validity]
  - 변경: notes
  - notes: 근로자들에게 행한 계약해지는 정당한 사유가 있으나 해고서면통지에 하자가 있어 해고가 부당하고, 근로자들이 해고의 효력을 다투는 중 근로계약이 만

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
