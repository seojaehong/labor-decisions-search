# contract_expiry_batch_110_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_110_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_55631` [dismissal_validity]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로자로 간주되었음에도 사용자가 계약기간 만료를 이유로 근로관계를 종료한 것은 정당한 해고사유에 해당하지 않고, 해고사유와 
- `id_55637` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권은 인정되나 갱신거절의 합리적인 이유가 있어 근로관계는 계약기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신
- `id_55649` [renewal_expectation]
  - 변경: notes
  - notes: 촉탁직 재고용기대권이 인정되지 않아 사용자가 촉탁직근로자로 재고용하지 않은 것은 정당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합
- `id_55651` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 사용자의 일방적 의사표시에 의해 근로관계가 종료되었다고 보기 어려우므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처
- `id_55653` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로자들은 일용 근로자에 해당하고, 설령 근로자들이 기간제근로자에 해당한다고 하더라도 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
