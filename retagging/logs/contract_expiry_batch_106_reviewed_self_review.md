# contract_expiry_batch_106_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_106_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_53621` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 근로계약 체결에 대한 정당한 갱신기대권이 인정되고 갱신거절의 합리적 사유가 없어 근로계약 만료는 부당해고에 해당한다고 판정한 사례 — discr
- `id_53623` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 만료로 근로관계가 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_53625` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 계약갱신 기대권이 존재하나 사용자의 근로계약 갱신 거절에 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리
- `id_53627` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 새로운 수탁업체로 고용이 승계되리라는 기대권이 인정되고, 사용자가 이를 거부할 합리적인 이유가 없으므로 고용승계 거부는 부당해고와 마
- `id_53631` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'training_opportunity', 'dismissal_validity']
  - notes: 갱신기대권이 인정되지 않아 근로계약기간 만료로 근로계약관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
