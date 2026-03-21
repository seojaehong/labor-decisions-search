# contract_expiry_batch_024_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_024_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_24567` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되는 근로자들에게 합리적 이유 없이 근로계약을 거절한 것은 부당해고라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신
- `id_24569` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로계약 갱신기대권이 인정되지 않아 계약기간 만료로 인한 근로관계 종료라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_24581` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_24597` [dismissal_validity]
  - 변경: notes
  - notes: 근로자들은 일용직이 아닌 기간제근로자임에도 불구하고 구두해고 통보한 것은 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 
- `id_24603` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 계약갱신의 요건 및 절차에 관한 규정 없이 직원의 근무태도 등에 따라 사용자가 재량으로 계약 갱신을 결정해 온 점 등을 고려해 볼 때, 근로자에

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
