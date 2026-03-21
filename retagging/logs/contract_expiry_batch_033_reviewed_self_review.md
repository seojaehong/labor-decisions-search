# contract_expiry_batch_033_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_033_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_29361` [renewal_expectation]
  - 변경: notes
  - notes: 한시적 사업에 채용되어 `기간제근로자 사용기한 제한의 예외`에 해당하므로 무기계약직으로 전환되었다고 볼 수 없고, 근로계약의 갱신기대권이 없어 
- `id_29363` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 계약갱신의 요건, 기준 및 절차에 관한 규정이 없고 계약갱신의 관행도 존재하지 않아 근로계약의 갱신기대권을 인정하기 어렵다고 판정한 사례 — 갱
- `id_2937` [dismissal_validity]
  - 변경: notes
  - notes: 각하근로계약기간이 종료되었을 뿐 아니라 사용자의 복직명령으로 구제신청 목적이 달성되어 구제이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 
- `id_29373` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 공사가 종료되어 구제신청의 이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_29377` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자로서 정규직 전환에 대한 기대권이 인정되나, 정규직 전환 거절에 합리적인 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
