# contract_expiry_batch_013_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_013_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_17719` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되지 않으므로 계약기간 만료로 근로관계가 종료된 것으로 보아 기각 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합
- `id_1773` [dismissal_validity]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로계약을 체결한 근로자에게 정당한 사유 없이 구두로 근로계약 종료를 통보한 것은 부당해고에 해당한다고 판정한 사례 — 해고
- `id_17751` [renewal_expectation]
  - 변경: notes
  - notes: 근로관계가 종료된 후 3개월이 지난 시점에 부당해고 구제신청을 제기하여 제척기간이 도과하였다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_17765` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'training_opportunity', 'dismissal_validity']
  - notes: 갱신기대권이 있음에도 계약기간 만료의 사유로 근로관계를 종료한 것은 부당해고라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_17767` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되나 갱신거절의 합리적 사유가 인정되어 근로계약 갱신거부는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
