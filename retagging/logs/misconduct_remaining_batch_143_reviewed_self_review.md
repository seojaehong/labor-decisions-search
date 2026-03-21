# misconduct_remaining_batch_143_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_143_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_60691` [misconduct]
  - 변경: notes
  - notes: 근로자의 비위행위가 해고사유에 해당하고 취업규칙상 근로자의 비위행위에 대하여 해고의 장과 징계의 장을 구분하여 규정하고 있으므로 징계위원회 의결
- `id_60697` [disciplinary_severity]
  - 변경: notes
  - notes: 견책은 징계사유가 존재하나 양정이 과도하여 부당하고, 변상처분은 그 밖의 징벌에 해당하나 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수
- `id_60701` [misconduct]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 근로자의 지위와 책임을 고려하면 인정되는 징계사유에 대하여 정직 3월의 징계양정이 과하다고 보기 어렵고 징계절차도 적법
- `id_60705` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차의 적법성이 인정되어 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_6071` [disciplinary_severity]
  - 변경: notes
  - notes: 인정징계사유는 일부 인정되나 징계양정이 과도하여 해고가 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
