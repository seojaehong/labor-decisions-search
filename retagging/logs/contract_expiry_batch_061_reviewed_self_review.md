# contract_expiry_batch_061_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_061_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_38693` [renewal_expectation]
  - 변경: notes
  - notes: 기각 - 특정한 업무의 완성에 필요한 기간을 정하여 채용되었으므로 2년을 초과하여 계속 근로하였더라도 기간의 정함이 없는 근로자로 전환되지 않고
- `id_38701` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자 사용기간 제한의 예외 사유에 해당하는 근로자로 무기계약으로 전환되었다고 볼 수 없으며 근로계약에 대한 갱신기대권 내지 정규직 전환 
- `id_38709` [renewal_expectation]
  - 변경: notes
  - notes: 당사자 간 근로관계는 임기 만료 또는 사직서 제출로 인해 종료되었고 근로계약의 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여
- `id_38721` [renewal_expectation]
  - 변경: notes
  - notes: 일용근로자로서 계약기간 만료에 따라 근로관계가 종료되었으며, 갱신기대권 또한 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_38729` [renewal_expectation]
  - 변경: notes
  - notes: 정규직 전환 기대권이 인정되나, 정규직 전환 면접평가에서 불합격되어 근로계약만료를 한 것으로 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
