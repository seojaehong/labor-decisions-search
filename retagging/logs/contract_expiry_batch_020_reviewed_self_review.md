# contract_expiry_batch_020_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_020_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_22209` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 기간의 정함이 있는 근로계약을 체결하여 계약기간이 만료됨에 따라 근로관계가 종료되었고 부당노동행위에도 해당되지 않는다고 판정한 사례 — 갱신기대
- `id_22217` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'renewal_expectation']
  - notes: 기간의 정함이 없는 근로자로 전환되었으므로 계약기간 만료를 이유로 근로계약을 종료한 것은 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는
- `id_22241` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되는 근로자에게 합리적인 이유 없이 공개채용을 근거하여 근로계약의 갱신을 거절한 것은 부당하다고 판정한 사례 — 갱신기대권 성립
- `id_22243` [dismissal_validity]
  - 변경: notes
  - notes: 계약기간 만료를 사유로 기간의 정함이 없는 근로계약을 체결한 근로자와의 고용관계를 종료한 것은 부당한 해고에 해당한다고 판정한 사례 — 해고 사
- `id_22259` [renewal_expectation]
  - 변경: notes
  - notes: 재임용의 기대권이 인정되고 재임용 거부의 합리적 사유도 없으므로 임용기간 만료를 사유로 행한 면직처분은 부당하다고 판정한 사례 — 갱신기대권 성

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
