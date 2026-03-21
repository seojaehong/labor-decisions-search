# misconduct_remaining_batch_054_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_054_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_350477` [misconduct]
  - 변경: notes
  - notes: 징계사유가 일부 인정되나, 징계양정이 과하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_350479` [misconduct]
  - 변경: notes
  - notes: 이 사건 근로자에 대한 당연면직은 그 사유가 단체협약 등 관련 규정에 위배되지 아니하고 절차상 하자가 있다고 보기 어렵고, 강등처분 역시 그 사
- `id_350493` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근무시간 중 겸업행위 및 개인성과 조작행위의 징계사유가 모두 인정되고 양정도 적정하여 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 
- `id_350533` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고, 절차상 중대한 하자가 있다고 볼 수도 없으나, 인정되는 징계사유만으로는 양정이 과하여 부당하다고 판정한 사례 — 징계
- `id_350543` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 비위행위의 정도를 고려할 때 징계양정이 적정하며 징계절차가 적법하여 해고가 정당하다고 판정한 사례 — 비위행위 존재 및 중대

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
