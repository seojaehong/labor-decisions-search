# contract_expiry_batch_047_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_047_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_347381` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 만료로 근로관계가 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_347385` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않아 근로계약 기간만료에 따른 근로계약 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리
- `id_347395` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'disciplinary_severity', 'dismissal_validity']
  - notes: 해고가 존재하지 않고, 근로계약 갱신기대권이 인정되지 않으므로 근로관계 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리
- `id_347409` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['work_ability', 'procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자들에게 갱신기대권이 인정되나, 갱신거절에 합리적 이유가 있다고 본 사례 — discrimination 판단이 핵심
- `id_347421` [renewal_expectation]
  - 변경: notes
  - notes: 고용승계 기대권이 인정되지 않고, 계약기간 만료에 따라 근로관계가 종료된 것이므로 부당해고가 아니라고 판정한 사례 — 갱신기대권 성립 여부 및 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
