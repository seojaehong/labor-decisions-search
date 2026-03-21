# misconduct_remaining_batch_092_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_092_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_411983` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 중 일부가 인정되지 않아 정직 3월의 양정이 과하고, 징계절차도 위법하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_411989` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정이 적정하며, 징계절차에 하자가 없어 해임 처분이 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한
- `id_412005` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 과도하다고 볼 수 없으며, 징계절차상 하자도 없으므로 정직 처분은 정당하다고 판정한 사례 — 비위 인정이나 해고
- `id_412041` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계재량권을 남용했다고 보이지 않으며 절차상으로도 하자가 있다고 보기 어려워 해고가 정당하다고 판정한 사례 — 비위 인정이나
- `id_41207` [misconduct]
  - 변경: notes, conf:high→medium
  - notes: 사용자의 지시에도 불구하고 동료 근로자가 횡령하였다며 다른 근로자, 사용자 및 도급인 관계자 등에게 수차 문제 제기한 것은 정당한 징계사유가 된

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
