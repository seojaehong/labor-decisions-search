# misconduct_remaining_batch_042_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_042_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_34127` [misconduct]
  - 변경: notes
  - notes: 업무상 횡령 등의 징계사유가 인정되고 징계양정기준에 비추어 볼 때 양정이 과하지 않으며, 징계절차상 하자가 없으므로 해고가 정당하다고 판정한 사
- `id_34133` [misconduct]
  - 변경: notes, conf:medium→high
  - notes: 노동조합의 조합원들에 대한 제명처분은 징계사유의 정당성이 인정되지 않고, 징계절차 또한 중대한 하자가 있어 노동조합 규약에 위반된다고 의결한 사
- `id_34165` [misconduct]
  - 변경: notes
  - notes: 사용자가 근로자에게 행한 2018. 11. 1.자 징계면직은 사유가 존재하고, 절차상 중대한 하자는 없으나, 양정이 과하다고 판단하여 부당해고로
- `id_3417` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 업무상 횡령은 징계사유에 해당하며, 비위행위에 따른 징계양정도 적정하고, 징계절차상 하자도 없어 해임은 정당하다고 판정한 사례 — 징계·해고 절
- `id_34175` [misconduct]
  - 변경: notes
  - notes: 수년에 걸친 공금 횡령·유용 등에 대하여 행한 해고는 정당하며, 징계부가금의 부과는 노동위원회의 심판대상이 아니라고 판정 — 비위행위 존재 및 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
