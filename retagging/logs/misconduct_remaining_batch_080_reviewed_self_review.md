# misconduct_remaining_batch_080_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_080_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_406309` [disciplinary_severity]
  - 변경: notes
  - notes: 이 사건 징계는 '휴대전화 사용’이라는 동일한 사유로 세 번째 징계를 받은 것으로 징계사유가 존재하고, 취업규칙에 가중처벌 규정이 있는 등 징계
- `id_406313` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 존재하고, 징계양정이 적정하며, 징계절차에 하자가 없다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판
- `id_406329` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure']
  - notes: 징계사유가 존재하고 양정 및 절차도 적정하여 감봉 3개월 처분이 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정
- `id_40635` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고 징계양정이 과하지 않으며 절차상 하자가 없다고 판정 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_406363` [misconduct]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고, 비위의 정도 등을 볼 때 양정이 과다하지 않으며, 절차상 하자도 없으므로 해고의 징계가 정당하다고 판정한 사례 — 비

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
