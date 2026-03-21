# misconduct_remaining_batch_111_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_111_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_47531` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유에 비해 해고의 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_47537` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 정당한 것으로 인정되고, 징계양정이 적정하며, 징계절차에 하자가 없어 징계해고는 정당하다고 판정한 사례 — 징계양정(제재 수위)
- `id_47545` [unfair_treatment]
  - 변경: notes
  - notes: 사용자가 근로자들에게 행한 징계해고는 징계사유가 존재하지 않으므로 부당해고에 해당하나, 불이익 취급 및 지배·개입의 부당노동행위에는 해당하지 않
- `id_47559` [unfair_treatment]
  - 변경: notes
  - notes: 근로자의 징계사유 중 일부 징계사유만이 인정되고, 인정된 징계사유의 비위 정도와 징계의 형평성에 비추어 징계처분은 인사권을 남용한 것으로 보이므
- `id_47563` [misconduct]
  - 변경: notes
  - notes: 근로자가 거래업체로부터 다년간 향응을 제공받은 비위행위는 정당한 징계사유로 인정되고, 정직처분의 징계양정과 절차에 하자가 없음 — 비위행위 존재

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
