# contract_expiry_batch_019_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_019_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_21731` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 기각임원인 이사대우라 하더라도 실질적으로는 「근로기준법」상 근로자에 해당하나, 기간의 정함이 있는 근로자로서 갱신기대권이 인정되지 않아 사용자의
- `id_21751` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않아 계약기간 만료에 따라 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵
- `id_21771` [dismissal_validity]
  - 변경: notes
  - notes: 경영상 해고 요건인 긴박한 경영상 필요성이 인정되지 않아 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_21781` [renewal_expectation]
  - 변경: notes
  - notes: 회사의 규정과 관례에 따라 정규직 근로자로 전환될 수 있는 기대권이 형성되었음에도 사용자가 객관성과 공정성이 결여된 평가를 근거로 근로자와의 근
- `id_21793` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity'], conf:high→medium
  - notes: 갱신기대권이 인정되지 않는다고 판정한 사례 — worker_status 판단이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
