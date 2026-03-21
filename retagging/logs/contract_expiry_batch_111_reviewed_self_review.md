# contract_expiry_batch_111_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_111_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_56091` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 초심 유지 (초심: 기각)이 사건 근로자에게 근로계약에 대한 갱신기대권 또는 무기계약직 전환기대권이 인정되지 않으므로, 당사자 간 근로관계는 계
- `id_56109` [discrimination]
  - 변경: notes
  - notes: 비교대상근로자는 존재하나, 합리적 이유 없는 차별적 처우라 볼 수 없다고 판정한 사례 — discrimination 판단이 핵심
- `id_5611` [dismissal_validity]
  - 변경: notes
  - notes: 기간제(계약직) 근로계약으로, 계약기간 만료에 따라 근로관계가 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또
- `id_56111` [discrimination]
  - 변경: notes
  - notes: 근로자에 대한 불리한 처우가 존재하지 않는다고 판정한 사례 — discrimination 판단이 핵심
- `id_56113` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 만료로 근로관계가 종료되었으므로 해고는 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
