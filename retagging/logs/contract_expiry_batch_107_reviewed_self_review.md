# contract_expiry_batch_107_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_107_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_54119` [renewal_expectation]
  - 변경: notes
  - notes: 근로자의 근로계약 갱신기대권이 인정되나 근로계약 갱신 거절에 합리적인 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 
- `id_54135` [discrimination]
  - 변경: notes, secondary:['worker_status', 'dismissal_validity', 'renewal_expectation']→['worker_status', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자는 기간제법상 사용기간 제한의 예외에 해당하여 기간제 근로자이고 근로계약의 갱신기대권이 인정되며 갱신 거절에 합리적 이유가 없으므로 근로관
- `id_54139` [worker_status]
  - 변경: notes, conf:high→medium
  - notes: 근로자는 시용근로자이며 본채용 거절의 정당성이 인정되고 절차상 하자가 없다고 판정한 사례 — worker_status 판단이 핵심
- `id_54145` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권을 인정할 수 있음에도 합리적 이유 없이 갱신을 거절해 근로관계를 종료한 것은 부당해고에 해당한다고 판정한 사례 — 갱신기대
- `id_54147` [renewal_expectation]
  - 변경: notes
  - notes: 업무위탁 관계에 있는 자는 근로기준법 및 노조법상 사용자로 볼 수 없고, 촉탁직 고용에 대한 기대권이 인정되지 않으며, 정년퇴직 통보는 정당하고

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
