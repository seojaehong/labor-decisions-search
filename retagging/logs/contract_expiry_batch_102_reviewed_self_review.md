# contract_expiry_batch_102_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_102_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_51203` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없어 근로계약관계는 계약기간 만료로 당연히 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및
- `id_51217` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로자의 근로계약기간은 1년에 해당하고, 근로계약기간이 남아 있음에도 근로계약기간 만료를 이유로 근로관계를 종료한 것은 해고에 해당하며, 해고사
- `id_51225` [dismissal_validity]
  - 변경: notes
  - notes: 사용자가 근로자의 의사에 반하여 일방적으로 근로관계를 종료시켰다고 보기 어려워 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 
- `id_5125` [dismissal_validity]
  - 변경: notes
  - notes: 계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_51253` [renewal_expectation]
  - 변경: notes
  - notes: 근로자에게 근로계약의 갱신기대권이 존재한다고 볼 수 없어 계약기간 만료에 따른 근로계약 종료는 정당하다고 판정한 사례 — 갱신기대권 성립 여부 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
