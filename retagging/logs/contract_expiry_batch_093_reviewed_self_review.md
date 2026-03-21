# contract_expiry_batch_093_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_093_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_46683` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['attendance', 'misconduct', 'procedure', 'dismissal_validity'], conf:high→medium
  - notes: 근로자에게 촉탁직으로 재고용 될 것이라는 정당한 기대권이 인정되나, 사용자가 근로자의 촉탁직 재고용을 거절할 만한 합리적인 이유가 있다고 판정한
- `id_46691` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'unfair_treatment', 'dismissal_validity']→['attendance', 'procedure', 'unfair_treatment', 'dismissal_validity'], conf:high→medium
  - notes: 근로자에게 촉탁직으로 재고용 될 것이라는 정당한 기대권이 인정되나, 사용자가 근로자의 촉탁직 재고용을 거절할 만한 합리적인 이유가 있고, 사용자
- `id_46711` [dismissal_validity]
  - 변경: notes
  - notes: 근로자는 기간제법에서 정한 ‘사용기간 제한의 예외’에 해당하는 기간제근로자로서 2년을 초과하여 근로하였다 하더라도 기간의 정함이 없는 근로계약을
- `id_46727` [renewal_expectation]
  - 변경: notes, secondary:['unfair_treatment', 'dismissal_validity']→['absence_without_leave', 'misconduct', 'disciplinary_severity', 'unfair_treatment']
  - notes: 근로자1의 징계사유는 일부 인정되나, 해고에 이를 정도의 사유가 아님에도 해고한 것은 부당하며, 근로자2에 대한 갱신거절은 합리적인 이유가 없어
- `id_46729` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 고용승계 기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
