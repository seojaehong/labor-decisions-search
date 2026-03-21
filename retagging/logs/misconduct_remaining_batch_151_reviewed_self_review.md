# misconduct_remaining_batch_151_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_151_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_8511` [disciplinary_severity]
  - 변경: notes
  - notes: 보행자 아차사고, 업무지시 거부 및 관리자에 대한 막말 행위 등 징계사유가 인정되고, 징계양정이 적정하므로 해고가 정당하다고 판정한 사례 — 비
- `id_8515` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정도 적정하며, 징계절차에도 하자가 없어 징계해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌
- `id_8525` [workplace_harassment]
  - 변경: notes
  - notes: 직장 내 괴롭힘에 대한 원조사 결과로 근로자의 직장 내 괴롭힘에 대한 구체적인 사실관계가 객관적으로 입증되었다고 볼 수 없으므로 징계사유를 인정
- `id_8535` [misconduct]
  - 변경: notes
  - notes: 징계사유가 모두 인정되지 않으므로 징계해고는 부당하다고 판정한 사례 — 비위사실이 명확히 인정되어 해고 정당성 직접 좌우
- `id_8545` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 과도하다고 볼 수 없으며, 징계절차도 적법하여 해고가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
