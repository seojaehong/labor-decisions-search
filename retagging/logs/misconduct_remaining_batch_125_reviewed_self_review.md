# misconduct_remaining_batch_125_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_125_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_5315` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고 비위행위에 비추어 징계양정이 과하다고 볼 수 없으며 징계절차에 하자가 없으므로 징계해고는 정당하다고 판정한 사례 — 징계·해
- `id_53151` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자1, 2의 징계사유가 모두 존재하지 않아 해고는 부당하고, 근로자3의 징계사유 일부가 인정되고 징계절차가 적법하나 양정이 과하여 해고는 부
- `id_53163` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정이 과하다고 볼 수 없으며, 징계절차에도 하자가 없어 해고는 정당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가
- `id_5317` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 근로자의 명함에 대표라고 되어 있으나 실제 사용자의 지휘·감독하에 근로를 제공한 근로기준법상 근로자에 해당하고, 징계사유 중 일부가 인정되나 그
- `id_53191` [disciplinary_severity]
  - 변경: notes
  - notes: 사용자의 징계절차는 적법하나 근로자의 비위행위 중 일부만 징계사유로 인정되고 그 비위행위의 정도에 비해 징계양정이 과도하여 부당한 징계라고 판정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
