# sexual_harassment_batch_004_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_004_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_27861` [disciplinary_severity]
  - 변경: notes
  - notes: 후배 여직원에게 신체접촉 등 직장 내 성희롱을 한 근로자에 대한 해고는 징계양정이 적정하고, 징계절차를 준수하여 정당하다고 판정한 사례 — 징계
- `id_27877` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 근로자가 성추행 가해자로 지목한 상급자로부터 해고통보 및 사직요구를 받고 퇴직일자 및 퇴직사유가 미리 작성된 사직서에 서명한 것은 사직의 의사표
- `id_27899` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 언어적 성희롱 행위는 인정되나, 해고처분은 사유에 비하여 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심
- `id_27941` [misconduct]
  - 변경: notes
  - notes: 동료 여직원에게 외모를 비하하는 지속적인 성희롱을 한 데 대해 정직 1월의 징계를 한 것은 정당한 징계권의 행사라고 판정한 사례 — 비위행위 존
- `id_27949` [disciplinary_severity]
  - 변경: notes
  - notes: 부서장으로서 어린 여직원에게 성희롱적 언동을 한 것은 징계사유로 인정되나 해고는 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
