# contract_expiry_batch_088_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_088_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_44151` [discrimination]
  - 변경: notes
  - notes: 사용자2는 당사자능력이 없으므로 당사자 적격은 사용자1에게 있고, 근로자는 기간제근로자로서 정규직 전환 기대권이 있음에도 객관성？공정성이 결여된
- `id_44201` [renewal_expectation]
  - 변경: notes
  - notes: 근로자의 갱신기대권은 인정되나 갱신거절의 합리적인 이유가 있어 근로관계가 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절
- `id_44203` [renewal_expectation]
  - 변경: notes
  - notes: 징계 이력이 없는 자들에 대한 촉탁직 재계약 관행이 있어 근로자에게 촉탁직 재계약 기대권이 존재하나, 근로자의 징계 이력을 살펴볼 때 재계약 거
- `id_44217` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity'], conf:high→medium
  - notes: 근로자들에게 근로계약의 갱신기대권이 인정되고 사용자의 갱신거절에 합리적 이유가 없으므로 계약기간 만료를 이유로 한 근로관계 종료는 부당해고라고 
- `id_44219` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 갱신기대권이 인정되고 갱신 거절에 합리적인 이유가 없어 부당해고로 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
