# contract_expiry_batch_015_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_015_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_19137` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자로 새로이 계약된 근로자에 대해 갱신거절의 합리적인 사유가 존재하며 이를 부당노동행위로도 볼 수 없다고 판정한 사례 — 갱신기대권 성
- `id_19151` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되는 기간제근로자에게 합리적 이유 없이 근로계약 갱신을 거절한 것은 부당해고에 해당한다고 판정한 사례 — 갱신기대권 성립 여부 
- `id_19181` [dismissal_validity]
  - 변경: notes, secondary:[]→['training_opportunity']
  - notes: 기간의 단절 없이 법령에서 정한 사용제한기간 4년을 초과하여 근무하여 기간의 정함이 없는 근로자로 전환되었으므로 계약기간 만료를 이유로 근로관계
- `id_19209` [dismissal_validity]
  - 변경: notes, secondary:['procedure', 'worker_status']→['attendance', 'procedure', 'worker_status']
  - notes: 근로자는 2년을 초과하여 근무하였으므로 무기계약근로자에 해당하고, 무단 휴가 사용, 청소업무 소홀, 안전모 미착용, 근무태도 불량 등을 사유로 
- `id_19219` [dismissal_validity]
  - 변경: notes, secondary:[]→['training_opportunity'], conf:high→medium
  - notes: 당사자 적격이 있는 실질적인 사용자를 피신청인으로 추가한 시점에 이미 무기계약 전환 거부가 있었던 날부터 3개월을 경과하여 제척기간이 도과되었다

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
