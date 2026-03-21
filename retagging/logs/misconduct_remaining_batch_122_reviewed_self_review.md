# misconduct_remaining_batch_122_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_122_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_51973` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계절차에 흠이 없으나 징계양정이 과하여 징계해고는 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부
- `id_51979` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 정당한 징계사유로 인정되고 징계양정이 적정하며 징계절차가 적법하므로 징계해고는 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정
- `id_51981` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 적정하며, 징계절차에도 하자가 없어 정직 5월의 처분이 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위
- `id_51987` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하지 않아 징계해고는 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_52005` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 적정하며, 징계절차가 적법하여 징계가 정당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
