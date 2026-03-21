# contract_expiry_batch_032_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_032_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_28977` [dismissal_validity]
  - 변경: notes
  - notes: 근로관계 종료가 해고에 해당되지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_28995` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자로서 근로계약의 갱신기대권이 인정되고, 갱신거절의 합리적 사유가 존재하지 않아 부당해고에 해당한다고 판정한 사례 — 갱신기대권 성립 
- `id_29005` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 정년을 이유로 근로관계를 종료한 것은 해고가 아니라고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_29011` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로계약을 체결한 근로자에게 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없어 근로관계는 계약기간 만료로 당연히 종료되었
- `id_29017` [renewal_expectation]
  - 변경: notes
  - notes: 근무평가의 공정성과 객관성이 결여되어 근로계약 갱신거절은 부당하다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
