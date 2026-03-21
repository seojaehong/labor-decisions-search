# contract_expiry_batch_116_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_116_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_59063` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되나 갱신 거절에 합리적인 이유가 있어 근로관계 종료가 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및
- `id_59079` [unfair_treatment]
  - 변경: notes
  - notes: 고용승계 기대권이 있는 근로자들의 고용승계를 합리적인 이유 없이 거절한 것은 부당해고에 해당하나, 불이익 취급 및 지배·개입의 부당노동행위에는 
- `id_591` [renewal_expectation]
  - 변경: notes
  - notes: 이 사건 근로자들에게는 촉탁직 재고용 기대권이 인정됨에도 이 사건 사용자가 합리적 이유 없이 재고용을 거절한 것은 부당해고에 해당하나, 사용자의
- `id_59103` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들은 일용근로자이므로 근로계약의 갱신기대권이 인정되지 않으며, 근로관계 만료 통보가 부당노동행위에 해당하지 않는다고 판정한 사례 — 갱신기
- `id_59105` [dismissal_validity]
  - 변경: notes
  - notes: 계약기간 만료에 따른 당사자 간 합의에 의해 근로관계가 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
