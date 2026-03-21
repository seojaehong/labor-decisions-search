# contract_expiry_batch_059_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_059_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_37795` [renewal_expectation]
  - 변경: notes
  - notes: 사용사업주가 아닌 파견사업주에 사용자 적격이 있고, 당사자 간 근로관계는 계약기간이 만료됨으로써 종료되었으며 근로자에게 근로계약의 갱신기대권이 
- `id_37807` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 부당휴직에 대한 구제를 신청하여 다투던 중 정년으로 사용자와 근로관계가 종료되어 더 이상 구제절차를 진행할 이익이 없다고 판정한 사례 
- `id_37811` [renewal_expectation]
  - 변경: notes
  - notes: 갱신거절에 대한 합리적 이유 없이 계약기간 만료로 근로계약을 해지한 것은 부당하지만, 불이익취급의 부당노동행위는 불인정한 사례 — 갱신기대권 성
- `id_37817` [dismissal_validity]
  - 변경: notes
  - notes: 근로자와 사용자 사이의 근로계약은 이미 갱신되었음에도 사용자가 근로자에게 행한 근로계약만료 통보는 해고에 해당하고 해고사유도 없고 해고절차도 위
- `id_37823` [renewal_expectation]
  - 변경: notes
  - notes: 근로자의 촉탁직 재고용 기대권이 인정되고 재고용 거절에 합리적인 이유가 없으므로 부당해고에 해당하며, 부당노동행위로 보기는 어렵다고 판정한 사례

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
