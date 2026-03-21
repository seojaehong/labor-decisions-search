# contract_expiry_batch_050_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_050_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_349229` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신의 관행이 존재하여 촉탁직 근로계약 갱신기대권은 인정되나, 고령, 건강상태, 교통사고 이력 등을 고려하여 근로계약 갱신을 거절한 것
- `id_349249` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들에게 근로계약의 갱신기대권이 인정되나 사용자의 갱신거절에 합리적 이유가 있어 당사자 간 근로관계는 기간만료로 정당하게 종료되었다고 판정한
- `id_34925` [renewal_expectation]
  - 변경: notes
  - notes: 정규직전환 기대권이 있는 근로자를 근로계약기간 만료만을 사유로 근로관계를 종료한 것은 부당해고에 해당한다고 판정한 사례 — 갱신기대권 성립 여부
- `id_349255` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_349267` [dismissal_validity]
  - 변경: notes
  - notes: 해고가 존재하고 서면으로 통지하지 아니하여 절차상 하자가 있어 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
