# contract_expiry_batch_081_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_081_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_412175` [dismissal_validity]
  - 변경: notes
  - notes: 해고 사유의 정당성이 인정되지 않고 해고의 절차도 적법하지 않으므로 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_412177` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않아 근로계약기간 만료를 사유로 근로관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신
- `id_412179` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되나 갱신거절의 합리적 이유가 존재하여 근로계약 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및
- `id_412183` [renewal_expectation]
  - 변경: notes
  - notes: 계약기간만료 사유가 발생한 것으로 보여 해고로 볼 수 없고, 해고로 보더라도 구제이익이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 
- `id_412205` [renewal_expectation]
  - 변경: notes
  - notes: 촉탁직 근로계약에 대한 갱신 기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
