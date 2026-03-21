# misconduct_remaining_batch_132_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_132_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_56149` [workplace_harassment]
  - 변경: notes
  - notes: 근로자의 비위행위는 모두 징계사유로 인정되나, 그 비위행위에 비하여 징계양정이 과하여 징계해고는 부당하다고 판정한 사례 — 직장 내 괴롭힘 성립
- `id_56151` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 양정이 적정하며, 절차에 하자가 없어 근로자에 대한 정직 3월의 징계가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계
- `id_56161` [misconduct]
  - 변경: notes
  - notes: 근로자는 사용자와 위촉계약을 체결하고 채권추심업무를 함에 있어 사용종속관계에서 근로를 제공하였다고 보기 어려우므로 근로기준법상 근로자에 해당하지
- `id_56169` [disciplinary_severity]
  - 변경: notes
  - notes: 징계해고 사유가 존재하고 양정이 적정하며 절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을
- `id_5617` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되며 정직 4개월의 징계는 양정이 적정하고 절차에 하자도 없어 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
