# misconduct_remaining_batch_139_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_139_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_59209` [unfair_treatment]
  - 변경: notes
  - notes: 절차상 하자는 없으나, 인정되는 징계사유에 비해 양정이 과다하여 부당해고이고, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불
- `id_5921` [misconduct]
  - 변경: notes
  - notes: 사용자가 징계사유로 삼은 근로자의 비위행위가 확인되지 않으므로, 징계사유가 인정되지 않아 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 
- `id_59217` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 2023. 8. 11. 자로 행한 해고의 정당성 여부가 확정되지 않았으므로 구제이익이 존재하고, 징계사유가 인정되며, 징계절차가 적법하나, 인정
- `id_59219` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 절차상 하자는 없으나 양정이 과다하여 부당정직이라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 
- `id_59225` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차에도 하자가 없어 해임 처분은 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
