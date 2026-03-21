# contract_expiry_batch_078_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_078_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_409969` [dismissal_validity]
  - 변경: notes
  - notes: 해고 기간의 임금상당액이 전액 지급되었으므로 구제이익이 더 이상 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁
- `id_409971` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 갱신기대권은 인정되나, 갱신거절에 합리적인 이유가 있어 근로계약 만료를 통보한 것이 정당하다고 판정한 사례 — 갱신기대권 성립 여부 
- `id_409981` [discrimination]
  - 변경: notes
  - notes: 기간제근로자인 근로자1은 특별상여금이 발생하지 않아 불리한 처우가 존재하지 않으나, 근로자2는 특별상여금이 발생하고 산출된 특별상여금을 지급하지
- `id_409989` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['misconduct', 'procedure', 'disciplinary_severity']
  - notes: 제척기간이 도과하지 않았고, 정직이 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_409991` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'training_opportunity']
  - notes: 근로자의 아동학대 행위는 기간제교원의 계약해지 사유에 해당하므로 해고가 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
