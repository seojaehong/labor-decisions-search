# contract_expiry_batch_007_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_007_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_14135` [renewal_expectation]
  - 변경: notes
  - notes: 기간제 근로자에게 근로계약 갱신기대권이 인정됨에도 합리적 사유 없이 계약 갱신을 거절한 것은 부당한 해고에 해당한다고 판정한 사례 — 갱신기대권
- `id_14161` [renewal_expectation]
  - 변경: notes
  - notes: 기간제법 제4조제1항제1호의 사업의 완료를 위한 기간제 근로자이나, 사업이 종료되지 않았으며 갱신기대권이 형성되었고 합리적인 갱신거절의 사유가 
- `id_14163` [dismissal_validity]
  - 변경: notes
  - notes: 사용자에게 당사자 적격이 인정되며, 근로계약기간 만료 이후에도 상당기간 계속 근로하던 근로자에 대해 계약기간 만료를 이유로 근로계약 해지를 통보
- `id_14191` [discrimination]
  - 변경: notes, secondary:['dismissal_validity']→['procedure', 'dismissal_validity']
  - notes: 정규직 전환에 대한 기대권이 인정되고, 정규직 전환 거절에 합리적 이유가 없어 부당해고로 판정한 사례 — discrimination 판단이 핵심
- `id_14201` [renewal_expectation]
  - 변경: notes
  - notes: 근로자의 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 종료된 것으로 해고에 해당하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
