# contract_expiry_batch_004_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_004_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_11841` [renewal_expectation]
  - 변경: notes
  - notes: 당사자 간 근로관계는 계약기간이 만료됨으로써 종료되었고, 근로자에게 근로계약의 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여
- `id_1185` [renewal_expectation]
  - 변경: notes
  - notes: 변경된 위탁업체에게 고용승계 의무가 있다거나 근로자들에게 고용승계 기대권이 형성되었다고 볼 수 없어 사용자 적격이 없다고 판정 — 갱신기대권 성
- `id_11865` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 근로자에게 근로계약에 대한 갱신기대권이 존재하고 사용자의 갱신 거절에는 합리적 이유가 없어 근로계약 종료는 부당하다고 판정한 사례 — discr
- `id_1189` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자의 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_11891` [dismissal_validity]
  - 변경: notes
  - notes: 사용자가 서면통지 의무를 위반하여 근로자에게 행한 해고가 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
