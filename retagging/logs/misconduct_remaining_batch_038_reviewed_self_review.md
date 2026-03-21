# misconduct_remaining_batch_038_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_038_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_31699` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자에게 징계원인이 된 비위행위를 구체적으로 통보하지 않아 소명 기회를 제대로 보장하지 않은 절차상 하자가 존재하여 사용자가 근로자에게 행한 
- `id_31715` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 사용자가 근로관계를 종료한 것은 해고이고, 해고의 서면통지 절차를 위반하여 부당해고라고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성
- `id_31719` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 공공기관 직원으로서 성실·품위유지 의무를 위반한 행위는 징계사유에 해당하고, 양정이 적정하며 절차에도 하자가 존재하지 않으므로 해고는 정당하다고
- `id_31735` [disciplinary_severity]
  - 변경: notes
  - notes: 허위사실 적시로 동료직원의 명예를 훼손한 징계사유는 인정되나, 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심
- `id_31737` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하지 않음에도 노동조합이 조합원에 대하여 징계를 결의ㆍ처분한 것은 규약에 위반된다고 의결한 사례 — 비위행위 존재 및 중대성이 해

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
