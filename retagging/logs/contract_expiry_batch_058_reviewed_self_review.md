# contract_expiry_batch_058_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_058_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_37261` [dismissal_validity]
  - 변경: notes
  - notes: 소정근로시간이 주 15시간 미만인 기간제근로자는 사용기간 제한의 예외사유에 해당하므로 계속근로기간이 2년을 초과하였더라도 사용자가 근로계약기간 
- `id_37265` [renewal_expectation]
  - 변경: notes
  - notes: 해고의 효력을 다투던 중 근로계약기간의 만료로 근로관계가 종료되어 구제이익이 없다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 
- `id_3727` [dismissal_validity]
  - 변경: notes
  - notes: 근로자 불법파견에 해당하여 직접고용의무를 이행하면서 기간의 정함이 있는 근로계약을 체결해야 할 특별한 사정이 존재하지 않아 계약기간 만료를 이유
- `id_37273` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['attendance', 'dismissal_validity']
  - notes: 총 근로기간이 1년에 불과하더라도 취업규칙 및 계약기간 설정의 동기, 갱신 관행 등을 보았을 때 갱신기대권이 있다고 판정한 사례 — 갱신기대권 
- `id_37289` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되지 않아 근로관계 종료통보는 부당해고에 해당하지 않으며, 갱신기대권이 인정되지 않는 계약해지는 계약만료일 뿐 노조의 와해나 활

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
