# misconduct_remaining_batch_049_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_049_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_347583` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 양정도 적정하고 절차도 적법하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_347585` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 양정도 적정하고 절차도 적법하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_347589` [misconduct]
  - 변경: notes
  - notes: 징계사유로 인정되지 않는 행위를 이유로 한 노동조합의 제명처분은 부당하다고 의결한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_34759` [misconduct]
  - 변경: notes
  - notes: 인정되는 징계사유의 중대성을 고려할 때 해고는 양정이 적정하며, 징계절차상의 하자도 없으므로 징계해고는 정당하다고 판정한 사례 — 비위행위 존재
- `id_347619` [misconduct]
  - 변경: notes
  - notes: 사용자가 징계사유로 삼은 근로자의 비위행위가 모두 징계사유로 인정되지 않아 견책처분이 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
