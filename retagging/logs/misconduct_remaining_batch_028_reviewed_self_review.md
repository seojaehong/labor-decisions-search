# misconduct_remaining_batch_028_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_028_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_25001` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유에 대해 다툼이 없고, 징계양정이 적정하며, 징계절차도 적법하므로 부당해고가 아니라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵
- `id_25013` [misconduct]
  - 변경: notes
  - notes: 사규위반 행위는 인정되나 징계절차를 위반하였고, 관여 정도와 형평성을 고려할 때 징계양정에 있어서도 부당하다고 판정한 사례 — 비위행위 존재 및
- `id_25027` [disciplinary_severity]
  - 변경: notes
  - notes: 이해상충금지 위반 등 대부분의 징계사유가 인정되고, 징계양정 및 징계절차에도 하자가 없어 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·
- `id_25037` [misconduct]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 인정되지 아니하므로 견책징계 처분은 정당한 인사권의 행사라고 볼 수 없어 부당징계라고 판정한 사례 — 비위행위 존재 및
- `id_2505` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 연구용역 수행과정에서 외부연구원을 허위로 등록하고 인건비를 편취한 것은 인사규정을 위반한 행위로 징계사유에 해당하고 비위행위에 비해 해

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
