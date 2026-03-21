# contract_expiry_batch_094_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_094_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_47151` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권은 인정되나 갱신거절의 합리적인 이유가 있어 근로관계는 계약기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 
- `id_4717` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['procedure', 'dismissal_validity']
  - notes: 정규직 전환기대권은 인정되나 정규직 전환거절에 합리적인 이유가 있어 계약기간 만료에 따른 근로관계 종료는 부당해고가 아니라고 판정한 사례 — 갱
- `id_47173` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않고 계약기간 만료에 따라 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵
- `id_47205` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되지 않으므로 근로계약관계는 계약기간 만료로 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_47225` [discrimination]
  - 변경: notes
  - notes: 동일？유사 업무를 수행하고 있음에도 기간제근로자임을 이유로 비교대상근로자와 달리 자격수당, 가족수당, 자체평가급 및 인센티브평가급, 근무장려수당

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
