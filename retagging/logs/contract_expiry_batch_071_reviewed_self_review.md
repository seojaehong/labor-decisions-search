# contract_expiry_batch_071_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_071_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_405177` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자는 시용근로자에 해당하고, 본채용 거부에 합리적인 사유가 없으며, 서면 통지 의무를 위반하여 부당하다고 판정한 사례 — 갱신기대권 성립 여
- `id_405189` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 기간제 근로자에 해당하고, 근로계약의 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_40519` [renewal_expectation]
  - 변경: notes
  - notes: 기각 - 당사자 간 근로관계는 계약기간이 만료됨으로써 종료되었고, 근로자에게 근로계약의 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권
- `id_405207` [dismissal_validity]
  - 변경: notes
  - notes: 제척기간을 도과하여 각하 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_405239` [renewal_expectation]
  - 변경: notes
  - notes: 기각: 갱신기대권 인정안됨 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
