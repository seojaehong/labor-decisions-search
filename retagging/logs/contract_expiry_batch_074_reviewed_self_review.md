# contract_expiry_batch_074_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_074_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_406959` [dismissal_validity]
  - 변경: notes
  - notes: 구제신청을 할 당시 이미 근로계약 기간이 만료되어 구제이익이 소멸하였다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_406965` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'training_opportunity', 'disciplinary_severity'], conf:high→medium
  - notes: 징계사유가 일부 인정되고 징계절차는 적법하나 양정이 과하므로 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_40699` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'worker_status', 'dismissal_validity']→['procedure', 'training_opportunity', 'worker_status', 'dismissal_validity']
  - notes: 기간제근로자로서 근로계약 갱신에 대한 정당한 기대권이 있음에도 사용자가 합리적인 이유 없이 근로계약 갱신을 거절한 것은 부당하다고 판정한 사례 
- `id_406991` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['disciplinary_severity', 'dismissal_validity']
  - notes: 근로계약 갱신기대권은 인정되나 갱신 거절의 합리적 이유가 있어 근로관계 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리
- `id_407` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 기간제근로자로 정규직 전환기대권과 근로계약의 전환기대권과 갱신기대권이 인정되고, 전환거절에는 합리적 이유가 있으나, 갱신거절에는 합리적 이유가 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
