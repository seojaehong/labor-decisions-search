# misconduct_remaining_batch_063_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_063_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_3819` [disciplinary_severity]
  - 변경: notes
  - notes: 근무지 이탈 및 복무위반의 징계사유는 인정되나, 징계사유에 비하여 해임은 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_38195` [misconduct]
  - 변경: notes
  - notes: 해고 사유 및 절차가 정당하지 않아 부당한 해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_38201` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유는 모두 정당한 것으로 인정되고, 비위행위의 정도와 징계형평성 등을 고려할 때 징계양정은 적정하며, 징계절차상 하자는 치유
- `id_38209` [disciplinary_severity]
  - 변경: notes
  - notes: 대기발령을 행할 업무상 필요성이 부족하고 불이익한 대기발령(부서이동) 처분은 부당하나, 도박행위에 대한 징계사유가 인정되고 양정, 절차에도 하자
- `id_3821` [dismissal_validity]
  - 변경: notes
  - notes: 징계사유 중 일부만 인정되고, 인정되는 비위행위의 정도에 비해 양정이 과도하여 해고는 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
