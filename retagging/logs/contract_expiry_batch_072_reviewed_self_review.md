# contract_expiry_batch_072_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_072_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_405713` [discrimination]
  - 변경: notes
  - notes: 근로자가 비교대상근로자와 동일한 업무를 수행함에도 예산편성지침을 근거로 비교대상근로자 등 정규직원에 대해서만 근무실적평정을 통해 성과급을 지급하
- `id_405715` [discrimination]
  - 변경: notes
  - notes: 기간제근로자라는 이유로 성과급을 지급하지 않은 것은 합리적 이유가 없는 불리한 처우라고 판정한 사례 — discrimination 판단이 핵심
- `id_405721` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['misconduct', 'dismissal_validity']
  - notes: 근로자에게 근로계약 갱신기대권이 인정되나, 갱신거절에 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_405725` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약 기간이 종료된 이후에 구제신청을 제기하여 구제이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_405731` [dismissal_validity]
  - 변경: notes
  - notes: 고용승계기대권 인정할 수 없음 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
