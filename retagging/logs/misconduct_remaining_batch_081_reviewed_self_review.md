# misconduct_remaining_batch_081_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_081_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_406813` [misconduct]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 징계절차도 적법하나, 해고의 징계는 인정되는 징계사유에 비해 양정이 과도하여 부당하다고 판정한 사례 — 비위행위 존재 
- `id_406819` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 징계사유가 존재하고 징계절차에 하자는 없으나, 징계양정이 과하여 징계해고는 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 
- `id_40685` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 일부 인정되나 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_406855` [disciplinary_severity]
  - 변경: notes
  - notes: 인정: 징계사유가 인정되나, 징계양정이 과도 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우
- `id_406885` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 대부분의 징계사유가 인정되고, 양정이 적정하며, 이중징계에 해당하지 않으므로 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
