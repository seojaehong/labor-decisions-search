# misconduct_remaining_batch_086_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_086_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_409169` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 중 일부가 인정되나 정직 2개월의 징계양정이 과도하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_40917` [disciplinary_severity]
  - 변경: notes
  - notes: 동료 미화원에 대한 언어폭력, 근태불량 등의 행위는 모두 징계사유에 해당하고, 비위행위로 인한 직원 상호간 협력적 업무분위기 방해, 조직질서 저
- `id_409185` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부만 인정되며, 인정되는 징계사유에 비해 양정이 과도하여 정직 3개월의 징계가 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적
- `id_409191` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차에도 하자가 없어 해고는 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_409195` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 대부분 인정되고, 인정되는 징계 사유만으로도 징계양정이 과도하다고 볼 수 없으며 징계절차도 적법하다고 판정한 사례 — 징계양정(제재 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
