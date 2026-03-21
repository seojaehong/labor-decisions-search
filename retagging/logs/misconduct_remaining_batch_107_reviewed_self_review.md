# misconduct_remaining_batch_107_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_107_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_45923` [misconduct]
  - 변경: notes
  - notes: 근로자에 대한 1차 및 2차 출근정지의 징계사유가 모두 인정되지 않고 징계절차에 하자가 있어 출근정지는 부당하다고 판정한 사례 — 비위사실이 명
- `id_45935` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 정직 2개월의 징계양정이 과하다고 볼 수 없으며, 징계절차에 하자가 없어 정직은 정당하다고 판정한 사례 — 비위 인정이나 
- `id_45957` [misconduct]
  - 변경: notes
  - notes: 근로자의 징계사유가 제반 증거 등을 통해 모두 인정되고, 징계사유에 대한 해고의 징계양정은 과도하지 않으며, 징계절차도 적법하다고 판정한 사례 
- `id_45961` [misconduct]
  - 변경: notes
  - notes: 징계의 정당성이 모두 인정되어 해고는 정당하다고 판정한 사례 — 비위사실이 명확히 인정되어 해고 정당성 직접 좌우
- `id_45975` [misconduct]
  - 변경: notes
  - notes: 근로자에게 징계사유가 인정되나 징계양정이 과도하여 부당한 정직이라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
