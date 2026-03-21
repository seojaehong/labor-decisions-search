# misconduct_remaining_batch_082_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_082_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_407301` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정도 적정하며 징계절차도 적법하여 징계해고처분이 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직
- `id_40733` [misconduct]
  - 변경: notes
  - notes: 사회복지시설의 원장인 근로자가 입소자들을 비하하고, 입소자들에게 유류금품을 기부하도록 강요하는 행위 등은 징계사유로 인정되며 이에 대해 사용자가
- `id_407335` [misconduct]
  - 변경: notes
  - notes: 근로자들의 징계사유가 인정되고, 징계절차에 하자는 없으나, 징계사유에 비하여 양정이 과도하여 강등 처분이 부당하다고 판정한 사례 — 비위행위 존
- `id_407343` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 고용관계를 지속하기 어려울 정도의 비위행위를 하였음에도 개선 가능성이 매우 낮아 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을
- `id_40735` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정도 적정하며, 절차도 적법하여 정직 3개월 처분은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
