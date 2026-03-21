# contract_expiry_batch_026_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_026_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_257` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되지 않아 근로계약기간 만료에 따라 근로관계가 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 
- `id_25731` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계 종료에 있어 사용자는 파견사업주이고, 파견계약 만료에 따른 근로계약 종료는 해고에 해당하지 않는다고 판정한 사례 — 해고 사실 자체의 
- `id_25771` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권은 있으나 갱신거절의 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_25787` [renewal_expectation]
  - 변경: notes
  - notes: 계약기간 만료로 근로관계 종료 후 20여 일이 지나 새로 채용된 경우에는 계속 근로한 것이 아니므로 무기계약직으로 전환된 것으로 볼 수 없고 갱
- `id_25809` [dismissal_validity]
  - 변경: notes
  - notes: 조합에서 운영하던 의원이 폐업되고 개인이 인수하면서 근로관계를 포함한 포괄적 양도·양수가 이루어졌음에도 고용배제의 특약을 이유로 고용을 승계하지

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
