# misconduct_remaining_batch_017_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_017_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_19081` [misconduct]
  - 변경: notes
  - notes: 기물을 파손하고, 문서를 외부로 유출하여 중요 계획이 중단되어 행한 ‘해임’의 징계는 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고
- `id_1909` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 인정되며 징계양정이 적정하고 관련 규정에 따라 절차를 준수하여 징계한 것으로 견책의 징계처분이 정당하며 이를 사용자의 부당노동행위 의
- `id_191` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자들의 비위행위는 징계사유에 해당하고 징계절차는 적법하나, 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심
- `id_19103` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 징계사유가 인정되나 그 비위행위의 정도에 비하여 정직 2개월 처분은 양정이 과하여 부당징계라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 
- `id_19113` [disciplinary_severity]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 양정이 과하여 부당해고에 해당한다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
