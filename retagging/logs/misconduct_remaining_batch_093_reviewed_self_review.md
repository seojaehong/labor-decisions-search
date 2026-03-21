# misconduct_remaining_batch_093_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_093_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_412585` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 적정하며, 징계절차에 하자가 없어 근로자에 대한 징계해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 
- `id_41259` [misconduct]
  - 변경: notes
  - notes: 징계위원으로서 행한 징계 심의 및 의결 행위가 징계사유에 해당하지 않는다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_412609` [misconduct]
  - 변경: notes
  - notes: 감봉은 징계사유가 존재하고 징계양정이 적정하며 절차상 위법이 있다고 보이지 않으므로 정당하고, 조장 직위해제는 업무상 필요성이 존재하고 생활상 
- `id_412613` [misconduct]
  - 변경: notes
  - notes: 근태불량, 허위 보고 및 자료 조작, 업무지시 위반 등 징계사유가 인정되고, 징계양정도 적정하므로 징계해고가 정당하다고 판정한 사례 — 비위행위
- `id_41263` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 재량권을 벗어난 과도한 징계로 보이지 않으며, 징계절차도 적법하여 부당해고가 아니라고 판정한 사례 — 비위행위 존재 및 중

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
