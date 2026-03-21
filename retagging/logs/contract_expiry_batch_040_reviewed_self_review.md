# contract_expiry_batch_040_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_040_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_3337` [renewal_expectation]
  - 변경: notes
  - notes: 근로자의 갱신기대권이 인정되지 않아 계약기간 만료로 고용관계를 종료한 것은 정당하고, 부당노동행위에 해당하지 않는다고 판정한 사례 — 갱신기대권
- `id_33375` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 평가자의 주관에 따른 근무성적평정 미달을 이유로 행한 재임용 거부 처분은 갱신거절에 합리적 이유가 없다고 판단한 사례 — discriminati
- `id_33399` [renewal_expectation]
  - 변경: notes
  - notes: 계약기간 만료로 근로관계가 종료되었고, 정규직 전환 또는 근로계약 갱신에 대한 기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 
- `id_33405` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계는 계약기간 만료로 자동 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_33419` [discrimination]
  - 변경: notes, conf:medium→high
  - notes: 기본연봉은 차별적 처우에 합리가 이유가 있으나, 성과급(일부)은 차별적 처우에 합리적 사유가 없다고 판정한 사례 — discrimination 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
