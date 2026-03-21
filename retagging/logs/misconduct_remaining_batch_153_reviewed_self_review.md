# misconduct_remaining_batch_153_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_153_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_911` [disciplinary_severity]
  - 변경: notes
  - notes: 유류비 횡령, 판매병들에 대한 욕설 등의 비위행위는 정당한 해고사유에 해당되고, 징계양정 및 절차도 정당하다고 판정한 사례 — 징계양정(제재 수
- `id_9113` [misconduct]
  - 변경: notes
  - notes: 해고가 존재하고, 해고사유의 정당성이 없어 부당한 해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_9121` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에게 대금 지연지급 등의 징계사유가 인정되고, 징계양정이 과도하지 않으며, 징계절차도 적법하여 해고가 정당하다고 판정한 사례 — 비위 인정
- `id_9131` [misconduct]
  - 변경: notes
  - notes: 징계위원회 구성에 중대한 하자가 있으므로 징계가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_9133` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 징계처분이 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
