# contract_expiry_batch_066_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_066_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_402307` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자의 근로계약 갱신기대권이 인정되나, 2024년 근무성적 평가 시 원장 단독으로 평가한 것으로 보이는 점, 근무성적평가서의 업무실적이 202
- `id_402313` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 기간의 정함이 있는 근로계약을 체결하였고, 근로계약서나 회사의 취업규칙 등에 근로계약이 갱신된다는 취지의 내용 또는 재계약을 위한 요건
- `id_402315` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 사용자가 리모델링 공사를 이유로 근로자에게 사직을 권고한 사실이 있으나, 이후 공사계획 변경에 따라 근로자에게 근로계약기간 만료일까지 근로할 것
- `id_402325` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자에 해당하고 근로계약이 갱신된다는 신뢰관계가 형성되어 있다고 보기 어려워 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성
- `id_402335` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 고용승계 기대권이 인정되지 않아 근로계약기간 만료에 따라 근로관계가 종료되었는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
