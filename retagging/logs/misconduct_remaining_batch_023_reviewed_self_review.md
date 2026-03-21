# misconduct_remaining_batch_023_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_023_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_2219` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'training_opportunity']→['misconduct', 'procedure', 'training_opportunity']
  - notes: 징계사유가 인정되고, 징계사유에 비해 그 양정이 과하다고 볼 수 없으며, 징계절차상 하자도 없어 감봉처분은 정당하다고 판정한 사례 — 비위 인정
- `id_22193` [misconduct]
  - 변경: notes
  - notes: 징계절차에 중요한 하자가 있어 징계사유 인정 여부에 관계없이 징계해고가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접
- `id_22207` [misconduct]
  - 변경: notes
  - notes: 이력서 허위기재를 사유로 행한 정직처분은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_2221` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차의 하자가 없어 정당한 감봉처분이라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가
- `id_22221` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 업무지시 불이행 등 일부 징계사유는 인정되나, 소명기회 부여 등 징계절차 없이 행한 해고는 절차상 하자가 존재하여 부당하다고 판정한 사례 — 소

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
