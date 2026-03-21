# misconduct_remaining_batch_152_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_152_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_8797` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유 상당수가 인정되고, 그 비위행위 정도에 비해 징계양정이 과하다고 보기 어려우며, 징계절차도 적법하여 해고가 정당하다고 판
- `id_8801` [workplace_harassment]
  - 변경: notes
  - notes: 사용자의 정당한 업무지시 불이행, 위계질서 침해 등 징계사유가 인정되고, 인정되는 징계사유만으로도 해고의 양정은 적정하며 징계절차도 적법하여 해
- `id_8803` [disciplinary_severity]
  - 변경: notes
  - notes: 인정같은 종류의 비위행위에 대해 이 사건 근로자만 징계처분한 것은 형평에 반하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심
- `id_8807` [disciplinary_severity]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 승무정지 처분은 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_8809` [disciplinary_severity]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 승무정지 처분은 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
