# contract_expiry_batch_027_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_027_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_26397` [renewal_expectation]
  - 변경: notes
  - notes: 상시 근로자 수가 5명인 사업장이고 근로자에게 근로계약의 갱신기대권은 있으나 갱신거절의 합리적 이유가 있어 근로계약 종료가 정당하다고 판정한 사
- `id_26407` [discrimination]
  - 변경: notes
  - notes: 비교대상근로자들에게 지급한 명절 상여금과 근속수당, 가족수당, 자격수당을 근로자들에게 합리적 사유 없이 지급하지 아니한 것은 차별적 처우라고 판
- `id_26421` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 구제신청을 하여 해고의 효력을 다투던 중 근로계약기간이 만료되어 구제이익이 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또
- `id_26423` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'disciplinary_severity']
  - notes: 인정되는 징계사유에 비해 징계양정이 과하고, 재심 징계절차에 하자가 있어 부당해고라고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이
- `id_26441` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약서 및 관행에 따라 근로계약 갱신에 대한 기대권은 인정되나 근무태도 불량, 교통법규 위반 등 갱신 거부에 합리적인 사유가 있으므로 근로계

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
