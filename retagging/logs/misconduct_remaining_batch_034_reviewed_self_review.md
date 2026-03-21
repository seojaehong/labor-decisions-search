# misconduct_remaining_batch_034_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_034_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_2903` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 법인통장 관리 소홀 등 징계사유가 존재하고, 양정 및 절차에 하자가 없으므로 감봉처분의 정당성이 인정된다고 판정한 사례 — 비위 인정이나 해고·
- `id_29129` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되나, 인정되는 징계사유에 비해 해고의 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_29147` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure']
  - notes: 직무와 관련하여 향응을 수수한 것은 정당한 징계사유에 해당되고 징계절차도 적법하나, 해임처분은 징계양정이 과하여 부당하다고 판정 — 징계양정(제
- `id_29149` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure']
  - notes: 징계사유가 인정되고, 징계절차에도 하자가 없으나, 양정이 과하여 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정
- `id_29155` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 존재하고, 그 비위의 정도와 비교하면 해고는 징계양정이 과하지 않다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
