# contract_expiry_batch_113_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_113_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_57053` [dismissal_validity]
  - 변경: notes
  - notes: 공사종료를 이유로 근로관계가 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_57067` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되나 갱신 거절의 합리적 이유가 있어 기간만료로 고용관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권 성립 여부
- `id_57069` [discrimination]
  - 변경: notes
  - notes: 기간제근로자들에게 비교대상근로자에 비하여 가족수당 등을 지급하지 않은 것은 차별적 처우에 해당한다고 판정한 사례 — discrimination 
- `id_57095` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 구제신청을 할 당시 이미 근로계약기간이 만료되어 근로자의 지위에 있지 아니하므로 구제신청의 이익이 없다고 판정한 사례 — 해고 사실 자체의 존부
- `id_57107` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로자1 ？ 해고가 존재하고 해고사유가 부당하다고 판정한 사례근로자2, 3 - 해고는 사유가 정당하지 않고 절차도 적법하지 않아 부당하다고 판정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
