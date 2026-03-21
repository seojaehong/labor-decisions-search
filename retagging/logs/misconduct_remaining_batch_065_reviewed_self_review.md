# misconduct_remaining_batch_065_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_065_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_3919` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure']
  - notes: 부당 이자 감면 및 재대출 취급 부적합 등 징계사유가 인정되고, 양정이 적정하며 절차상 하자가 없어 해고는 정당하고, 변상처분은 근로기준법상 `
- `id_39193` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 교육 미 이수, 정당한 업무 지시 불이행하여 징계사유가 인정되고, 양정 및 절차도 적정하다고 판정한 사례 — 비위 인정이나 해고·징계 
- `id_39197` [disciplinary_severity]
  - 변경: notes
  - notes: 단협규정을 어기고 행한 사내 시위행위는 징계사유가 될 수 있고, 부당노동행위에도 해당되지 않는다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_39207` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 징계사유 중 일부만 인정되고, 징계의 근본이유가 사용자 관련 비리제보인 점 등을 감안할 때 해임은 양정이 과하여 부당하다고 판정한 사례 — 징계
- `id_3921` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 중 일부가 인정되지 않고, 인정되는 징계사유에 비해 양정이 과도하며, 절차상 중대한 하자가 있어 해고가 부당하다고 판정한 사례 — 징계

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
