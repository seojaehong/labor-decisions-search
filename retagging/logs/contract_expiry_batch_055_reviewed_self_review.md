# contract_expiry_batch_055_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_055_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_35819` [renewal_expectation]
  - 변경: notes
  - notes: 상시근로자수가 5인 이상 사업장으로 근로기준법 적용 대상이며 구제의 이익이 존재함에도 일방적으로 근로관계를 종료하면서 해고의 서면통지 의무를 위
- `id_35831` [renewal_expectation]
  - 변경: notes
  - notes: 재계약에 대한 갱신기대권이 인정되지 않으므로 근로관계는 계약기간 만료로 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 
- `id_35841` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 정규직으로 전환되거나 근로계약이 갱신될 수 있으리라는 정당한 갱신기대권이 있고, 그 갱신거절에 합리적인 사유가 없어 기간만료 통보는 부
- `id_35847` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신에 대한 기대권이 인정되지 않아 근로계약기간 만료에 따른 근로관계 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거
- `id_35861` [dismissal_validity]
  - 변경: notes
  - notes: 당사자 사이에 근로계약관계가 성립되었다고 볼 수 없어 근로자에게 구제신청의 당사자 적격이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
