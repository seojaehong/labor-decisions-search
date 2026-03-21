# contract_expiry_batch_087_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_087_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_43617` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약 만료일 도래 전 자의로 퇴사하였으므로 부당해고에 해당하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_43627` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들이 일용직이 아닌 기간제근로자이기는 하나, 근로계약 갱신기대권이 인정되지 않아 근로관계는 근로계약기간의 만료로 종료된 것이므로 해고가 존
- `id_43647` [dismissal_validity]
  - 변경: notes
  - notes: 근로자들은 기간제근로자에 해당하여 공사가 완료됨에 따라 계약기간 만료로 근로관계가 종료된 것으로 해고가 존재하지 않는다고 판정한 사례 — 해고 
- `id_4365` [dismissal_validity]
  - 변경: notes
  - notes: 회사의 상시근로자 수가 5명 이상이므로 근로기준법에서 정한 부당해고등 구제신청에 관한 규정이 적용되고, 해고사유와 해고시기를 서면으로 통지하지 
- `id_43667` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 정년 후 재고용기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
