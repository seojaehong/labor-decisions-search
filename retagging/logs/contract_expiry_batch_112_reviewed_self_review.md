# contract_expiry_batch_112_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_112_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_56515` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되나, 사용자의 근로계약 갱신거절에 합리적 이유가 존재하지 않아 기간만료로 근로관계를 종료한 것은 부당해고
- `id_56517` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 만료 시 근로계약이 갱신된다는 신뢰 관계가 형성되어 있다고 볼 수 없으므로 근로계약 만료에 따라 근로관계가 종료된 것이라고 판정한 사례
- `id_56519` [dismissal_validity]
  - 변경: notes
  - notes: 근로자는 무기계약직 근로자로 전환되었고, 근로관계 종료의 정당성이 없으므로 근로관계 종료는 부당해고라고 판정한 사례 — 해고 사실 자체의 존부 
- `id_56533` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 촉탁직 재고용 기대권이 인정되지 않아 정년 도달에 따른 근로관계 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 
- `id_56545` [discrimination]
  - 변경: notes, secondary:['procedure', 'worker_status', 'dismissal_validity']→['procedure', 'worker_status', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자는 기간의 정함이 있는 근로자로서 근로계약의 갱신기대권이 인정되고 사용자의 갱신거절에는 합리적 이유가 없다고 판정한 사례 — discrim

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
