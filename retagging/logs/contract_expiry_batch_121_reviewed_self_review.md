# contract_expiry_batch_121_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_121_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_6875` [discrimination]
  - 변경: notes, secondary:['unfair_treatment', 'dismissal_validity', 'renewal_expectation']→['unfair_treatment', 'renewal_expectation', 'dismissal_validity'], conf:high→medium
  - notes: 근로계약의 갱신기대권이 인정되고 갱신거절의 합리적 이유가 없어 부당해고에 해당하나, 부당노동행위에는 해당하지 않는다고 판정한 사례 — discr
- `id_6889` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 기간의 정함이 없는 근로계약을 체결한 근로자에 해당하지 않아, 근로계약기간이 만료되어 근로관계가 종료된 경우 해고로 볼 수 없다고 판정
- `id_6891` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 기간의 정함이 없는 근로자로 전환되었음에도 사용자가 근로관계를 종료한 것은 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분
- `id_6899` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['procedure', 'dismissal_validity']
  - notes: 정규직 전환 기대권이 인정되나 정규직 전환 거절의 합리적 이유가 있으므로 정규직 전환을 거부하고 계약기간 만료에 따라 근로계약을 종료한 것은 정
- `id_6901` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없어 근로관계는 계약기간 만료로 당연히 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
