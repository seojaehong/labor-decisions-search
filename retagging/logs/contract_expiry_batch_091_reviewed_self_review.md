# contract_expiry_batch_091_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_091_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_4581` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간이 만료되지 않았음에도 근로계약기간 만료를 이유로 당사자 간의 근로관계를 일방적으로 종료하여 부당해고라고 판정한 사례 — 해고 사실 
- `id_45821` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되나 갱신거절의 합리적 이유가 있고, 갱신거절이 불이익취급의 부당노동행위가 아니라고 판정한 사례 — 갱신기대권 성립 여부 및 갱
- `id_45839` [discrimination]
  - 변경: notes, conf:high→medium
  - notes: 근로자는 공무직 전환기대권이 있음에도 객관성？공정성이 결여된 평가를 근거로 근로관계를 종료한 것은 합리적 이유가 없어 부당하다고 판정한 사례 —
- `id_4585` [dismissal_validity]
  - 변경: notes
  - notes: 부당해고 구제신청 전에 근로계약기간이 만료되어 근로관계가 종료되었으므로 구제신청의 이익이 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존
- `id_45851` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['disciplinary_severity', 'dismissal_validity'], conf:high→medium
  - notes: 정규직 전환 기대권은 인정되나, 정규직 전환 평가를 통해 정규직 전환을 거절한 것은 정당한 이유가 존재한다고 판정한 사례 — 갱신기대권 성립 여

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
