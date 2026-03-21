# contract_expiry_batch_120_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_120_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_6317` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['attendance', 'procedure', 'dismissal_validity']
  - notes: 기간제근로자로서 근로계약의 갱신기대권은 인정되나, 갱신거절의 합리적인 이유가 존재하므로 계약만료 통보는 정당하다고 판정한 사례 — 갱신기대권 성
- `id_6323` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 비자 연장을 하지 않아 자동적으로 근로관계가 소멸되어 해고는 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성
- `id_6325` [renewal_expectation]
  - 변경: notes
  - notes: 근로자의 구제신청이 기존의 구제신청과 심판대상이 달라 구제이익이 있으나, 계약기간 만료에도 불구하고 계약이 갱신된다는 신뢰관계가 형성되지 않아 
- `id_6331` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['misconduct', 'procedure', 'disciplinary_severity', 'renewal_expectation'], conf:high→medium
  - notes: 징계사유 일부가 인정되고, 인정되는 징계사유에 비해 징계양정이 과하지 않으며 징계절차에도 하자가 없어 해고가 정당하다고 판정한 사례 — 해고 사
- `id_6333` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약 만료에 따라 근로관계가 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
