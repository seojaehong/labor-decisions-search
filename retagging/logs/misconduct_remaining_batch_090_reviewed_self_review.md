# misconduct_remaining_batch_090_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_090_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_41105` [misconduct]
  - 변경: notes
  - notes: 근로자의 비위행위에 대해 퇴직 후 4년이 지난 시점에 징계한 것은 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_411051` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유1, 2, 4와 징계사유3 일부의 징계사유가 인정되고, 양정이 과도하지 않으며, 절차상 하자도 없어 정직 1개월의 징계가 정당하다고 판정
- `id_41109` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되나, 해고는 양정이 과중하여 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우
- `id_411091` [misconduct]
  - 변경: notes
  - notes: 공시업무를 원활하게 이행하지 않아 차질을 발생시키는 등 징계사유가 모두 인정되고 징계사유에 비해 그 양정이 과하다고 보기 어려우며 징계절차도 적
- `id_411101` [disciplinary_severity]
  - 변경: notes
  - notes: 구제신청 근로자 5명 중 일부(2명)는 징계사유가 인정되고 양정이 적정하고 절차 하자도 없어 정당하나, 일부(3명)는 징계사유가 인정되고 절차 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
