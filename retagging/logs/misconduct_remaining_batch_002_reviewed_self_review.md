# misconduct_remaining_batch_002_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_002_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_10585` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 근로자의 이사회 의사록 인장날인 오류, 노동조합 탈퇴 유발행위 외 다른 징계사유는 인정되지 않으므로 징계면직(해고)은 양정이 과다하여 부당하다고
- `id_10595` [procedure]
  - 변경: notes
  - notes: 징계사유가 존재하나, 근로자의 비위행위의 정도에 비하여 징계양정이 과도하므로 부당한 해고라고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접
- `id_10609` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 특정되지 않아 징계 자체가 부당하며, 설령 징계사유가 특정되었더라도 인정되는 사유에 비해 양정이 과하여 정직의 징계는 부당하다고 판정
- `id_1063` [misconduct]
  - 변경: notes
  - notes: 징계위원으로서 행한 징계 심의 및 의결 행위가 징계사유에 해당하지 않는다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_10651` [misconduct]
  - 변경: notes
  - notes: 징계사유가 객관적으로 입증되지 않아 해고의 징계처분은 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
