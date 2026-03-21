# contract_expiry_batch_023_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_023_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_23941` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['misconduct', 'procedure', 'dismissal_validity']
  - notes: 근로자에게 근로계약 종료 시 정규직 전환에 대한 정당한 기대권이 인정되지 않으므로 근로관계는 계약기간 만료로 종료되었다고 판정한 사례 — 갱신기
- `id_23943` [dismissal_validity]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 인사권을 남용한 대기발령 처분은 구제이익이 있어 부당한 인사처분이라고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_2395` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자의 근로계약 갱신기대권이 인정됨에도 합리적 이유 없이 계약기간 만료로 근로관계를 종료한 것은 부당해고라고 판정한 사례 — 갱신기대권 
- `id_23983` [renewal_expectation]
  - 변경: notes
  - notes: 계약갱신에 관한 요건과 절차 규정 없이 인력수요 및 근로자의 근무태도에 따라 재량적으로 계약 갱신 여부를 결정하여 온 사실을 알 수 있으므로 근
- `id_24003` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
