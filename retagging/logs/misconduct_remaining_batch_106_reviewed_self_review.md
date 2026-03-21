# misconduct_remaining_batch_106_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_106_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_45517` [misconduct]
  - 변경: notes
  - notes: 총괄관리자임에도 인사업무 및 관련 문서의 관리를 소홀히 한 행위는 징계사유로 인정되나, 그 사유에 비해 양정이 과도하여 부당하다고 판정한 사례 
- `id_45525` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재 하고, 징계양정도 적정하며, 징계절차도 적법하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_45535` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 과하다고 보기 어려우며 징계절차도 적법하여 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직
- `id_45541` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 적정하며, 징계절차에 하자가 없어 정당한 해고라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부
- `id_45547` [disciplinary_severity]
  - 변경: notes
  - notes: 사용자가 비위행위로 삼은 징계사유 중 일부만 인정되고, 징계사유에 비해 해고는 징계양정이 과도하다고 판정한 사례 — 징계양정(제재 수위)의 적정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
