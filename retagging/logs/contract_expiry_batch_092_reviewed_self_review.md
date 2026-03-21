# contract_expiry_batch_092_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_092_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_46255` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약이 갱신되지 않았고, 근로계약 갱신기대권이 존재하지 않아 근로계약 만료로 고용관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권 성
- `id_46263` [discrimination]
  - 변경: notes, secondary:['worker_status']→['attendance', 'worker_status']
  - notes: 용역업무 위탁계약을 체결하고 출퇴근 의무없이 자택에서 근무하며 전화 수신 건당에 따라 수수료를 지급받은 재택 용역 에이전트(Agent)들은 근로
- `id_46271` [renewal_expectation]
  - 변경: notes
  - notes: 정규직 전환기대권은 인정되나, 평가결과를 근거로 근로관계를 종료한 것에 합리적인 이유가 있다고 판단한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_46277` [renewal_expectation]
  - 변경: notes
  - notes: 근로관계는 계약기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_46281` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자는 기간제법에서 정한 사용기간 제한의 예외에 해당하는 기간제근로자에 해당하고, 근로계약 갱신기대권이 인정되지 않아 사용자가 근로계약기간 만

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
