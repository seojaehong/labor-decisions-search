# misconduct_remaining_batch_068_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_068_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_400415` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정이 사회통념상 현저하게 타당성을 잃어 징계권자의 재량권을 남용하였다고 볼 수 없으며, 징계절차가 적법하므로 징계가 
- `id_400417` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정이 사회통념상 현저하게 타당성을 잃어 징계권자의 재량권을 남용하였다고 볼 수 없으며, 징계절차가 적법하므로 징계가 
- `id_400441` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 이중징계에 해당하지 않으며, 징계양정 및 절차도 적정하여 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 
- `id_400443` [unfair_treatment]
  - 변경: notes
  - notes: 생활폐기물을 수집ㆍ운반하는 근로자가 본인의 작업구역을 벗어나 대형폐기물을 수거한 행위는 징계사유에 해당하고, 사용자가 단체협약에 따라 징계양정을
- `id_400451` [misconduct]
  - 변경: notes
  - notes: 직위해제 처분은 업무상 필요성이 인정되고 생활상 불이익이 근로자가 통상 감수하여야 할 정도를 현저하게 벗어난 것으로 볼 수 없으며, 절차상 위법

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
