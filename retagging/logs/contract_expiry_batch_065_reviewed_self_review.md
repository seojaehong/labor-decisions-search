# contract_expiry_batch_065_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_065_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_401549` [renewal_expectation]
  - 변경: notes
  - notes: 피신청인 적격은 사용자1에게 있고, 정년퇴직자 촉탁직 재고용 기대권이 인정되지 않으므로 정년 도래로 인한 근로관계 종료는 정당하다고 판정한 사례
- `id_401553` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 종료로 근로기준법상 해고로 보기 어려워 해고가 존재하지 않는 것으로 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_401555` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되나, 갱신거절에 합리적인 이유가 존재하므로 근로계약 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거
- `id_401559` [renewal_expectation]
  - 변경: notes
  - notes: (주위적 청구) 근로계약 만료 이후 구제신청을 한 것이므로 구제이익이 존재하지 않으며, (예비적 청구) 근로계약 갱신기대권이 인정되나, 갱신거절
- `id_401627` [dismissal_validity]
  - 변경: notes
  - notes: 근로자는 1일 단위로 근로관계가 종료되는 일용근로자에 해당하므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
