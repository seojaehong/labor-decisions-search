# misconduct_remaining_batch_053_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_053_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_349975` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없는 정당한 징계해고라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지
- `id_349991` [disciplinary_severity]
  - 변경: notes
  - notes: 사내 의료비 지원금을 부정하게 수급하고 부정행위 방법 등을 동료들에게 적극적으로 공유？전파한 행위는 모두 징계사유로 인정되고 징계해고의 양정 및
- `id_349997` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 징계양정이 적정하며, 징계절차상 하자가 없다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_350017` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 모두 인정되고, 징계절차도 적법하나, 징계 양정이 과하여 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_350019` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 이해관계자와의 금전거래 등은 취업규칙의 징계사유에 해당하고 양정이 적정하며 절차적 하자가 없다고 판정한 사례 — 징계·해고 절차 하자가 결론을 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
