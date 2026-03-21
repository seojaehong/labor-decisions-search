# misconduct_remaining_batch_095_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_095_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_413439` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 일부 징계사유만 정당한 징계사유로 인정되고, 각 징계사유에 참작할 만한 사정이 있는바, 인정되는 징계사유만으로 파면의 양정은 과도하다고 판정한 
- `id_413445` [procedure]
  - 변경: notes
  - notes: 징계사유 네 가지가 모두 정당한 징계사유로 인정되고, 최소 수위의 징계인 견책의 양정이 과도하다고 볼 수 없으며, 특별한 절차상 하자도 발견되지
- `id_41345` [disciplinary_severity]
  - 변경: notes
  - notes: 일부 징계사유가 인정되나 징계 양정이 과도하고 징계절차에도 하자가 있어 해고는 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한
- `id_413453` [disciplinary_severity]
  - 변경: notes, conf:medium→high
  - notes: 일부 징계사유가 인정되나, 비위행위의 경위, 근로자의 공적, 개전의 정 등 참작 사유가 있음에도 사용자가 징계재량권을 행사하지 않았으므로 징계면
- `id_413455` [disciplinary_severity]
  - 변경: notes
  - notes: 환자에 대한 서비스 소홀, 시술 중 발생한 과실에 대한 후속 조치 미비, 기본 업무 수칙 미준수 등의 행위는 정당한 징계사유로 인정되고, '감봉

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
