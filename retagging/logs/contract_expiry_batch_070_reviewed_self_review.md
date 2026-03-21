# contract_expiry_batch_070_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_070_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_404679` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['attendance', 'dismissal_validity']
  - notes: 근로계약에 대한 정당한 갱신기대권이 있는 근로자에 대하여, 갱신을 거절할만한 합리적인 이유가 없음에도 불구하고 거절한 것은 부당해고라고 판단한 
- `id_404681` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'training_opportunity']
  - notes: 채용형 인턴은 시용 근로관계에 해당하고, 본 채용을 거부하면서 서면으로 통지한 사실이 없어 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또
- `id_404685` [renewal_expectation]
  - 변경: notes
  - notes: 고용승계 기대권이 인정되며 고용승계 거절에 합리적인 이유가 있다고 보아 기각 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_404691` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로계약의 갱신기대권이 인정되지 않으므로 근로계약기간 만료에 따른 근로계약 종료는 정당하다고 판정한 사례 — discrimination 판단이 
- `id_40471` [renewal_expectation]
  - 변경: notes
  - notes: 계약직 근로자로서 근로계약의 갱신기대권이 인정되고 갱신거절에 대한 합리적 이유 없이 기간 만료로 근로계약을 해지한 것은 부당해고에 해당하지만, 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
