# contract_expiry_batch_095_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_095_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_47667` [renewal_expectation]
  - 변경: notes, secondary:['worker_status', 'dismissal_validity']→['misconduct', 'worker_status', 'dismissal_validity']
  - notes: 근로자에게 구제신청의 이익이 있고, 근로자는 기간제근로자로서 근로계약 갱신기대권이 인정되나 사용자의 갱신거절에 합리적 이유가 있으므로 사용자가 
- `id_47679` [dismissal_validity]
  - 변경: notes
  - notes: 구제신청은 제척기간을 도과하지 아니하였고, 근로자가 사직서를 제출하고 사용자가 이를 수리함으로써 당사자 간의 근로관계는 합의에 의해 종료되었다고
- `id_47685` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['misconduct', 'procedure', 'disciplinary_severity'], conf:high→medium
  - notes: 근로자의 행위가 모두 징계사유로 인정되며, 그 비위행위 정도에 비해 징계양정이 과하다고 보기 어려우므로 징계가 정당하다고 판정한 사례 — 해고 
- `id_47689` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로계약을 체결한 근로자로서 근로계약 갱신에 대한 기대권이 인정되지 아니하여 계약기간 만료에 따라 근로관계가 정당하게 종료되
- `id_47693` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['absence_without_leave', 'procedure', 'dismissal_validity']
  - notes: 근로자는 시용근로자에 해당하고, 근로자에 대해 근무성적평가를 통해 본채용을 거부한 것은 정당하다고 판정한 사례 — worker_status 판단

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
