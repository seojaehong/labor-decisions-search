# contract_expiry_batch_083_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_083_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_413515` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계가 계약기간 만료로 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_413529` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 정규직으로 전환될 것이라는 정당한 기대권이 인정되고 사용자의 정규직 전환 거절의 사유가 객관적이고 합리적이며 공정하다고 볼 수 없다고
- `id_413541` [renewal_expectation]
  - 변경: notes
  - notes: 근로자의 무기계약직 전환 기대권이 인정되고, 무기계약 전환거절의 합리적 사유가 없어 부당해고에 해당한다고 판정한 사례 — 갱신기대권 성립 여부 
- `id_413551` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['attendance', 'absence_without_leave', 'dismissal_validity']
  - notes: 근로자에게 갱신기대권이 인정되나, 갱신거절에 합리적 이유가 있다고 본 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_413579` [renewal_expectation]
  - 변경: notes
  - notes: 기간제 근로자에 대한 근로계약 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
