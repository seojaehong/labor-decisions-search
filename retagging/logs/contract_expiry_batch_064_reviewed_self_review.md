# contract_expiry_batch_064_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_064_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_400829` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되나, 갱신 거절에 합리적인 이유가 존재하지 않으므로 사용자가 계약만료로 근로계약을 종료한 것은 부당하다고 판정한 사례
- `id_400831` [renewal_expectation]
  - 변경: notes
  - notes: 정규직 전환기대권이 인정되고, 정규직 전환 거절에 합리적인 이유가 없으므로 사용자가 계약만료로 근로계약을 종료한 것은 부당하다고 판정한 사례 —
- `id_400847` [dismissal_validity]
  - 변경: notes
  - notes: 해고 사실이 인정되고, 해고사유와 절차에 하자가 있어 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_400867` [renewal_expectation]
  - 변경: notes
  - notes: 기간제 근로자의 갱신기대권이 인정되지 않으므로, 근로계약기간 만료에 따라 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거
- `id_400893` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로관계 종료 이후 구제신청을 한 것으로 구제이익이 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
