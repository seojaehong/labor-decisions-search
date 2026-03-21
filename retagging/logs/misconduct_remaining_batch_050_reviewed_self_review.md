# misconduct_remaining_batch_050_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_050_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_348127` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 일부 징계사유가 존재하고 징계절차에 하자는 없으나, 인정되는 징계사유에 비해 징계양정이 과하여 부당하다고 판정한 사례 — 징계·해고 절차 하자가
- `id_348139` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자의 어떠한 행위가 징계사유로 된 것인지 특정하기 어렵고, 해고사유의 서면통지 의무를 위반하여 부당하다고 판정한 사례 — 소명기회 미부여 또
- `id_34815` [misconduct]
  - 변경: notes
  - notes: 인정되는 징계사유에 비해 해고는 그 양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_348165` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되나 징계양정이 과도하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_348209` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 비위행위는 징계사유에 해당하고, 그 비위행위의 정도에 비하면 견책 처분은 징계양정이 과도하다고 볼 수 없으며, 징계절차에 하자가 없으므

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
