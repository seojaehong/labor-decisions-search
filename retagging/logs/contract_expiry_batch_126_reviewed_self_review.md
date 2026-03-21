# contract_expiry_batch_126_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_126_reviewed`
- 2차 패스 처리 건수: 47
- 실질 변경 건수: 47
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_9513` [renewal_expectation]
  - 변경: notes
  - notes: 사용자는 부당해고 구제신청 적용대상 사업장에 해당하고, 정규직 전환 기대권이 인정됨에도 불구하고 합리적인 이유 없이 정규직 전환을 거절하고 근로
- `id_9519` [discrimination]
  - 변경: notes, conf:high→medium
  - notes: 정년 후 기간제근로자로 재고용 기대권이 인정되고, 재고용 거절의 합리적 이유가 없어 재고용 거절이 부당하다고 판정한 사례 — discrimina
- `id_9533` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 만료로 근로관계가 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_9539` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약에 대한 갱신기대권이 존재한다고 보기 어렵다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_9545` [dismissal_validity]
  - 변경: notes
  - notes: 양 당사자 사이의 근로관계는 계약기간 만료로 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
