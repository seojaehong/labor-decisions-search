# misconduct_remaining_batch_066_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_066_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_39585` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유에 비해 양정이 과하므로 징계권 남용에 해당한다고 판정 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_3959` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유는 모두 인정되나, 비위행위의 정도와 징계 형평성 등을 고려할 때 해임은 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재
- `id_39591` [disciplinary_severity]
  - 변경: notes, conf:medium→high
  - notes: 근로자의 징계사유 중 일부는 징계사유로 인정되고, 징계처분1(감봉 1개월)은 사용자의 정당한 재량권의 행사로 그 양정이 과하다고 할 수 없으나,
- `id_39615` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유중 일부는 부당하나 징계양정 및 절차는 적정하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_39617` [disciplinary_severity]
  - 변경: notes
  - notes: 사용자가 근로자들에게 행한 징계해고를 사유의 존재·양정의 적정성·절차의 정당성에 따라 판단하였을 때, 다른 근로자에 비해 책임이 가벼운 근로자에

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
