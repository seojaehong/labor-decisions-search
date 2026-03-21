# contract_expiry_batch_057_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_057_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_36813` [dismissal_validity]
  - 변경: notes
  - notes: 해고의 효력을 다투던 중 근로계약기간의 만료로 근로관계가 종료되어 구제이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 
- `id_36819` [dismissal_validity]
  - 변경: notes
  - notes: 고용승계 의무가 없고, 고용승계 기대권도 인정되지 않으며, 당사자 간 근로계약을 체결한 사실이 없어 사용자는 구제신청의 당사자 적격이 없다고 판
- `id_36823` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 갱신기대권이 있음에도 사용자가 합리적인 이유 없이 근로계약 갱신을 거절한 것은 부당한 해고이며, 단일 노동조합이 있는 상태에서 교섭창
- `id_36843` [discrimination]
  - 변경: notes
  - notes: 기간제근로자들에게 비교대상근로자에 비해 정액급식비, 교통보조비, 특정업무수당, 법정선임수당을 지급하지 않거나 적게 지급한 것은 불합리한 차별이라
- `id_36845` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가？사실상？이미？기간의？정함이？없는？근로자이므로？사용자의？근로계약？만료？처분은？부당해고임을？인정한？사례 — 해고 사실 자체의 존부 또는 처

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
