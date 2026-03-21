# contract_expiry_batch_076_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_076_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_408449` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['absence_without_leave', 'dismissal_validity']
  - notes: 기간제근로자에게 갱신기대권이 인정되나, 사용자의 근로계약 갱신거절에 합리적인 이유가 존재하므로 근로계약 종료는 정당하다고 판정한 사례 — 갱신기
- `id_40847` [dismissal_validity]
  - 변경: notes
  - notes: 공종종료에 따라 근로자들의 근로계약기간이 종료되었고, 근로자들이 근무한 설비공정이 대부분 마무리되어 근로자들이 현장으로 복귀하여 근무하는 것도 
- `id_408483` [dismissal_validity]
  - 변경: notes
  - notes: 시용근로자이고, 본채용 거부의 합리적인 사유가 존재하지 않으며, 본채용 거부 통보에 절차적 하자가 있어 부당하다고 판정한 사례 — 해고 사실 자
- `id_40851` [renewal_expectation]
  - 변경: notes
  - notes: 정년이 도과한 근로자들과의 근로계약 갱신 거절은 합리적 사유가 있어 정당하고, 부당노동행위에도 해당하지 않는다고 판정한 사례 — 갱신기대권 성립
- `id_408541` [renewal_expectation]
  - 변경: notes
  - notes: 사용자 적격은 법인인 사용자2에 있고, 근로계약 갱신기대권은 인정되나, 갱신 거절의 합리적인 이유가 있으므로 계약기간 만료에 의한 근로관계 종료

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
