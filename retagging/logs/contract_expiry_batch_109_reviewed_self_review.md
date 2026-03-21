# contract_expiry_batch_109_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_109_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_55163` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 무기계약직 전환기대권이 인정되지 않아 근로관계는 계약기간 만료로 정당하게 종료되었고, 불이익 취급 및 지배·개입의 부당노동행위에도 해
- `id_55167` [dismissal_validity]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 기간제근로자의 계약기간 만료로 근로계약이 종료되었고, 이에 앞서 종전의 근로계약서 재계약 관련 조항에 따라 계약이 이미 갱신되었다는 근로자의 주
- `id_55175` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들에게 근로계약의 갱신기대권이 인정되고, 갱신거절의 합리적인 이유가 존재하지 않으며, 근로계약 만료 통보는 불이익 취급의 부당노동행위에 해
- `id_55179` [renewal_expectation]
  - 변경: notes
  - notes: 사용자1에게 당사자적격이 인정되며 정규직 전환 기대권이 인정되나 전환 거절에 합리적 이유가 있어 근로관계를 종료한 것은 정당하다고 판정한 사례 
- `id_55181` [renewal_expectation]
  - 변경: notes, secondary:['worker_status', 'dismissal_validity']→['misconduct', 'worker_status', 'dismissal_validity']
  - notes: 근로자는 기간제 근로자에 해당하고, 근로자의 근로계약 갱신기대권이 인정되나, 사용자의 근로계약 갱신거절에 합리적 이유가 존재하므로 사용자가 계약

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
