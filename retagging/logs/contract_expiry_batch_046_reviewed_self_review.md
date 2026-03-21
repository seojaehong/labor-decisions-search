# contract_expiry_batch_046_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_046_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_346709` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['attendance', 'procedure', 'disciplinary_severity']
  - notes: 해고절차는 적법하지만 해고사유 및 양정이 과도하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_346713` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되나, 갱신거절에 합리적인 이유가 있어 근로관계 종료가 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 
- `id_346721` [dismissal_validity]
  - 변경: notes
  - notes: 부당해고 구제신청 대한 사용자 적격은 사용자1에게 있고, 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁
- `id_346729` [worker_status]
  - 변경: notes
  - notes: 근로자는 기간제근로자로 입사하여 계속 근로기간이 총 2년을 초과하여 기간의 정함이 없는 근로계약을 체결한 근로자에 해당하므로 사용자가 근로계약기
- `id_346757` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들은 기간제근로자이고, 근로계약 갱신기대권이 인정되지 않으므로 해고가 존재하지 않으며, 근로관계 종료가 불이익 취급 또는 지배, 개입의 부

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
