# misconduct_remaining_batch_007_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_007_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_13151` [disciplinary_severity]
  - 변경: notes
  - notes: 겸직금지 및 품위유지의무를 위반한 징계사유가 인정되고, 그에 따른 징계양정도 과하다고 볼 수 없어 해임처분이 정당하다고 판정한 사례 — 비위 인
- `id_13167` [disciplinary_severity]
  - 변경: notes
  - notes: 징계에 정당한 사유가 있고, 징계사유 통보가 미흡한 절차상의 하자는 진행과정에서 치유되었으며, 양정에 있어 사용자의 재량권이 남용되었다고 볼 수
- `id_13187` [misconduct]
  - 변경: notes
  - notes: 교통사고를 유발한 행위는 징계사유에 해당하고, 단체협약에 규정된 대물 피해액수에 따라 사용자가 행한 정직(휴직) 2월의 징계처분은 적정하다고 판
- `id_1319` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 양정이 적정하며 절차도 적법하므로 징계해고는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정
- `id_13197` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유에 해당하나, 해고처분을 하는 것은 그 양정이 과하고 형평성에도 어긋나므로 부당해고라고 판정한 사례 — 징계·해고 절차 하자가 결론을 직

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
