# misconduct_remaining_batch_040_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_040_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_32881` [unfair_treatment]
  - 변경: notes
  - notes: 교통사고로 2,300만여 원의 물적 피해를 낸 것을 이유로 징계해고한 것은 정당한 해고이며, 부당노동행위에도 해당되지 않는다고 판정 — 부당노동
- `id_32889` [disciplinary_severity]
  - 변경: notes
  - notes: 내부규정에 위반되는 영업활동을 통해 업무대행수수료를 편취한 것이 인정되고, 비위행위 기간, 관리자의 지위 및 금융업 특성을 고려할 때 해고의 양
- `id_32899` [disciplinary_severity]
  - 변경: notes
  - notes: 대학교의 행정정보처장이 주요 사업을 제대로 관리·감독하지 아니하는 등의 비위행위로 사용자에게 막대한 손해를 입힌 것에 대하여 해고는 정당하다고 
- `id_329` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차에 하자가 없어 징계해고가 정당하고, 부당노동행위에도 해당하지 않는다고 판정한 사례 — 부당노동행
- `id_32901` [misconduct]
  - 변경: notes
  - notes: 근로자가 금품을 수수하는 등 비위행위를 하여 사용자가 이를 징계에 부의하고, 근로자가 계속 업무를 담당할 경우 발생할 수 있는 추가 위험을 방지

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
