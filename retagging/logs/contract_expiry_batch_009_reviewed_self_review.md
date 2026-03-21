# contract_expiry_batch_009_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_009_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_15309` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간의 만료로 인해 구제신청의 이익이 소멸되었다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_1531` [renewal_expectation]
  - 변경: notes, secondary:['unfair_treatment', 'dismissal_validity']→['disciplinary_severity', 'unfair_treatment', 'dismissal_validity']
  - notes: 근로자1에 대한 해고는 정당하고, 근로자2, 3은 갱신기대권이 인정됨에도 합리적인 이유 없이 계약기간 만료로 고용관계를 종료하여 부당하나, 부당
- `id_15369` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 기간의 정함이 없는 근로자로 전환되었으므로 계약기간 만료를 사유로 근로계약을 종료한 것은 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는
- `id_15385` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정됨에도 합리적인 이유 없이 재계약을 거부한 것은 부당해고에 해당된다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이
- `id_15393` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로계약 갱신거절에 합리적 이유가 없어 부당해고로 판정한 사례 — discrimination 판단이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
