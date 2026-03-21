# misconduct_remaining_batch_137_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_137_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_58273` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 적정하며 징계절차가 적법하여 부당해고에 해당하지 않는다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을
- `id_58275` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차에도 하자가 없어 해고는 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_58301` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 사용자가 교부한 해고예고통지서에 해고사유를 구체적으로 작성하지 않아 절차상 위반으로 부당해고라고 판정한 사례 — 징계·해고 절차 하자가 결론을 
- `id_58309` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유 중 일부가 징계사유로 인정되고 징계절차도 적법하나 징계양정이 과다하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_5831` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 수습 기간 중인 근로자가 상급자를 폭행하고 살해 협박하여 징계해고한 것은 징계사유가 인정되어 사용자의 재량권을 남용한 위법한 처분으로 보기 어렵

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
