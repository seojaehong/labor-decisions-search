# contract_expiry_batch_031_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_031_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_28465` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되지 않아 계약기간 만료로 인한 근로관계 종료라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_28471` [dismissal_validity]
  - 변경: notes, secondary:[]→['misconduct', 'renewal_expectation']
  - notes: 해고사유가 당사자 간 신뢰를 현저히 저하하여 근로관계를 더 이상 지속시킬 수 없을 정도의 사유라고는 보기 어려워 해고는 부당하다고 판정한 사례 
- `id_28475` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로계약기간이 종료됨에 따라 구제이익이 소멸하였다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_28493` [dismissal_validity]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 근로자들이 제출한 사직서를 비진의 의사표시로 볼만한 사정이 없고, 사용자의 일방적 의사에 의한 근로관계 종료로 보기 어렵다고 판정한 사례 — 해
- `id_28495` [renewal_expectation]
  - 변경: notes
  - notes: 계약기간이 만료됨에 따라 근로관계가 종료되었고 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
