# contract_expiry_batch_077_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_077_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_409159` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자에게 근로계약 갱신에 대한 기대권이 존재하지 않아 근로계약 기간만료에 따른 근로관계 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부
- `id_409193` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자에게 정규직 전환기대권이 존재하고, 정규직 전환거절의 합리인 이유가 없다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이
- `id_409227` [renewal_expectation]
  - 변경: notes
  - notes: 재계약 요건 및 절차에 관한 규정이 없는 점, 기간제법에서 사용 기간 제한의 예외를 인정하는 전문직의 경우 갱신기대권을 엄격하게 봐야 하는 점 
- `id_409229` [renewal_expectation]
  - 변경: notes
  - notes: 고용승계 기대권이 인정되지 않고, 계약기간 만료에 따라 근로관계가 종료된 것이므로 부당해고가 아니라고 판정한 사례 — 갱신기대권 성립 여부 및 
- `id_409235` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 기간제근로자에 해당하고 계약기간만료로 근로관계가 종료되었으며, 구제신청을 할 당시 이미 근로자의 지위를 벗어났으므로 부당해고에 대한 구제신청의 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
