# misconduct_remaining_batch_026_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_026_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_23815` [disciplinary_severity]
  - 변경: notes
  - notes: 재직근로자가 학력증명서 등 서류제출요구를 거부한 행위에 대해 정직 6개월 처분한 것은 정당하다고 판정 — 징계양정(제재 수위)의 적정성이 핵심 
- `id_23825` [disciplinary_severity]
  - 변경: notes
  - notes: 은행원의 사문서 위조, 여신업무 취급 불철저, 고객정보 임의 변경 등의 행위는 징계사유로 정당하나 인정되는 비위행위의 정도에 비하여 해고는 양정
- `id_23847` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 반출절차에 대한 내부규정을 위반한 행위는 징계사유로 타당하나, 고용관계를 지속할 수 없을 정도로 신뢰관계가 훼손된 것은 아니라고 판정한 사례 —
- `id_23851` [disciplinary_severity]
  - 변경: notes
  - notes: 회계처리 부적정과 변상 지시 불이행을 사유로 행한 해고는 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_23877` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 인정되나 양정이 과다하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
