# misconduct_remaining_batch_130_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_130_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_55255` [disciplinary_severity]
  - 변경: notes, secondary:['attendance', 'absence_without_leave', 'misconduct', 'procedure', 'training_opportunity']→['attendance', 'absence_without_leave', 'misconduct', 'procedure']
  - notes: 근로자의 징계사유가 인정되고 징계양정도 적정하며 징계절차도 적법하여 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 
- `id_55265` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정도 적정하며, 징계절차 또한 하자가 없어 근로자에 대한 징계가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결
- `id_5527` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 직무수행 능력 부족 및 책임감 결여, 지속적 민원유발, 상급자 사진촬영으로 인한 질서문란은 징계사유로 인정되지만, 징계사유가 그 비위의 정도가 
- `id_55277` [misconduct]
  - 변경: notes
  - notes: 직위해제의 구제이익은 존재하나 직위해제의 사유가 정당하며, 근로자에 대한 5개의 징계사유 중 4개만 인정되나, 2가지 징계사유만으로도 징계양정은
- `id_55289` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정이 징계권자에게 맡겨진 징계재량권을 남용하였다고 볼 수 없으며, 징계처분이 절차상 부당하다고 볼 수 없으므로 2건의

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
