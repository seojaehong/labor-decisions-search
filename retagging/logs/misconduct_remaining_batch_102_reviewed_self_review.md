# misconduct_remaining_batch_102_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_102_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_43817` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 인정되고, 징계양정이 과도하다고 볼 수 없으며, 징계절차에 하자가 없어 징계해고가 정당하다고 판정한 사례 — 비위 인정이나 
- `id_43829` [misconduct]
  - 변경: notes
  - notes: 인사명령(업무명령)은 구제이익이 없고, 대기명령도 정당하며, 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 2개월 정직처분
- `id_43833` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차도 적법하여해고처분은 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_43837` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 존재하고 징계절차는 적법하나 양정이 과하므로 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_43845` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 해고는 징계사유가 존재하고, 양정도 적정하며, 절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
