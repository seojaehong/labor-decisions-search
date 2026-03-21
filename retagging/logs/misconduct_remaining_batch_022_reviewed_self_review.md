# misconduct_remaining_batch_022_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_022_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_21635` [misconduct]
  - 변경: notes
  - notes: 어린이집 원장으로서 사업 위탁자 및 사용자로부터 요구받은 사항을 개선하지 않고 오히려 갈등을 심화시켜 어린이집 운영에 지장을 초래한 근로자를 해
- `id_21645` [misconduct]
  - 변경: notes
  - notes: 근로자가 직무전념의 의무를 져버리고 직원 간의 금전거래 등의 비위행위를 행하였다는 사유로 행한 징계해고는 정당하다고 판정한 사례 — 비위행위 존
- `id_2165` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정이 적정하며, 징계절차에 하자가 없어 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_21655` [misconduct]
  - 변경: notes
  - notes: 장기간 작업거부로 징계사유가 인정되고, 징계양정도 과하지 않다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_21657` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 일부 인정되나 징계양정이 과하고 징계절차가 부당하며, 아울러 부당노동행위 의사에 따라 발생한 징계라고 판정한 사례 — 부당노동행위(불

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
