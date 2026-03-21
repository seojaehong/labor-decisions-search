# contract_expiry_batch_048_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_048_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_347977` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['disciplinary_severity', 'dismissal_validity']
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되나 사용자의 갱신거절에 합리적 이유가 있어 당사자 간 근로관계는 기간만료로 종료되었다고 판정한 사례 — 
- `id_347981` [dismissal_validity]
  - 변경: notes
  - notes: 기간제 근로자로 2년을 초과하여 근무하였으므로 무기계약직 근로자로 전환되었고, 정당한 해고사유가 존재하지 않으며 절차적 하자도 존재하므로 해고처
- `id_347983` [dismissal_validity]
  - 변경: notes, secondary:['procedure', 'worker_status']→['procedure', 'worker_status', 'renewal_expectation']
  - notes: 기간의 정함이 없는 근로자를 계약기간 만료 사유로 해고한 것은 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_347991` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약 관계가 이미 종료된 후 구제신청이 제기되어 구제이익이 존재하지 아니한다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁
- `id_347995` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 갱신기대권이 인정되지 않으므로 사용자가 근로계약기간 만료로 근로관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
