# contract_expiry_batch_037_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_037_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_31507` [discrimination]
  - 변경: notes
  - notes: 군복무 경력을 호봉에 산입하지 않은 것은 불리한 처우이나 합리적 사유가 있다고 판정한 사례 — discrimination 판단이 핵심
- `id_3151` [discrimination]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로자로 전환되었음에도 정당한 사유 없이 계약기간 만료로 근로관계를 종료한 것은 부당해고에 해당한다고 판정한 사례 — dis
- `id_31535` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되지 않아 근로계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_31569` [dismissal_validity]
  - 변경: notes
  - notes: 사용자의 원직복직 명령으로 구제신청의 목적이 달성되었으므로 구제이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_31571` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 사용자와 기간의 정함이 있는 근로계약을 체결하였고, 계약갱신의 기대권이 존재하며, 사용자의 계약갱신 거절에 합리적인 이유가 없다고 판정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
