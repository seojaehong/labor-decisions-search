# misconduct_remaining_batch_115_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_115_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_49173` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 정당하고, 징계양정이 적정하며, 징계절차가 적법하여 징계해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵
- `id_4921` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하고(다만 MSC운영지침에 맞지 않게 특별휴가를 사용한 부분은 징계사유로 부적절) 징계 절차가 적법하며 이 사건 발생의 경위 및 
- `id_49217` [misconduct]
  - 변경: notes
  - notes: 사용자가 근로자를 해고한 근거로 든 징계사유 중 일부가 인정된다고 하더라도 징계양정의 재량권을 남용하였고 절차상 하자가 크다고 볼 수 있어 부당
- `id_49219` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 시용기간 중인 근로자의 음주운전을 사유로 한 해고는 합리적 이유가 있어 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁
- `id_4923` [unfair_treatment]
  - 변경: notes
  - notes: 인터넷 카페에 댓글을 작성하여 회사의 비공개 정보를 유출하고 불명확한 사실을 단정적으로 적시하여 회사의 신뢰도를 훼손한 행위에 대한 정직 3월의

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
