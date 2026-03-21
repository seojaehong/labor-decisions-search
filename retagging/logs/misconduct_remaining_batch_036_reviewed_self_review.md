# misconduct_remaining_batch_036_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_036_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_30497` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정은 적정하며 징계절차도 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우
- `id_30499` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 인정되는 징계사유에 비해 징계해직 처분이 과하다고 볼 수 없고, 징계절차상 하자도 없어 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을
- `id_30509` [disciplinary_severity]
  - 변경: notes
  - notes: 업무수행 과정에서 행동규범 등을 위반한 행위는 징계사유에 해당하나, 그 비위행위의 정도에 비해 해고는 사회통념상 타당성을 잃어 징계 재량권을 남
- `id_3051` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자들에 대한 징계사유는 인정됨. 근로자1에 대한 해고처분은 징계사유에 비해 양정이 과하다고 볼 수 없고 징계절차도 적법하여 정당하나 근로자2
- `id_30517` [misconduct]
  - 변경: notes
  - notes: 근로자에 대한 해임처분은 징계사유에 비하여 양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
