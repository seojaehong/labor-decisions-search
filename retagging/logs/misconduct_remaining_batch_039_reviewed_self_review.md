# misconduct_remaining_batch_039_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_039_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_3233` [misconduct]
  - 변경: notes
  - notes: 근로자에게 품질경영체계 심사 시 부적절한 대응으로 회사의 신뢰도를 손상하고 업무적 지장을 준 과실이 존재하므로 징계사유는 인정되나, 근로자의 비
- `id_32361` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 인정되나 징계양정이 과도하여 정직 1월의 징계는 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_32367` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하며, 징계양정이 과도하다고 보기 어렵고, 징계절차에도 하자가 없어 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수
- `id_32379` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 존재하나 그 양정이 과하여 부당징계이고, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 
- `id_32381` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 존재하지 않아 부당징계에 해당하나, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
