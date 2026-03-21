# contract_expiry_batch_010_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_010_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_15831` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권은 인정되나, 갱신거절에 합리적 이유가 있어 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_1585` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'disciplinary_severity']
  - notes: 징계사유가 인정되고, 징계양정이 적정하며, 징계절차도 하자가 없어 징계해고가 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성
- `id_15877` [renewal_expectation]
  - 변경: notes
  - notes: 무기계약직 전환의 정당한 기대권이 있고, 그 거절의 합리적인 사유가 없음을 이유로 부당해고라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_15887` [worker_status]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['attendance', 'misconduct', 'renewal_expectation', 'dismissal_validity']
  - notes: 계약 갱신 거절에 합리적인 사유가 존재하므로 계약기간 만료에 따른 계약 종료로 보아 기각 판정한 사례 — worker_status 판단이 핵심
- `id_15921` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로계약에서 갱신기대권이 인정되지 않으므로 해고에 해당하지 아니한다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
