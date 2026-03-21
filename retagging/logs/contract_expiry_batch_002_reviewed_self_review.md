# contract_expiry_batch_002_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_002_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_10569` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자는 기간제근로자로서 근로계약 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여
- `id_10587` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'training_opportunity', 'dismissal_validity']
  - notes: 근로자는 방송국에서 디지털뉴스 그래픽 제작 업무를 수행한 근로기준법상 근로자에 해당하고, 기간의 정함이 없는 근로계약을 체결한 근로자로 전환된 
- `id_10617` [renewal_expectation]
  - 변경: notes
  - notes: 당사자 간 근로관계는 계약기간이 만료됨으로써 종료되었고, 근로자에게 근로계약의 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여
- `id_10623` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로자들은 기간의 정함이 없는 근로자이고, 근로자들을 해고하면서 해고의 서면통지 절차를 위반하여 부당하다고 판정한 사례 — 해고 사실 자체의 존
- `id_10625` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약기간이 형식에 불과하다고 볼 수 없고, 근로계약 갱신기대권이 인정되지 않아 당사자 간 근로관계는 근로계약기간이 만료됨으로써 종료되었다고 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
