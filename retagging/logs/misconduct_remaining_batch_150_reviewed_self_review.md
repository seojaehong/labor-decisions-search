# misconduct_remaining_batch_150_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_150_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_8063` [unfair_treatment]
  - 변경: notes, conf:medium→high
  - notes: 1) 회사가 징계사유인 불성실 근로에 대한 입증을 하지 못하였으므로 부당한 징계에 해당하나,2) 사용자가 노동조합에 대하여 부당노동행위를 하였다
- `id_8085` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고 양정이 적정하며 절차에 하자도 없어 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_809` [disciplinary_severity]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_8091` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 징계절차에도 하자는 없으나, 인정되는 비위행위에 비해 그 양정이 과하여 해고처분은 부당하다고 판정한 사례 — 직장 내 
- `id_8093` [procedure]
  - 변경: notes
  - notes: 사용자가 징계사유 대부분을 입증하지 못하고, 근로자 비행의 정도에 비하여 징계양정이 과도하며, 취업규칙에서 정한 징계절차를 준수하지 않았으므로 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
