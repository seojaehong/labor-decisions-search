# contract_expiry_batch_021_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_021_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_22795` [dismissal_validity]
  - 변경: notes
  - notes: 초심유지(기각) — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_22797` [renewal_expectation]
  - 변경: notes
  - notes: 정년이 도래하여 퇴직하게 된 근로자를 촉탁직으로 재고용하지 않은 것은 부당해고 및 부당노동행위에 해당되지 않는다고 판정한 사례 — 갱신기대권 성
- `id_22821` [dismissal_validity]
  - 변경: notes
  - notes: 총 근로기간 2년이 초과한 근로자에게 근로계약기간 만료로 계약 종료를 통보한 것은 부당해고라고 판정한 사례 — 해고 사실 자체의 존부 또는 처분
- `id_22831` [dismissal_validity]
  - 변경: notes, secondary:['unfair_treatment']→['unfair_treatment', 'renewal_expectation']
  - notes: 입주자대표회의가 보안(경비)용역업체를 새로 선정하기로 의결하여 사용자가 보안대원들에게 근로계약 기간만료예고통지를 하자 근로자들이 계속 근로하기를
- `id_22833` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 인정되지 않아, 근로관계는 계약기간만료 종료되어 해고에 해당하지 않는다고 판정한 사례 — 갱신기대권 성립 여부

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
