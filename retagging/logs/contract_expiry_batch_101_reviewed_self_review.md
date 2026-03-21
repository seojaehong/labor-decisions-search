# contract_expiry_batch_101_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_101_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_50623` [dismissal_validity]
  - 변경: notes
  - notes: 사용자와 근로자 간 근로관계는 시용근로관계에 해당하나 해고의 서면통지 의무를 위반하여 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처
- `id_50633` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로자4, 6의 경우, 제척기간이 도과되었으며, 나머지 근로자들의 근로관계는 근로계약기간 만료(공사종료)로 인해 종료되어 해고가 존재하지 않는다
- `id_50635` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약 갱신기대권이 인정되지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_50647` [dismissal_validity]
  - 변경: notes
  - notes: 근로자의 사용자1에 대한 고용승계 기대권이 성립하나 사용자1이 근로자의 고용승계를 거부한 데에 합리적 이유가 있고, 사용자2는 근로자를 해고하면
- `id_50659` [renewal_expectation]
  - 변경: notes
  - notes: 기간제 근로계약을 체결하고 근로계약이 종료된 근로자에게 정규직 전환기대권이 인정되나, 사용자의 정규직 전환 거절에 합리적인 사유가 인정된다고 판

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
