# contract_expiry_batch_115_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_115_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_5839` [discrimination]
  - 변경: notes
  - notes: 근로자들에게 정규직 전환 기대권이 있음에도 합리적 이유 없이 정규직 전환을 거절한 것은 부당해고지만, 불이익 취급 및 지배·개입의 부당노동행위는
- `id_58407` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_58409` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자들에게 갱신기대권이 인정되지 않아 근로관계는 계약기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성
- `id_5841` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자1은 근로계약이 갱신되리라는 신뢰관계가 형성되어 갱신기대권이 인정되며 근로계약 갱신거절에 합리적 이유가 없으므로 부당해고에 해당하고, 근로
- `id_58411` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계가 사용자에게 승계된 사실이 없고, 근로자에게 고용승계 기대권이 있다고 볼 수도 없으므로 사용자가 부당해고 구제신청의 당사자 적격이 없다

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
