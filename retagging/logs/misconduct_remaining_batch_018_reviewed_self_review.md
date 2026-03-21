# misconduct_remaining_batch_018_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_018_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_19539` [disciplinary_severity]
  - 변경: notes
  - notes: 2016년 2분기 조직도입 및 업적이 전무한 것은 징계사유로 인정되고, 징계양정도 과하지 않아 경고의 징계처분은 정당하다고 판정한 사례 — 징계
- `id_19547` [misconduct]
  - 변경: notes
  - notes: 일용직 인건비를 부당하게 집행하고, 직무관련자로부터 금품을 수수한 행위를 이유로 행한 파면은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성
- `id_19549` [misconduct]
  - 변경: notes
  - notes: 국책과제비 집행 부적정 등 일부 징계사유는 인정되나 양정이 과하여 부당해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌
- `id_19563` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유에 비해 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_19615` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 중 일부가 인정되나 양정이 과하여 부당한 해고라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
