# misconduct_remaining_batch_043_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_043_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_343931` [misconduct]
  - 변경: notes
  - notes: 근로자의 업무상 과실은 인정되나 이는 단순한 과오에 의한 경미한 사고로서 견책처분의 정당한 징계사유에 해당된다고 보기 어려우므로 징계가 부당하다
- `id_343941` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 적정하며 징계절차에 하자가 없어 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가
- `id_343957` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 존재하고 징계양정이 과다하다고 볼 수 없으나, 징계 재심절차에 중대한 하자가 존재하므로 부당하다고 판정한 사례 — 비위
- `id_343987` [unfair_treatment]
  - 변경: notes, conf:medium→high
  - notes: 징계사유 중 일부가 정당한 사유로 인정되나 인정되는 징계사유에 비하여 징계양정이 과하고, 징계절차도 준수하지 않았으므로 부당해고에 해당하며, 해
- `id_34401` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 공공기록물을 임의로 삭제한 근로자1에 대한 정직은 사유, 양정, 절차 모두 정당하고, 업무추진비 등을 부적정하게 사용한 근로자2에 대한 해고는 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
