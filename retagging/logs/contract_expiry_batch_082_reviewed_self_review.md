# contract_expiry_batch_082_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_082_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_412885` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자에 해당하고 근로계약이 갱신된다는 신뢰관계가 형성되어 있다고 보기 어려워 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성
- `id_41289` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자에게 근로계약 갱신에 대한 기대권이 존재한다고 볼만한 규정이나 관행이 없어 사용자가 근로계약기간 만료로 근로관계를 종료한 것은 정당하
- `id_412907` [renewal_expectation]
  - 변경: notes
  - notes: 이 사건 근로자는 기간의 정함이 있는 근로자이나 무기계약 전환기대권이 인정되며, 이 사건 근로자에 대한 무기계약 전환 거부에 합리적 이유가 존재
- `id_412911` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 계약기간 만료에 따라 근로관계가 종료된 것이므로 해고가 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵
- `id_412941` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['training_opportunity', 'disciplinary_severity', 'dismissal_validity']
  - notes: 근로계약기간 만료에 대한 사전 통지는 해고라고 볼 수 없고, 갱신기대권이 인정되나 근무평가 등 종합점수가 기준에 미달하여 갱신거절한 것은 합리적

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
