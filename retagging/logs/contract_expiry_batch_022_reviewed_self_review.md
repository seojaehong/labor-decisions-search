# contract_expiry_batch_022_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_022_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_23365` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_23369` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 기간의 정함이 있는 근로계약의 계약기간이 만료되자 스스로 사직서를 작성하고 제출하여 해고가 존재하지 않는다고 판정한 사례 — discrimina
- `id_23375` [discrimination]
  - 변경: notes, secondary:['worker_status', 'dismissal_validity', 'renewal_expectation']→['worker_status', 'renewal_expectation', 'dismissal_validity']
  - notes: 국공립연구기관에서 6년간 단절 없이 근로한 기간제 연구원에게 불합리한 근무성적 평가 결과에 따라 근로계약 갱신을 거절한 것은 부당해고라고 판정한
- `id_23389` [dismissal_validity]
  - 변경: notes
  - notes: 대기발령에 대한 구제신청 과정에서, 근로계약이 종료되었다면 구제이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_23411` [dismissal_validity]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 근로계약기간이 만료되어 근로관계가 종료되었다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
