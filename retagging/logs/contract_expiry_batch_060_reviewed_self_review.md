# contract_expiry_batch_060_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_060_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_38169` [discrimination]
  - 변경: notes
  - notes: 대체직 기간제근로자라는 이유로 비교대상근로자에 비해 근속수당을 지급하지 않고 맞춤형복지비를 배정하지 않은 것은 합리적인 이유 없는 차별이라고 판
- `id_38175` [dismissal_validity]
  - 변경: notes
  - notes: 사용자의 정규직 전환 관행으로 인해 근로자의 정규직 전환기대권은 인정되나 근로자의 평가점수가 낮아 정규직 전환을 거절한 것은 정규직 전환거절의 
- `id_38179` [discrimination]
  - 변경: notes, secondary:['unfair_treatment', 'dismissal_validity', 'renewal_expectation']→['unfair_treatment', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자에게 근로계약의 갱신기대권이 존재하고 사용자가 합리적인 이유 없이 근로계약의 갱신을 거절한 것은 부당하지만, 불이익 취급의 부당노동행위에는
- `id_38189` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약에 대한 갱신기대권은 인정되나 근로계약의 갱신을 거절할 만한 합리적 이유가 존재하므로, 사용자가 계약기간 만료에 따라 행한 근로관계의 종
- `id_38205` [dismissal_validity]
  - 변경: notes
  - notes: 근로자들이 무기계약 근로자로 전환이 되었으므로 근로계약기간 만료로 근로계약을 종료한 것은 정당한 이유없는 부당해고에 해당한다고 판정한 사례 — 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
