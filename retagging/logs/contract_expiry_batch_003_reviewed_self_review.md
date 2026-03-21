# contract_expiry_batch_003_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_003_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_11153` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 정년 후 재고용기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_11207` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않으므로 계약기간만료로 근로관계가 종료되어 해고가 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱
- `id_11217` [discrimination]
  - 변경: notes, secondary:['unfair_treatment', 'dismissal_validity', 'renewal_expectation']→['unfair_treatment', 'renewal_expectation', 'dismissal_validity']
  - notes: 징계사유가 인정되지 않아 견책처분은 부당하고, 촉탁 재고용의 갱신기대권이 인정되고 갱신거절의 합리적 이유가 없으므로 촉탁계약 갱신거절은 부당해고
- `id_11239` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들은 기간제근로자에 해당하나 근로계약에 관한 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_1125` [dismissal_validity]
  - 변경: notes
  - notes: 무기계약직으로 전환된 근로자에 대한 계약기간 만료는 해고이며, 해고사유와 절차가 적법하지 아니하여 부당한 해고로 판정한 사례 — 해고 사실 자체

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
