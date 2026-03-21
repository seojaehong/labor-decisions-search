# contract_expiry_batch_080_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_080_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_411503` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 1일 단위로 근로계약을 체결한 일용직 근로자로 판단되고, 이미 근로계약관계가 종료된 일용직에 대하여는 해고가 성립하지 아니하므로 해고는
- `id_411515` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계 종료 사유가 계약기간 만료로 종료된 것으로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_411517` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권은 인정되나 갱신거절의 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_411533` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 정년 이후 재고용 기대권이 인정되나, 재고용 거절에 합리적인 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이
- `id_411535` [dismissal_validity]
  - 변경: notes
  - notes: 근로자는 기간제근로자이고, 사용자와 원청사 간의 도급계약이 종료됨에 따라 근로계약이 종료된 것이므로 해고는 존재하지 않는다고 판정한 사례 — 해

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
