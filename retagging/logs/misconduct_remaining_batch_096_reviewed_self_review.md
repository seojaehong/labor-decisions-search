# misconduct_remaining_batch_096_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_096_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_413901` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고 양정도 적정하며 절차에도 하자가 없어 정당한 징계라고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_41393` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 비위 정도와 징계양정기준에 비추어 볼 때 양정이 과하지 않으며, 징계절차상 하자가 없으므로 정당하다고 판정한 사례 — 비위
- `id_413967` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정이 과하다고 볼 수 없으며, 징계절차에 하자가 없어 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을
- `id_413993` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되나, 인정되는 징계사유에 비해 징계양정이 과도하여 정직 3월의 징계가 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가
- `id_413997` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 중 일부가 인정되나, 인정되는 징계사유에 비해 징계양정이 과도하여 정직 3월의 징계가 부당하다고 판정한 사례 — 징계양정(제재 수위)의

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
