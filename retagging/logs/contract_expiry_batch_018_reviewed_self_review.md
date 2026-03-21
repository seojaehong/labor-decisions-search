# contract_expiry_batch_018_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_018_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_2121` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계가 근로계약 만료로 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_21219` [discrimination]
  - 변경: notes, secondary:['procedure', 'worker_status', 'dismissal_validity']→['attendance', 'absence_without_leave', 'procedure', 'worker_status']
  - notes: 근로자는 2년을 초과하여 근무하였으므로 무기계약근로자에 해당하고, 무단 휴가 사용, 청소업무 소홀, 안전모 미착용, 근무태도 불량 등을 사유로 
- `id_21225` [discrimination]
  - 변경: notes
  - notes: 제척기간을 도과하였고, 고용관계를 인정받지 못하여 가족수당 등을 지급받지 못한 것은 차별적 처우에 해당하지 않는다고 판정한 사례 — discri
- `id_21245` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'worker_status', 'dismissal_validity']→['procedure', 'training_opportunity', 'worker_status', 'dismissal_validity']
  - notes: 기간제근로자로 계속 근로한 기간이 2년을 초과하지 않았고, 갱신기대권도 인정되지 않아 계약기간 만료에 따른 근로관계 종료로 판정한 사례 — 갱신
- `id_21255` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들의 근로조건 결정은 용역업체에 귀속되어 있고 근로자들은 고용승계에 대한 기대권이 형성되었다고 보기 어려우므로 위탁주체 및 새로운 용역업체

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
