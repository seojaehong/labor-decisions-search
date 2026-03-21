# misconduct_remaining_batch_055_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_055_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_351023` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 인정되나 양정이 과하여 부당해고라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_351033` [disciplinary_severity]
  - 변경: notes
  - notes: 해고는 징계사유가 존재하고 양정도 적정하며 절차도 적법하므로 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 
- `id_351053` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 징계권자에게 맡겨진 징계재량권을 남용하였다고 볼 수 없으며 징계절차도 부당하다고 보기 어려우므로 해고처분이 정당하
- `id_351067` [misconduct]
  - 변경: notes
  - notes: 일부 징계사유가 인정되나, 징계양정이 과도하고, 근로자에게 충분한 소명기회를 부여하지 않은 징계절차상 위법이 있다고 판정한 사례 — 비위행위 존
- `id_351075` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 비위의 정도를 고려할 때 징계양정이 적정하며 징계절차상 하자가 없어 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
