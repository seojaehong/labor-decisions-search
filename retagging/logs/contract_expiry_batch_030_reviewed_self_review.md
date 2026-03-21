# contract_expiry_batch_030_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_030_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_28013` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 기간제 근로자로 근로계약의 갱신기대권이 인정되고, 갱신거절에 합리적 이유가 없어 사용자가 근로계약 갱신을 거절한 것은 부당해고라고 판정한 사례 
- `id_28021` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_28069` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간이 만료됨에 따라 구제이익이 소멸하였다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_28075` [discrimination]
  - 변경: notes
  - notes: 신청인(기간제근로자)이 지정한 비교대상근로자들은 2년을 초과하여 근로를 하지 않아 기간의 정함이 없는 근로자로 볼 수 없으므로 차별적 처우 여부
- `id_28077` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간이 만료됨에 따라 구제이익이 소멸하였다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
