# misconduct_remaining_batch_142_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_142_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_60331` [misconduct]
  - 변경: notes
  - notes: 근로자가 회사의 공금 80만 원을 분실하고 보고하지 않은 사실은 징계사유에 해당하나 양정이 과다하여 부당하다고 판정한 사례 — 비위행위 존재 및
- `id_60337` [misconduct]
  - 변경: notes
  - notes: 사용자에게 고용관계를 원상회복하겠다는 진정성이 있다고 볼 수 없으므로 구제신청의 이익이 존재하며, 정당한 징계사유가 확인되지 않아 부당해고라고 
- `id_60339` [disciplinary_severity]
  - 변경: notes
  - notes: 고의 저속 운행, 무단 승무 불이행, 무단결근 등을 한 시내버스 운전원에 대한 정직 1월의 징계처분은 정당하다고 본 사례 — 징계양정(제재 수위
- `id_60341` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 인정되며, 징계절차가 적법하나, 인정되는 징계사유에 비해 징계양정이 과하므로 부당해고라고 판정한 사례 — 직장 내 괴롭힘 성립 여부가
- `id_60347` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차에도 하자가 없어 정직이 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
