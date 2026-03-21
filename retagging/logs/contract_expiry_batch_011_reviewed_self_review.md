# contract_expiry_batch_011_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_011_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_16471` [renewal_expectation]
  - 변경: notes
  - notes: 정규직 근로자 전환 거절의 합리적인 이유가 없는 근로관계 종료는 부당하지만, 부당노동행위로 보기는 어렵다고 판정한 사례 — 갱신기대권 성립 여부
- `id_16481` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['training_opportunity', 'dismissal_validity']
  - notes: 근로계약의 갱신기대권은 인정되나, 중증장애인 등 교통약자의 이동을 지원하기 위한 차량을 운전하는 근로자가 1,000만원 이상의 교통사고를 발생시
- `id_16489` [dismissal_validity]
  - 변경: notes
  - notes: 일용근로자로 근로계약기간 만료에 따라 근로관계가 종료된 것이므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효
- `id_1649` [discrimination]
  - 변경: notes
  - notes: 복지포인트 미지급은 제척기간이 도과되었고, 비교대상근로자에 비하여 상여수당을 지급하지 않은 것은 합리적인 이유 없는 차별적 처우라고 판정한 사례
- `id_16493` [renewal_expectation]
  - 변경: notes
  - notes: 이 사건 근로계약은 갱신기대권이 있고 그 갱신거절의 합리적 사유가 없어 기간만료 통보는 부당해고이며, 부당노동행위에 대하여는 구체적인 증거가 없

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
