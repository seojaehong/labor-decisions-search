# misconduct_remaining_batch_149_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_149_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_773` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하지 않아 징계처분은 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_7741` [procedure]
  - 변경: notes, secondary:['misconduct', 'training_opportunity', 'disciplinary_severity']→['misconduct', 'training_opportunity', 'disciplinary_severity', 'workplace_harassment'], conf:medium→high
  - notes: 징계사유가 존재하고, 징계양정 또한 징계재량권을 남용하였다고 볼 수 없으며, 징계절차상 하자가 없으므로 파면처분은 정당하다고 판정한 사례 — 징
- `id_7743` [workplace_harassment]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 해고의 양정이 과하여 부당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_7749` [workplace_harassment]
  - 변경: notes
  - notes: 근로자가 폭행으로 회사 직원에게 상해를 입힌 행위를 징계사유로 삼은 것은 정당하나, 근로자와 쌍방폭행 당사자의 징계 형평성 등을 고려하였을 때 
- `id_7755` [disciplinary_severity]
  - 변경: notes
  - notes: 근로기준법상 근로자에 해당하고 징계사유는 인정되나, 징계사유에 비하여 해고의 양정이 과하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
