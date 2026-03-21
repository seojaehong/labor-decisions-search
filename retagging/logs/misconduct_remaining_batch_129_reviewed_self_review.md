# misconduct_remaining_batch_129_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_129_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_54823` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 일부 존재하고, 양정이 적정하며, 절차에도 하자가 없어 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_5483` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 일부가 인정되고, 징계양정도 적정하며, 징계절차에도 하자가 없어 해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심
- `id_54855` [procedure]
  - 변경: notes, secondary:['misconduct', 'disciplinary_severity']→['misconduct', 'disciplinary_severity', 'workplace_harassment'], conf:medium→high
  - notes: 징계사유가 존재하고 징계양정이 과하다고 보기 어려우며 징계절차도 적법하여 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_54857` [unfair_treatment]
  - 변경: notes
  - notes: 징계처분이 절차상 중대한 하자가 있어 부당하나, 징계사유가 일부 인정되고 인정되는 징계사유에 비해 양정이 과하지 않으므로, 부당노동행위에 해당하
- `id_54859` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 중 일부가 인정되고 징계절차상 하자는 없으나 인정되는 비위행위에 비해 양정이 과도하므로 부당하다고 판정한 사례 — 징계양정(제재 수위)

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
