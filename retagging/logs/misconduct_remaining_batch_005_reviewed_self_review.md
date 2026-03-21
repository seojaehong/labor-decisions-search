# misconduct_remaining_batch_005_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_005_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_12143` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유 중 일부가 인정되고, 징계절차에 중대한 하자가 없으나, 비위행위의 정도에 비해 ‘강등’의 중징계 처분은 양정이 과도하여 강등은
- `id_12149` [misconduct]
  - 변경: notes
  - notes: 의약품 영업 담당자가 보건의료전문가에게 부당한 향응을 제공하고 제품설명회를 진행하면서 1인당 식사비용 한도액을 초과하였으며 경비지출내역을 허위로
- `id_1215` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당한 해고라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여
- `id_12155` [disciplinary_severity]
  - 변경: notes
  - notes: 대출상담을 이유로 여성 고객을 술자리에 부른 비위행위가 언론에 보도되어 사용자의 명예가 훼손되는 등의 징계사유가 모두 인정되고, 징계양정이 적정
- `id_12157` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대해 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에 하자가 없어 해고는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
