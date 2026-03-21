# misconduct_remaining_batch_104_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_104_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_44627` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고 징계양정이 적정하며 징계절차에 하자가 없어 정직 3월의 징계는 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_44631` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고, 징계절차가 적법하나, 그 비위행위의 정도에 비하여 양정이 과도하여 징계면직은 부당하다고 판정한 사례 — 징계양정(제재
- `id_44649` [unfair_treatment]
  - 변경: notes
  - notes: 2건의 교통사고로 인한 물적피해는 징계사유로 인정되고, 운전기사로서의 자질, 근무성적, 징계 형평 등을 감안할 때 징계양정이 과하다고 볼 수 없
- `id_44651` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계절차도 하자가 없으며 징계양정도 과하지 않다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌
- `id_44663` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 일부 인정되고, 인정되는 징계사유에 비해 징계양정이 과하지 않으며, 징계절차가 적법하므로 정직 6개월은 정당하다고 판정한 사

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
