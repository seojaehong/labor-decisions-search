# contract_expiry_batch_099_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_099_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_49519` [renewal_expectation]
  - 변경: notes
  - notes: 로자들의 근로계약 갱신기대권이 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_49569` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['disciplinary_severity', 'dismissal_validity'], conf:high→medium
  - notes: 근로자에게 근로계약 갱신기대권이 인정되지 않으므로 근로계약기간 만료에 따라 정당하게 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부
- `id_4957` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 갱신기대권이 있고, 계약갱신 거절에 합리적 이유가 없으므로 해고가 부당하다고 판정한 사례 — discrimination 판단이 핵심
- `id_49577` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 촉탁직 근로자에 대한 갱신기대권이 있으나 갱신 거절에 합리적인 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_49583` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'unfair_treatment', 'dismissal_validity']→['procedure', 'disciplinary_severity', 'unfair_treatment', 'dismissal_validity']
  - notes: 촉탁직 재고용 기대권은 있으나 재고용 거절에 합리적인 사유가 인정되므로 정년퇴직으로 근로관계를 종료한 것은 정당하다고 판정한 사례 — 갱신기대권

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
