# misconduct_remaining_batch_141_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_141_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_59901` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계의 사유, 양정, 절차가 모두 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_5993` [misconduct]
  - 변경: notes
  - notes: 징계사유는 일부 인정되나 근로자의 비위행위의 정도나 과실에 비해 사용자가 근로자에게 행한 정직 2개월의 징계처분은 그 양정이 과하여 부당하다고 
- `id_59951` [misconduct]
  - 변경: notes
  - notes: 부당해고 판정 이후 추가된 징계사유가 이전 징계사유와 본질적으로 다르다고 볼 수 없어 징계가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성
- `id_59957` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 존재하고, 징계양정이 적정하며, 징계절차상 중대한 하자가 없어 정직 처분이 정당하다고 판정한 사례 — 비위 인정이나 해고·징
- `id_59983` [procedure]
  - 변경: notes, secondary:['absence_without_leave', 'misconduct', 'disciplinary_severity', 'unfair_treatment']→['attendance', 'absence_without_leave', 'misconduct', 'disciplinary_severity'], conf:medium→high
  - notes: ‘무단결근’의 비위행위를 사유로 행한 해고는 그 사유가 정당하며, 여객운수업을 경영하는 회사의 공공성 및 특수성, 근로자의 지속적인 지각 및 무

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
