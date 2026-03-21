# contract_expiry_batch_114_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_114_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_57667` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['misconduct', 'procedure', 'renewal_expectation'], conf:high→medium
  - notes: 사용자에게 당사자 적격이 인정되나, 사용자가 근로자에 대해 확정적·종국적으로 해고의 의사표시를 하였다고 볼 만한 사정이 존재하지 않아 해고가 존
- `id_57677` [worker_status]
  - 변경: notes, secondary:['unfair_treatment', 'dismissal_validity', 'renewal_expectation']→['unfair_treatment', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자들에게 근로계약의 갱신기대권이 인정되지 않고, 근로관계 종료가 부당노동행위에 해당하지 않는다고 판정한 사례 — worker_status 판
- `id_57679` [worker_status]
  - 변경: notes, secondary:['dismissal_validity']→['renewal_expectation', 'dismissal_validity']
  - notes: 근로자가 스스로 퇴사하여 해고가 존재하지 않는다고 판정한 사례 — worker_status 판단이 핵심
- `id_57681` [renewal_expectation]
  - 변경: notes
  - notes: 사용자의 일방적인 의사에 의해 근로관계가 종료되었다고 보기어려워 해고가 존재하지 않으며, 근로자에게 근로계약의 갱신기대권은 인정되지 않는다고 판
- `id_57705` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['dismissal_validity', 'workplace_harassment']
  - notes: 근로자에게 근로계약이 갱신기대권이 인정되고, 사용자의 근로계약 갱신거절에 합리적인 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
