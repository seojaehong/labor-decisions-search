# misconduct_remaining_batch_061_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_061_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_37159` [unfair_treatment]
  - 변경: notes, conf:high→medium
  - notes: 징계가 사유는 인정되나 양정이 과하여 부당하지만, 부당노동행위 의사에 기인한 것이라고 단정할 수 없어 불이익 취급 및 지배·개입의 부당노동행위는
- `id_37163` [disciplinary_severity]
  - 변경: notes
  - notes: 징계양정 과다 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_37167` [misconduct]
  - 변경: notes
  - notes: 노동조합이 조합원들에게 행한 징계처분은 징계사유에 해당하지 않아 노동조합 규약에 위반된다고 의결한 사례 — 비위행위 존재 및 중대성이 해고 정당
- `id_3717` [unfair_treatment]
  - 변경: notes, conf:high→medium
  - notes: 징계사유가 일부 인정되지 않아 양정이 과하여 부당하며, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부
- `id_37187` [disciplinary_severity]
  - 변경: notes
  - notes: 폭행에 대한 징계사유는 인정되나, 양정이 과하고, 단체협약 규정을 위반하여 개최된 징계위원회 처분은 중대한 징계절차의 하자라고 판단한 사례 — 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
