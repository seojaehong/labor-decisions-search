# contract_expiry_batch_039_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_039_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_32685` [discrimination]
  - 변경: notes, conf:high→medium
  - notes: 계산원 업무만을 수행하는 기간제근로자와 동종 또는 유사한 업무를 전담하는 비교대상근로자가 존재하지 않는다고 판정한 사례 — discriminat
- `id_32691` [renewal_expectation]
  - 변경: notes
  - notes: 촉탁직 재고용의 갱신기대권이 인정되지 않아 해고로 볼 수 없고, 불이익 취급의 부당노동행위에도 해당하지 않는다고 판정한 사례 — 갱신기대권 성립
- `id_32693` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['training_opportunity', 'dismissal_validity']
  - notes: 기간제근로자로서 당사자 간 근로관계는 계약기간이 만료됨으로써 종료되었고, 근로자에게 근로계약의 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱
- `id_32697` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'renewal_expectation']
  - notes: 기각근로계약이 갱신된다는 신뢰관계가 형성되었다고 볼 수 없어 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_32701` [dismissal_validity]
  - 변경: notes
  - notes: 사용자에게 당사자 적격이 있으나, 근로계약기간이 만료되어 구제신청의 이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
