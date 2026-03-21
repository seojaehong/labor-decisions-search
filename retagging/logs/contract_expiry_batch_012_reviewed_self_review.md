# contract_expiry_batch_012_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_012_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_17049` [renewal_expectation]
  - 변경: notes
  - notes: 갱신거절의 합리적 이유가 있어 계약기간만료에 따른 근로관계 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_17069` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 유효하게 작성된 근로계약서에 따라 근로계약기간 만료를 통보한 것은 해고에 해당하지 않는다고 판정한 사례 — discrimination 판단이 핵
- `id_1709` [renewal_expectation]
  - 변경: notes
  - notes: 구제신청의 제척기간이 도과하여 각하한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_17099` [renewal_expectation]
  - 변경: notes
  - notes: 정년 이후 재계약에 대한 기대권은 인정되나, 재계약 거절에 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_17101` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정된다고 볼 수 없어 근로계약기간의 만료로 고용관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
