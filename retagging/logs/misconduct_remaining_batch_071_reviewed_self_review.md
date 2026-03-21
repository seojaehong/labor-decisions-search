# misconduct_remaining_batch_071_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_071_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_402005` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유와 근로자의 태도 등을 고려하면 해고는 정당하고 해고가 정당한 이상 대기발령의 구제이익은 존재하지 않는다고 판정한 사례 — 징계·해고 절
- `id_402021` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하나, 양정이 과하여 부당해고라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우
- `id_40203` [disciplinary_severity]
  - 변경: notes
  - notes: 징계 사유가 인정되나 징계 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_402049` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계해고는 인정되는 징계사유에 비하여 양정이 과하고, 징계절차도 적법하지 않으므로 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접
- `id_40205` [misconduct]
  - 변경: notes
  - notes: 징계사유는 인정되나, 그 사유에 비해 징계양정이 과하여 부당해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
