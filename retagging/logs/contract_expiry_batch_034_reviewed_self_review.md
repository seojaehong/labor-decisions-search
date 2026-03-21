# contract_expiry_batch_034_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_034_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_29715` [renewal_expectation]
  - 변경: notes
  - notes: 공동주택관리업자에게 사용자 적격이 있고, 근로자에게 근로계약에 대한 갱신기대권이 있음에도 합리적 이유 없이 갱신을 거절한 것은 부당하다고 판정한
- `id_29729` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'disciplinary_severity', 'renewal_expectation']
  - notes: 근로자가 직무 관련자로부터 향응을 받는 등 징계사유가 존재하고 징계 규칙에 따라 징계양정이 적정하고 징계절차에 하자가 없다고 판정한 사례 — 해
- `id_29733` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 있음에도 불구하고 사용자가 객관적·합리적이지 않은 근무성적평정 점수를 근거로 근로계약의 갱신을 거부한 것은 부
- `id_29765` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없어 근로관계는 계약기간 만료로 당연히 종료되었다고 판정한 사례 — 갱신기대권 성립 
- `id_29801` [dismissal_validity]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 근로계약기간이 만료되어 구체신청의 이익이 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
