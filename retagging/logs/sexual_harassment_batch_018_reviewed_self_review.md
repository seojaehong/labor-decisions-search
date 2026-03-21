# sexual_harassment_batch_018_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_018_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_56307` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 4건이 모두 인정되고, 해고의 징계양정이 적정하며, 징계절차도 적법하여 해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_56405` [misconduct]
  - 변경: notes, secondary:['procedure', 'disciplinary_severity']→['procedure', 'disciplinary_severity', 'workplace_harassment']
  - notes: 근로자의 징계사유가 전부 인정되고, 비위행위 정도에 비해 징계양정이 적정하며, 징계절차에 하자가 없으므로 해고가 정당하다고 판정한 사례 — 비위
- `id_5645` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 비위행위 중 일부만 정당한 징계사유에 해당하고 인정되는 징계사유에 비해 해고처분은 징계양정이 과도하여 부당해고라고 판정한 사례 — 징계
- `id_56637` [disciplinary_severity]
  - 변경: notes
  - notes: 징계해고는 일부 징계사유가 인정되고 징계양정이 사회통념상 현저하게 타당성을 잃어 징계권자에게 맡겨진 재량권을 남용한 것으로 보기 어려우며 징계절
- `id_56649` [disciplinary_severity]
  - 변경: notes
  - notes: 직장 내 성희롱의 징계사유가 인정되고, 징계양정이 과하지 않으며, 징계절차도 적법하므로 정당한 해고라고 판정한 사례 — 비위 인정이나 해고·징계

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
