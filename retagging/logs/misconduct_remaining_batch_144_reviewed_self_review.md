# misconduct_remaining_batch_144_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_144_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_61053` [misconduct]
  - 변경: notes
  - notes: 노선버스 운행 중 흡연 및 무단결근 등의 징계사유가 인정되고 징계양정이 과도하다고 볼 수 없으며 징계절차도 적법하므로 정직 2월의 징계가 정당하
- `id_61063` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 양정이 적정하며 절차도 적법하여 정당한 징계처분이라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을
- `id_61083` [disciplinary_severity]
  - 변경: notes
  - notes: 취업규정상 징계사유가 인정되고 그 비위의 정도를 고려할 때 징계양정이 적정하며 징계절차상 하자가 없으므로 해고가 정당하다고 판정한 사례 — 비위
- `id_61091` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 징계절차상 하자는 없으나 인정되는 사유에 비해 정직 3월의 징계는 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제
- `id_61093` [procedure]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 적정하며, 징계절차상 하자가 없어 정직 처분이 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
