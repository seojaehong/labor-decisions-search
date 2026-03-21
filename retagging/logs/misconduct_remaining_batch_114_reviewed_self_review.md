# misconduct_remaining_batch_114_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_114_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_48733` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고 징계양정은 적정하며 징계절차상 하자도 없으므로 해고는 정당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_48737` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 징계사유가 모두 인정되고 징계양정이 적정하며, 징계절차도 적법하여 해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_48745` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정이 적정하며, 징계절차를 준수하여 정당한 징계처분이라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여
- `id_48767` [misconduct]
  - 변경: notes
  - notes: 근로자와 사용자가 행정소송을 제기하지 않아 재심판정이 확정된 사건에서, 사용자가 재심판정에서 인정된 징계사유 그대로 징계양정만 정직 2개월에서 
- `id_48769` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 인정되고, 양정이 과하지 않으며, 절차에 하자가 없어 견책 및 정직의 징계가 모두 정당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
