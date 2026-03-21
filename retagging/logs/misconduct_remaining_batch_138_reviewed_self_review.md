# misconduct_remaining_batch_138_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_138_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_58735` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 일부 인정되고 징계절차상 하자가 존재한다고 보기 어려우나 해고는 징계양정이 과하므로 부당하다고 판정한 사례 — 징계·해고 절차 하자가
- `id_58767` [misconduct]
  - 변경: notes
  - notes: 사유는 인정되나 양정이 과다하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_58777` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에 중대한 하자가 없어 강등의 징계가 정당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 
- `id_58779` [unfair_treatment]
  - 변경: notes, conf:medium→high
  - notes: 징계사유로 삼은 비위행위들이 객관적으로 확인되지 않아 징계사유 모두 부당하고, 징계해고절차에 중대한 하자가 존재하므로 부당해고이며, 불이익 취급
- `id_58807` [misconduct]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고, 일부 인정된 징계사유에 비해 그 양정이 과다하며, 징계 절차 또한 하자가 존재하여 부당해고라고 판정한 사례 — 비위행

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
