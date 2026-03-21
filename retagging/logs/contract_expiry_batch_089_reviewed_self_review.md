# contract_expiry_batch_089_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_089_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_44729` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['absence_without_leave', 'procedure', 'dismissal_validity']
  - notes: 고용승계 기대권이 있는 근로자에 대해 합리적 이유 없이 고용승계를 거부한 것은 부당해고에 해당한다고 판정한 사례 — discrimination 
- `id_44733` [renewal_expectation]
  - 변경: notes
  - notes: 근로자들은 기간제근로자이고, 갱신기대권이 인정되지 않아 기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리
- `id_44735` [renewal_expectation]
  - 변경: notes
  - notes: 기간제 근로계약을 체결하였고, 근로관계는 계약기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_44761` [renewal_expectation]
  - 변경: notes
  - notes: 근로관계는 계약기간 만료로 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_44763` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 사직원을 제출하고 사용자가 이를 수리함으로써 근로관계를 종료한 것으로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
