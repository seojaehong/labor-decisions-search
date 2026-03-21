# contract_expiry_batch_005_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_005_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_1273` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 정규직 전환기대권이 존재하지 않아 근로관계는 계약만료에 의해 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 
- `id_12739` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 갱신기대권이 인정된다고 하더라도, 갱신거절에 사회통념상 합리적 이유가 있어 부당해고에 해당하지 않는다고 판정한 사례 — discriminatio
- `id_12765` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않으므로 근로계약기간 만료에 따른 근로관계의 종료라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이
- `id_12775` [renewal_expectation]
  - 변경: notes
  - notes: 무기계약직 전환에 대한 기대권이 인정된다고 보기 어려워 근로계약만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 
- `id_12781` [discrimination]
  - 변경: notes
  - notes: 현저한 업무성격 차이가 있는 다른 기간제 근로자들이 무기계약직으로 전환된 사례가 있다는 것만으로는 기대권이 없다고 판정한 사례 — discrim

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
