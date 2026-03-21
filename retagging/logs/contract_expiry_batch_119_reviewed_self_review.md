# contract_expiry_batch_119_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_119_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_60927` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['attendance', 'procedure', 'dismissal_validity']
  - notes: 시용 근로자에 해당하고 해고 사유가 인정되며 절차에 하자도 없어 해고가 정당하다고 판정한 사례 — worker_status 판단이 핵심
- `id_60949` [discrimination]
  - 변경: notes
  - notes: 기간제근로자가 아닌 자들이 차별시정을 신청한 것으로 당사자적격이 인정되지 않는다고 판정한 사례 — discrimination 판단이 핵심
- `id_61013` [renewal_expectation]
  - 변경: notes
  - notes: 근로자를 1일 단위로 근로계약을 체결하는 일용근로자로 보아 해고가 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 
- `id_61029` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되나, 갱신거절에 합리적인 이유가 있어 근로관계 종료가 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및
- `id_6105` [dismissal_validity]
  - 변경: notes
  - notes: 일반직(무기계약직) 전환기대권은 인정되나, 일반직 전환을 거절할 합리적 이유가 있다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
