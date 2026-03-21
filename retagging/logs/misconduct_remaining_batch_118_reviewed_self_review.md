# misconduct_remaining_batch_118_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_118_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_50397` [unfair_treatment]
  - 변경: notes, secondary:['attendance', 'absence_without_leave', 'misconduct', 'procedure', 'disciplinary_severity']→['attendance', 'absence_without_leave', 'misconduct', 'procedure'], conf:high→medium
  - notes: 징계사유가 인정되고 징계절차상에 하자는 없는 것으로 확인되나, 인정되는 징계사유만으로 양정이 과도하여 부당징계라고 판단되며, 부당노동행위로는 볼
- `id_50407` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 일부 인정되나, 징계양정이 과하여 부당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_50413` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계해고가 사유, 양정, 절차에 있어 모두 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_50421` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유에 비해 해고의 양정이 과하여 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_50435` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되며 징계양정기준과 비교할 때 징계양정이 적정하고 징계절차상 하자가 없으므로 징계면직 처분은 정당하다고 판정한 사례 — 징계

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
