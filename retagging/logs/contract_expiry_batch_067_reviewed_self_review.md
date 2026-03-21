# contract_expiry_batch_067_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_067_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_403063` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['attendance', 'misconduct', 'dismissal_validity']
  - notes: 갱신기대권이 인정되나, 갱신 거절의 합리적 사유가 있다고 판단한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_403081` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 만료에 따라 근로관계가 종료되어 해고가 존재하지 않으므로 기각 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_403111` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 군 입영을 앞둔 상황에서 근로자가 제출한 퇴직원이 비진의 의사표시로써 무효라고 볼 수 없고, 사용자가 퇴직원을 수리하여 근로관계를 종료한 것은 
- `id_403123` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권은 인정되나, 갱신 거절에 합리적인 이유가 있으므로 근로관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권 
- `id_403141` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들에게 고용승계 기대권이 인정되고, 고용승계 거절에 합리적인 이유가 있다고 보기 어려워 부당한 해고라고 판정한 사례 — 갱신기대권 성립 여

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
