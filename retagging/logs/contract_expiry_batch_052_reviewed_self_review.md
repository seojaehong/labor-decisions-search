# contract_expiry_batch_052_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_052_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_350663` [renewal_expectation]
  - 변경: notes
  - notes: 당사자 간 근로계약기간 만료로 근로관계가 종료되었으며, 근로계약 갱신기대권이 인정될 만한 사정은 없다고 판정한 사례 — 갱신기대권 성립 여부 및
- `id_350687` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되지 않아 근로관계는 근로계약 기간만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱
- `id_350699` [renewal_expectation]
  - 변경: notes
  - notes: 근로자가 근로계약을 체결하기로 하고도 그만두겠다고 말한 후 출근하지 않아 근로관계가 종료된 것은 해고가 아니라고 판정한 사례 — 갱신기대권 성립
- `id_350701` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않으며, 설령 갱신기대권이 인정되더라도 근로자가 스스로 사직서를 제출하였으므로 해고는 존재하지 않는다고 판정한 
- `id_35073` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 사용자의 복직명령을 받고 출근을 하였고 해고기간에 대한 임금상당액도 모두 지급받아 구제신청의 목적이 달성되어 구제이익이 없다 고 판정한

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
