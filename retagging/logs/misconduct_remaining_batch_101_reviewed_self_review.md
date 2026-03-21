# misconduct_remaining_batch_101_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_101_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_43409` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 과하지 않고 절차가 적법하여 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판
- `id_43421` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 행위가 징계사유로 인정되고, 징계해고는 사용자의 재량권을 벗어난 과도한 징계로 보이지 않아 징계양정이 적정하며, 징계절차에 하자도 없으
- `id_43423` [disciplinary_severity]
  - 변경: notes
  - notes: 이 사건 사용자1은 피신청인적격이 없고, 이 사건 강등은 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없으므로 정당하다고 판정
- `id_43433` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 인정되나 징계양정이 과하여 감봉3개월 처분은 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_43437` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 인정되고 비위행위의 정도에 비하여 양정이 과하지 않으며 징계절차도 적법하므로 감급 5월의 징계처분은 정당하다고 판정한 사례 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
