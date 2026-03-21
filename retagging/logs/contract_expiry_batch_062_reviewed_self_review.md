# contract_expiry_batch_062_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_062_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_39471` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계가 당사자 간 합의에 의하여 종료되지 않았으므로 해고에 해당하고, 기간의 정함이 없는 근로자를 계약기간 만료를 이유로 해고한 것은 부당하
- `id_39481` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자로서 근로계약기간이 만료되었고 근로계약의 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵
- `id_39501` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약에 대한 갱신기대권이 인정되나 갱신거절에 합리적인 이유가 있어 재계약 거부는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_39509` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되지 않아 근로계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_39513` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자가 계약기간 만료에 따라 근로관계가 종료된 것으로 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
