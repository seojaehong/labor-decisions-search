# misconduct_remaining_batch_029_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_029_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_25763` [misconduct]
  - 변경: notes
  - notes: 사용자가 근로자의 사내 교제 등을 이유로 정직 3월의 징계 처분을 한 것은 징계사유의 정당성이 없어 부당하다고 판정한 사례 — 비위행위 존재 및
- `id_25773` [disciplinary_severity]
  - 변경: notes
  - notes: 상시 근로자 수가 5명 이상이고, 회사 규정에 반하여 부당한 업무지시를 한 행위 등이 징계사유로 인정되나, 고용관계를 계속할 수 없을 정도로 책
- `id_25785` [misconduct]
  - 변경: notes
  - notes: 원산지 거짓 표시 및 품질보증관련 서류의 위조와 변조 등의 징계사유가 인정되고 절차상 하자도 없어 정당한 해고라고 판정한 사례 — 비위행위 존재
- `id_2579` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 양정이 과하지 않으며, 절차에도 하자가 없어 해고는 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_25815` [disciplinary_severity]
  - 변경: notes
  - notes: 유죄 확정판결 이전에도 사용자가 징계혐의 사실을 인정하여 징계 처분을 하는 것이 무죄 추정의 원칙에 저촉되는 것은 아니라고 판정한 사례 — 징계

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
