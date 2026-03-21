# contract_expiry_batch_063_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_063_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_400001` [renewal_expectation]
  - 변경: notes
  - notes: 사용자1이 사용자2와 고용을 승계하기로 하는 계약을 체결하거나 합의한 사실은 없으므로 사용자2에게 사용자 적격이 있고 고용승계 기대권이 인정되지
- `id_40003` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_400035` [dismissal_validity]
  - 변경: notes
  - notes: 용역계약서, 관행 등에서 고용승계에 대한 기대권을 인정할 만한 내용이 확인되지 아니하여 기각으로 판정한 사례 — 해고 사실 자체의 존부 또는 처
- `id_400081` [renewal_expectation]
  - 변경: notes
  - notes: 정년 후 촉탁직 재고용 기대권은 존재하나, 정년 후 촉탁직 재고용 거절의 합리적 이유가 있으므로 부당해고에 해당하지 않는다고 판정한 사례 — 갱
- `id_400083` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'renewal_expectation']
  - notes: 비상대비업무담당자의 임기는 법률의 정당한 위임에 따라 임용기관의 정년까지로 규정되어 있고 사용자의 기본정년이 '만 60세’임에도 사용자가 그에 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
