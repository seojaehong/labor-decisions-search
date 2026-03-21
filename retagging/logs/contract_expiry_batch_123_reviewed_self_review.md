# contract_expiry_batch_123_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_123_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_7981` [renewal_expectation]
  - 변경: notes
  - notes: 근로관계는 기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_7985` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 기간제(계약직) 근로계약으로, 계약기간 만료에 따라 근로관계가 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또
- `id_8005` [discrimination]
  - 변경: notes, secondary:['worker_status', 'dismissal_validity', 'renewal_expectation']→['worker_status', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자들은 기간제근로자로서 근로계약의 갱신기대권이 인정되고 갱신 거절의 합리적 이유가 없어 근로관계 종료가 부당하다고 판정한 사례 — discr
- `id_8015` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 해고의 사실을 인정할만한 객관적이고 구체적인 입증자료가 없어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이
- `id_8023` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로계약 갱신기대권이 인정되고, 갱신 거절의 합리적 이유가 없어 근로관계 종료가 부당하다고 판정한 사례 — discrimination 판단이 핵

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
