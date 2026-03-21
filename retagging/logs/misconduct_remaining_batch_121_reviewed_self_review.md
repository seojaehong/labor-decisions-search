# misconduct_remaining_batch_121_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_121_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_51481` [workplace_harassment]
  - 변경: notes
  - notes: 근로자의 비위행위가 징계사유로 인정되고 징계절차도 적법하나 징계양정이 과다하여 부당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_51483` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 인정되고 비위행위의 정도를 고려할 때 감봉의 징계는 징계양정이 적정하며 징계절차상 하자가 없으므로 정당하다고 판정한 사례 — 직장 내
- `id_51497` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자의 징계사유는 인정되나, 징계양정이 과하여 해고가 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_51505` [disciplinary_severity]
  - 변경: notes
  - notes: 성실의무 위반, 복종의무 위반의 징계사유가 인정되고, 징계양정이 적정하며, 징계절차에 하자가 없어 징계가 정당하다고 판정한 사례 — 비위 인정이
- `id_5151` [procedure]
  - 변경: notes
  - notes: 사용자가 징계사유 대부분을 입증하지 못하고, 근로자 비행의 정도에 비하여 징계양정이 과도하고, 취업규칙에서 정한 징계절차를 준수하지 않아 해고가

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
