# contract_expiry_batch_042_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_042_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_34417` [worker_status]
  - 변경: notes, secondary:['dismissal_validity']→['training_opportunity', 'dismissal_validity']
  - notes: 근로자성은 인정되나, 당사자가 재고용 기간을 사전에 합의하고 계약기간 만료로 근로관계를 종료한 것은 정당하다고 판정한 사례 — worker_st
- `id_344181` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약기간만료를 사유로 근로계약이 종료되었고, 근로자에게 근로계약 갱신에 대한 기대권이 인정되지 않으므로 근로계약기간 만료에 의한 근로관계 종
- `id_344199` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없어, 근로계약기간 만료에 의한 근로관계 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부
- `id_34421` [discrimination]
  - 변경: notes
  - notes: 기간제근로자들에게 비교대상근로자에 비해 정액급식비, 교통보조비, 특수업무수당, 법정선임수당을 지급하지 않거나 적게 지급한 것은 불합리한 차별이라
- `id_344215` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 정규직 전환기대권이 인정되지 않아 당사자 간 근로관계는 근로계약기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
