# misconduct_remaining_batch_147_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_147_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_6855` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고 징계양정도 적정하며 징계절차에 하자가 없으므로 정직은 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_6859` [disciplinary_severity]
  - 변경: notes
  - notes: 금품수수 행위는 징계사유에 해당하나 해고의 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_6861` [unfair_treatment]
  - 변경: notes
  - notes: 정직은 사유에 비하여 양정이 과하여 부당하나, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심
- `id_6873` [unfair_treatment]
  - 변경: notes
  - notes: 근로자의 재물 손괴, 사내질서 문란 행위 등에 대한 정직 2월의 징계는 징계사유·양정·절차가 정당하며, 근로자의 행위가 정당한 노동조합 활동이라
- `id_6883` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되나 인정되는 징계사유에 비해 양정이 과다하여 부당해고라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
