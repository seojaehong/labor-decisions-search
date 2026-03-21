# contract_expiry_batch_038_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_038_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_32161` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권은 인정되나, 갱신거절의 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_32167` [dismissal_validity]
  - 변경: notes
  - notes: 구제이익이 있으나, 해고 사실이 객관적으로 입증되지 않아, 해고가 존재하지 않는 것으로 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성
- `id_32173` [renewal_expectation]
  - 변경: notes
  - notes: 사용자2(입주자대표회의)는 당사자 적격이 없고, 사용자1(주택관리회사)이 당사자 적격이 있으며, 근로관계가 계약기간의 만료로 정당하게 종료되었다
- `id_32185` [dismissal_validity]
  - 변경: notes
  - notes: 부당해고 구제신청을 하여 해고의 효력을 다투던 중 근로계약기간이 만료되어 구제이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유
- `id_32203` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 갱신기대권이 존재하나 근무성적평가 결과 기준 점수에 미달하여 재임용을 거부한 것은 갱신거절에 합리적인 이유가 있다고 판정한 사례 — worker

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
