# misconduct_remaining_batch_009_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_009_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_1445` [procedure]
  - 변경: notes, conf:medium→high
  - notes: ""기각""징계사유가 인정되고, 징계양정이 타당하며, 징계절차에 하자가 없다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_14465` [disciplinary_severity]
  - 변경: notes
  - notes: 차내 안전사고 유발 등 징계사유가 인정되어 정직 5일로 징계한 것은 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 
- `id_14477` [misconduct]
  - 변경: notes
  - notes: 부하직원에 대한 관리감독의무 위반의 징계사유가 인정되므로 이를 이유로 행한 징계해고 처분은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이
- `id_14489` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유와 절차의 정당성은 인정되나 징계양정이 과하여 부당하고, 부당노동행위 의사에서 비롯된 것으로 볼 만한 근거가 없다고 판정한 사례 — 부당
- `id_14497` [misconduct]
  - 변경: notes
  - notes: 단체협약의 내용과 달리 징계절차를 거치지 아니하고 행한 징계처분은 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
