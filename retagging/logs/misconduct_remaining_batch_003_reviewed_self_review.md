# misconduct_remaining_batch_003_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_003_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_1117` [misconduct]
  - 변경: notes
  - notes: 징계사유 일부가 인정되나, 비위행위에 비해 과도하게 중한 징계처분을 행한 것은 부당하다고 인정한 사례 — 비위행위 존재 및 중대성이 해고 정당성
- `id_11175` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 사용자2에게 당사자 적격이 있고 구제신청의 제척기간은 도과하지 않았으며 해고는 사유, 양정, 절차에 있어서 모두 정당하다고 판정한 사례 — 징계
- `id_11179` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 법인의 감사라 하더라도 사용자로부터 업무수행 과정에서 상당한 지휘·감독을 받으면 근로기준법상 근로자에 해당하고, 징계사유 중 일부만 인정되고 절
- `id_11185` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 피해아동의 사망이라는 결과를 방지하지 못한 징계사유는 인정되지만, 근로자의 비위행위에 비하여 징계양정이 과도하여 정직 처분이 부당하다고
- `id_11193` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 정직처분은 징계사유가 인정되고 징계양정이 적정하며 징계절차상 하자도 없으므로 정당하고, 해고는 정당한 해고사유가 존재하지 않아 부당하다고 판정한

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
