# contract_expiry_batch_075_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_075_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_407733` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신 기대권이 인정되지 않아 근로계약 기간만료를 사유로 근로관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신
- `id_407741` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['work_ability', 'procedure', 'dismissal_validity']
  - notes: 근로계약의 갱신기대권이 인정되나, 갱신거절에 합리적인 이유가 있어 근로관계 종료가 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 
- `id_407747` [dismissal_validity]
  - 변경: notes, secondary:[]→['attendance']
  - notes: 근로관계가 매일의 근로계약에 따라 시작되고 종료되는 일용근로자로서 근로관계는 해고로 종료되었다고 볼 수 없다고 판정한 사례 — 해고 사실 자체의
- `id_40777` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 건설일용근로자로서 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_407789` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 일용근로자이므로 해고가 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
