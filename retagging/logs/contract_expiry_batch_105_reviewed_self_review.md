# contract_expiry_batch_105_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_105_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_53087` [renewal_expectation]
  - 변경: notes, secondary:['worker_status', 'dismissal_validity']→['worker_status', 'disciplinary_severity', 'dismissal_validity']
  - notes: 정직 1월은 인정되는 징계사유에 비하여 양정이 과다하여 부당하고, 근로자가 기간제근로자에 해당하고 갱신기대권이 인정되나 갱신 거절의 합리적 이유
- `id_53099` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 갱신기대권이 인정되고, 갱신거절의 합리적인 이유가 없으므로 당사자 간 근로관계 종료는 부당해고에 해당하나, 부당노동행위에는 해당하지 
- `id_53117` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로자들은 일용 근로자에 해당하고, 설령 근로자들이 기간제근로자에 해당한다고 하더라도 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의
- `id_53157` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자에게 촉탁직 갱신기대권이 인정되나 사용자의 근로계약 갱신거절에 합리적 이유가 있다고 본 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이
- `id_53161` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않아 근로자와 사용자 사이의 근로계약 관계가 계약기간 만료로 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
