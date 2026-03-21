# contract_expiry_batch_028_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_028_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_27055` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로자에게 갱신기대권이 인정됨에도 합리적인 이유 없이 계약기간만료로 고용관계를 종료한 것은 부당하다고 판정한 사례 — 갱신기
- `id_27083` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'training_opportunity', 'dismissal_validity']
  - notes: 기간제 사용기간 제한의 예외기간 초과 시점에서 신규 채용절차를 거쳐 계속 근로하게 한 후 근로계약 만료를 이유로 근로관계를 종료한 것은 부당해고
- `id_27087` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 「근로기준법」상 근로자에 해당되고, 해고의 사유와 시기를 서면으로 통지하지 아니하여 부당하다고 판정한 사례 — worker_status 판단이 
- `id_27089` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약기간 만료에 따라 근로관계도 당연 종료된 것일 뿐, 해고에 해당하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 
- `id_27095` [renewal_expectation]
  - 변경: notes
  - notes: 촉탁계약기간 만료 통보는 배차거부(해고) 및 부당노동행위에 해당되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
