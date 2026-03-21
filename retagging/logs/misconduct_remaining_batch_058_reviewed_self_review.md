# misconduct_remaining_batch_058_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_058_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_35817` [misconduct]
  - 변경: notes
  - notes: 여러 차례 동종의 비위행위로 징계처분을 받은 근로자에 대해 단체교섭장에서 발생한 폭력을 사유로 행한 해고는 정당하다고 판정한 사례 — 비위행위 
- `id_35821` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자가 사용자의 승인 없이 임의로 계약을 체결한 사실은 징계사유로 인정되며, 징계양정이 적정하다고 판정한 사례 — 징계·해고 절차 하자가 결론
- `id_35833` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계절차도 적법하나, 징계양정이 과하여 부당해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_35837` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 적정하며 징계절차에 하자가 없어 정당하고, 부당노동행위에 해당되지 않는다고 판정한 사례 — 부당노동행위(불이익취급
- `id_35839` [disciplinary_severity]
  - 변경: notes
  - notes: 징계 사유가 정당하고, 징계 양정이 적정하며, 징계 절차에 하자가 없어 징계 처분이 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
