# contract_expiry_batch_056_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_056_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_36297` [renewal_expectation]
  - 변경: notes
  - notes: 근로자1의 경우 정년 이후 촉탁직 재고용에 대한 기대권이 있다고 볼 수 없고, 근로자2의 경우 사용자의 근무지시로 구제신청의 목적이 달성되어 구
- `id_36317` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 갱신기대권이 있는 근로자들에게 합리적 이유 없이 갱신 거절한 것은 부당한 해고라고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵
- `id_3633` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'disciplinary_severity', 'dismissal_validity']
  - notes: 택시기사의 부당요금 징수에 대한 징계(승무정지 7일)는 부당하지 않고, 촉탁직 근로계약기간에 3회의 징계를 받은 근로자에 대해 촉탁직 근로계약 
- `id_36335` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간이 종료되어 부당해고 구제신청의 이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_36341` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되고, 정년을 이유로 근로관계 종료를 통보한 것은 갱신거절의 합리적 이유에 해당하지 않으며, 근로관계 종료

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
