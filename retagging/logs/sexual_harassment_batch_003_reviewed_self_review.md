# sexual_harassment_batch_003_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_003_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_21565` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되나, 제반사정을 고려할 때 징계양정이 지나치게 과하여 해고가 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지
- `id_21627` [disciplinary_severity]
  - 변경: notes
  - notes: 성희롱 행위에 해당하여 징계사유는 인정되나 해고는 양정이 과다하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_21799` [disciplinary_severity]
  - 변경: notes
  - notes: 사용자가 성추행을 이유로 근로자를 해고한 것은 정당하다고 판정 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_21813` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 징계를 감경받을 목적으로 사직서 제출의사를 밝힌 확약서로 징계를 감경받고 그 이행을 하지 아니한 행위를 기망행위로 하여 근로자를 해고한 것은 양
- `id_22223` [misconduct]
  - 변경: notes
  - notes: 근로자가 워크숍 행사 중 동료 여성근로자 3명을 성희롱한 것을 이유로 해고한 것은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
