# misconduct_remaining_batch_108_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_108_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_46295` [misconduct]
  - 변경: notes
  - notes: 전년 동기 대비 매출액이 상승하는 등 휴직명령의 업무상의 필요성이 존재하지 않고, 통상임금의 30%가 감소하는 상당한 경제적인 불이익을 입어 부
- `id_46303` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하지 않고, 근로기준법 제27조에서 정한 해고의 서면통지 절차를 위반하여 징계해고가 부당하다고 판정한 사례 — 소명기회 미부여 또
- `id_46323` [misconduct]
  - 변경: notes
  - notes: 무단결근이 징계사유로 인정되고 징계양정이 적정하며 징계절차에 하자가 없어 해고는 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당
- `id_46341` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 존재하고 징계절차도 적법하나, 징계양정이 과하여 부당한 해고라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_46379` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 자택대기 처분은 징계사유가 존재하고 절차상 하자는 없으나, 재량권을 남용하여 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
