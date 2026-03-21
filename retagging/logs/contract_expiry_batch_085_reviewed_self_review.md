# contract_expiry_batch_085_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_085_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_42165` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 근로자들이 기간제법의 적용 제외자에 해당하여 기간의 정함이 없는 근로자로 전환되었다고 보기 어렵고, 갱신기대권이 인정되며, 사용자의 갱신거절에 
- `id_4217` [discrimination]
  - 변경: notes, secondary:['unfair_treatment', 'dismissal_validity', 'renewal_expectation']→['misconduct', 'unfair_treatment', 'renewal_expectation', 'dismissal_validity']
  - notes: 명문 규정은 없지만 관행상 근로자들에게 근로계약의 갱신기대권이 인정되며 근로자1에 대한 갱신거절에는 합리적 이유가 없어 근로계약 갱신 거절은 부
- `id_42171` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약기간 중에 있는 근로자1에게 근로계약기간 만료로, 촉탁직 재고용 기대권이 있는 근로자2에게 합리적인 이유 없이 정년으로 근로관계를 종료한
- `id_42187` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 복직의사가 없고 근로계약기간이 만료되어 구제이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_42199` [renewal_expectation]
  - 변경: notes
  - notes: 기간제 근로자로서 계약기간이 만료됨으로써 근로관계는 종료되었고 근로자에게 갱신 기대권은 인정되나, 갱신거절의 합리적인 이유가 있다고 판정한 사례

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
