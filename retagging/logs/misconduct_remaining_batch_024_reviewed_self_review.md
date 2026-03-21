# misconduct_remaining_batch_024_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_024_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_22695` [disciplinary_severity]
  - 변경: notes
  - notes: 직무관련자로부터 향응을 제공받은 것을 사유로 해임한 것은 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_22699` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하지 않아 부당한 무기한 정직처분으로 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_22719` [misconduct]
  - 변경: notes
  - notes: 징계사유는 정당하나 제 규정을 준수하지 않는 등 징계절차를 위반하고 징계양정도 과하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을
- `id_22725` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 인정되지 않으며 노동조합 위원장에 대한 해고는 불이익 취급의 부당노동행위에 해당된다고 판정한 사례 — 부당노동행위(불이익취급·지배개입
- `id_2273` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자가 대표이사의 사업추진 불가 지시에도 불구하고 지속적으로 사업을 추진하는 등의 징계사유가 일부 인정되나 징계의 형평성 등에 비추어 해고는 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
