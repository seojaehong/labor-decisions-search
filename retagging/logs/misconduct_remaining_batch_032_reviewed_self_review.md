# misconduct_remaining_batch_032_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_032_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_27659` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 지각 등의 일부 징계사유가 인정되나, 그 사유에 비해 정직은 양정이 과하여 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 
- `id_27669` [disciplinary_severity]
  - 변경: notes
  - notes: 출퇴근 전산 기록부의 상당 기간 미등록, 근무시간 중 휴게실 사용 등 일부 징계사유가 인정되나, 정직은 그 양정이 과도하다고 판정한 사례 — 비
- `id_27677` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 일부 징계사유는 인정되지만, 해고는 다른 근로자들의 징계양정에 비해 과하고 징계절차상 하자가 있어 부당하다고 판정한 사례 — 징계·해고 절차 하
- `id_27691` [disciplinary_severity]
  - 변경: notes
  - notes: 법인카드를 개인적 용도로 사용하고 직무관련자로부터 향응을 제공받은 행위는 징계사유에 해당하고, 파면처분은 비위 정도와 징계양정기준에 비추어 볼 
- `id_27709` [misconduct]
  - 변경: notes, secondary:['attendance']→['attendance', 'disciplinary_severity']
  - notes: 근로자의 귀책사유가 일부 인정된다고 하더라도 근로자를 해고까지 한 것은 양정이 과하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
