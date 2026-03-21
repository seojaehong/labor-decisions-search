# misconduct_remaining_batch_077_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_077_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_404789` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정이 징계권자에게 맡겨진 징계재량권을 남용하였다고 볼 수 없으며, 징계절차에 중대한 하자가 있다고 보기 어렵다고 판정
- `id_404797` [disciplinary_severity]
  - 변경: notes
  - notes: 6가지 비위행위 중 장기간 출퇴근시간 및 재택근무제 운영지침 등을 위반한 행위는 징계사유가 인정되나, 비위행위의 경위와 사용자의 관리ㆍ감독 현황
- `id_40481` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 징계절차의 하자는 확인되지 않으나 그 비위행위의 정도에 비하면 해고는 징계양정이 과도하다고 판정한 사례 — 징계양정(제
- `id_404811` [misconduct]
  - 변경: notes
  - notes: 해외 법인에서 근무하면서 각종 수당을 과다하게 수령한 점, 해외 법인에서 상위관리자로 근무하여 수당 및 복리후생 규정을 일반 직원보다 잘 숙지하
- `id_404821` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 일부 인정되나 징계양정이 과하여 해고가 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
