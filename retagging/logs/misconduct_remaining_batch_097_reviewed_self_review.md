# misconduct_remaining_batch_097_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_097_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_41769` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차도 적법하여 해고는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판
- `id_41773` [misconduct]
  - 변경: notes
  - notes: 보호해야 할 장애인을 폭행·학대한 생활재활교사인 근로자에 대한 징계해고는 부당한 해고가 아니라고 판정한 사례 — 비위행위 존재 및 중대성이 해고
- `id_41787` [disciplinary_severity]
  - 변경: notes
  - notes: 반품절차 위반 및 고의적인 반품처리 지연에 의한 인센티브 부당 수령은 징계사유로 정당하고, 양정이 과하다고 볼 수 없으며, 절차상의 하자도 존재
- `id_41789` [disciplinary_severity]
  - 변경: notes
  - notes: 승객의 안전을 책임져야 하는 시내버스 운전기사인 근로자가 2017.부터 11건의 접촉사고 및 안전사고를 낸 것은 고용관계를 계속할 수 없을 정도
- `id_41793` [unfair_treatment]
  - 변경: notes
  - notes: 근로자들에 대한 승무정지는 정당하나, 해고는 양정이 과도하여 부당하고, 징계사유 대부분이 인정되고, 사용자의 부당노동행위 의사가 입증되지 않아 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
