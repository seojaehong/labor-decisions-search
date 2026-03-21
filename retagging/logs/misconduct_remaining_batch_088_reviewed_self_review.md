# misconduct_remaining_batch_088_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_088_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_410081` [disciplinary_severity]
  - 변경: notes
  - notes: 인사규정에서 규정한 직위해제 사유에 해당하지 않아 업무상 필요성이 존재하지 않아 부당한 직위해제에 해당하고, 징계사유 중 일부가 인정되지 않고,
- `id_410097` [unfair_treatment]
  - 변경: notes
  - notes: 해고는 징계사유가 정당하고, 징계절차의 하자가 없으나 징계양정 과다로 부당하며, 징계 처분 등은 부동노동행위에 해당하지 않는다고 판정한 사례 —
- `id_4101` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 징계양정이 적정하며, 징계절차에도 하자가 없어 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_410113` [procedure]
  - 변경: notes, secondary:['misconduct', 'disciplinary_severity']→['misconduct', 'training_opportunity', 'disciplinary_severity'], conf:medium→high
  - notes: 전라남도목포교육지원청에서 조사한 근로자의 언행 및 행위의 비위행위는 정당한 징계사유에 해당하고, 징계양정이 적정하며, 징계절차가 적법하므로 정당
- `id_410123` [misconduct]
  - 변경: notes, conf:high→medium
  - notes: 경영 전반에 대한 자문 업무를 위임받아 수행하였으므로 근로기준법상 근로자에 해당하지 않는다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
