# sexual_harassment_batch_007_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_007_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_34983` [misconduct]
  - 변경: notes
  - notes: 근로자가 직무를 이탈하고, 부하직원을 성희롱한 행위 등은 인사규정을 위반한 행위로 정직은 정당하고, 정직 후의 직위조정은 정직에 수반되는 인사명
- `id_349873` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 적정하며 징계절차가 적법하므로 정직 6개월의 징계는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과
- `id_350159` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되나, 인정되는 징계사유만으로는 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_350211` [disciplinary_severity]
  - 변경: notes
  - notes: 프리랜서 직원에 대한 성희롱 방조행위에 대한 견책의 징계가 적법하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_350287` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 징계사유 중 일부만 인정되고, 그 징계사유에 대한 양정이 적정하며, 징계절차에 하자가 일부 존재하나 소명기회를 충분히 부여받았으므로 절차상 하자

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
