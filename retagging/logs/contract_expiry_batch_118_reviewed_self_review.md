# contract_expiry_batch_118_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_118_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_60279` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되지 않고, 계약기간 만료에 따라 근로관계가 종료된 것이므로 부당해고가 아니라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거
- `id_60285` [worker_status]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 기간제 근로자에 해당하고 갱신기대권이 존재하지 않으므로 계약만료에 따른 근로계약 종료는 정당하다고 판정한 사례 — worker_status 판단
- `id_60287` [renewal_expectation]
  - 변경: notes
  - notes: 흡수합병한 법인 사이에 고용승계는 흡수합병 당시 근로관계를 유지하고 있었던 근로자에 한정되고, 흡수합병 이전에 근로관계가 종료된 근로자에게는 고
- `id_60303` [dismissal_validity]
  - 변경: notes
  - notes: 근로자들은 기간제근로자이고 근로계약 기간의 만료로 근로관계가 종료되었다고 판단되므로 해고가 존재하지 않아 기각한 사례 — 해고 사실 자체의 존부
- `id_6031` [dismissal_validity]
  - 변경: notes
  - notes: 당사자 간 의사가 일치되지 않아 근로계약이 갱신되지 않고 근로관계가 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
