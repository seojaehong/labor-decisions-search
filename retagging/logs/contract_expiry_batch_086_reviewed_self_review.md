# contract_expiry_batch_086_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_086_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_42897` [dismissal_validity]
  - 변경: notes
  - notes: 근로자와 사용자는 3개월 기간을 정하여 시용근로계약을 체결하였고, 시용기간 중 당사자 간 근로계약을 종료하기로 합의하여 계약을 해지하였으므로 해
- `id_42945` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들은 기간의 정함이 있는 근로자에 해당하며, 근로형태, 근로계약의 경위 및 내용, 공사 및 공종의 진행 정도 등을 볼 때 근로계약의 갱신기
- `id_42983` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들에게 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없어 근로관계는 계약기간 만료로 당연 종료되었다고 판정한 사례 — 갱신기대권 성립 
- `id_4299` [discrimination]
  - 변경: notes, secondary:[]→['training_opportunity']
  - notes: 기간제근로자가 성과급 지급요건을 충족하지 못한 것을 이유로 성과급을 지급하지 아니한 것은 차별적 처우가 아니라고 판정한 사례 — discrimi
- `id_42999` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 있는 기간제근로자에 대해 계약기간 만료를 이유로 근로계약을 종료한 것은 근로계약 갱신거절의 합리적인 사유를 인정하기 어려우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
