# misconduct_remaining_batch_052_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_052_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_349437` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 해고가 존재하며, 해고사유와 해고시기를 명시한 서면통보를 하지 않아 해고는 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_349441` [procedure]
  - 변경: notes
  - notes: 일부 징계사유는 인정되고 징계절차의 적법성은 인정되나 양정이 과하여 해고는 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_349445` [misconduct]
  - 변경: notes
  - notes: 근로기준법상 근로자성이 인정되고 징계사유가 모두 존재하지 않아 해고는 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 
- `id_349451` [misconduct]
  - 변경: notes
  - notes: 근로자가 근로기준법상 근로자에 해당하지 않으므로 구제신청의 당사자 적격이 없다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 
- `id_349469` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 양정이 적정하며, 절차상 하자도 없어 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
