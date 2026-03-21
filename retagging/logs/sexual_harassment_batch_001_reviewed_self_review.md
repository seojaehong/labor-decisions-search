# sexual_harassment_batch_001_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_001_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `2024부해OOO` [disciplinary_severity]
  - 변경: notes
  - notes: 직장 내 성희롱이 인정되므로 징계사유가 존재하고, 근로자의 지위와 비위행위의 정도에 비추어 징계양정이 적정하며, 징계 절차에도 하자가 없어 해고
- `id_10049` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 징계사유가 일부 인정되고 징계절차도 적법하나 인정되는 징계사유에 비하여 징계양정이 과도하여 부당해고라고 판정한 사례 — 징계양정(제재 수위)의 
- `id_1015` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 양정이 적정하며, 절차에도 하자가 없어 강등 처분은 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부
- `id_10151` [disciplinary_severity]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 해고의 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_10179` [disciplinary_severity]
  - 변경: notes
  - notes: 직장 내 성희롱 등 세 가지의 징계사유가 인정되고, 비위행위 반복성 등으로 볼 때 해고처분은 양정이 과도하지 않으며, 해고통보 후 육아휴직 신청

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
