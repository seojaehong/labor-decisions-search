# misconduct_remaining_batch_124_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_124_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_52815` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure']
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차상 하자가 없으므로 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여
- `id_52817` [misconduct]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고 징계 양정기준에 비추어 징계양정이 적정하며 징계절차상 하자가 없으므로 해고가 정당하다고 판정한 사례 — 비위사실이 명확
- `id_52819` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차상 하자가 없으므로 징계해고는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지
- `id_5283` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계해고가 사유, 양정, 절차에 있어 모두 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_52837` [disciplinary_severity]
  - 변경: notes
  - notes: 성실의무 및 복종의무 위반의 징계사유가 인정되고, 징계양정이 적정하며, 징계절차에 하자가 없어 징계(해임)가 정당하다고 판정한 사례 — 비위 인

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
