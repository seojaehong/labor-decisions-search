# contract_expiry_batch_100_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_100_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_50105` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약에 관한 갱신기대권이 인정되지 않으므로 근로계약기간 만료로 근로관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱
- `id_50129` [renewal_expectation]
  - 변경: notes
  - notes: 당사자 간 근로관계는 계약기간 만료로 종료되었으며, 근로자에게 근로계약의 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및
- `id_50143` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 촉탁직 재고용에 관한 기대권은 인정되나 사용자의 근로자에 대한 촉탁직 재고용 거부에는 합리적 이유가 있다고 판정한 사례 — 갱신기대권
- `id_50175` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않아 근로계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_50217` [dismissal_validity]
  - 변경: notes
  - notes: 근로자는 시용근로자에 해당하고, 본채용 거부 사유가 정당하나, 본채용 거부 사유와 시기를 서면으로 통지하지 않아 본채용 거부의 절차상 하자가 있

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
