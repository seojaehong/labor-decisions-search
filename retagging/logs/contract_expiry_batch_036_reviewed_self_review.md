# contract_expiry_batch_036_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_036_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_30905` [dismissal_validity]
  - 변경: notes
  - notes: 사용자2가 독립된 법인이라 볼 수 있으므로 노동관계법상 권리·의무의 주체가 될 수 있고, 구제신청을 다투던 중 근로자의 근로계약 기간이 종료되어
- `id_30927` [renewal_expectation]
  - 변경: notes
  - notes: 정규직 전환 기대권이 인정되지 않아 근로계약기간 만료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_30933` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약기간이 만료됨에 따라 구제이익이 소멸되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_30945` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['training_opportunity', 'dismissal_validity']
  - notes: 기간제근로자로서 당사자 간 근로관계는 계약기간이 만료됨으로써 종료되었고, 근로자에게 근로계약의 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱
- `id_30949` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되는 근로자들을 합리적 이유 없이 계약만료 통지한 것은 부당해고라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
