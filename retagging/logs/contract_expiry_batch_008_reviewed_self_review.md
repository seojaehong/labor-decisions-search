# contract_expiry_batch_008_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_008_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_14677` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 기간제 근로계약을 체결한 근로자로서 갱신기대권이 인정되지 않으므로 계약기간 만료로 고용관계를 종료한 것은 정당하다고 판정한 사례 — discri
- `id_14699` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로계약이고, 갱신기대권은 인정되나 갱신 거절의 합리적인 이유가 있어 부당한 해고가 아니라고 판정한 사례 — 갱신기대권 성립
- `id_14701` [renewal_expectation]
  - 변경: notes
  - notes: 근로자가 사직서 제출 후 체결한 기간제 근로계약기간이 만료되었고, 근로자에게 갱신기대권이 인정된다고 보기 어려우므로 근로계약기간 만료는 해고가 
- `id_14721` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약기간이 형식적이거나 근로계약 갱신기대권이 인정된다고 볼 수 없어 근로계약기간의 만료로 고용관계가 종료되었다고 판정한 사례 — 갱신기대권 
- `id_14727` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 계약기간 만료에 의해 근로관계가 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
