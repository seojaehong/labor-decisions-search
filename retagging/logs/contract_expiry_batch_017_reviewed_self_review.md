# contract_expiry_batch_017_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_017_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_20665` [renewal_expectation]
  - 변경: notes
  - notes: 계약기간 만료로 고용관계가 종료된 것으로 해고가 존재하지 않아 부당해고 및 부당노동행위에 해당하지 않는다고 판정한 사례 — 갱신기대권 성립 여부
- `id_2069` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 정당하게 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 
- `id_20695` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'disciplinary_severity', 'dismissal_validity']
  - notes: 한시적 기간제 근로계약을 맺은 근로자에게 당연히 근로계약이 갱신될 것이라는 기대권이 형성되어 있다고 보기 어렵고, 정년도래근로자에 대하여 정년규
- `id_20713` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신기대권이 인정되지 않아 계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_20719` [dismissal_validity]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로자로 전환되었음에도 정당한 이유 없이 근로계약기간 만료를 이유로 근로관계를 종료한 것은 부당한 해고라고 판정한 사례 — 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
