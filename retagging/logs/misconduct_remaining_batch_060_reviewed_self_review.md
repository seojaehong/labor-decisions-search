# misconduct_remaining_batch_060_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_060_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_3677` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유의 대부분이 인정되고, 징계양정이 적정하며, 절차상 하자도 없어 정직 3월의 징계는 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결
- `id_36771` [disciplinary_severity]
  - 변경: notes
  - notes: 징계 사유가 인정되나 징계 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_3679` [misconduct]
  - 변경: notes
  - notes: 근로자가 출판사와 상업 출판에 대한 협의를 하였다고 해서 출판사가 상업 출판계약의 체결 없이 책을 출판한 것이 근로자의 책임이라고 볼 수 없으므
- `id_36793` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차에 하자가 없으므로 징계해고는 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_36831` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure']
  - notes: 징계사유가 인정되고, 징계 절차상의 하자도 없으며, 정직 처분이 재량권을 일탈·남용한 것이라고 볼 수 없어 정당한 처분이라고 인정한 사례 — 비

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
