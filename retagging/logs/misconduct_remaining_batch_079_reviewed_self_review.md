# misconduct_remaining_batch_079_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_079_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_405775` [misconduct]
  - 변경: notes
  - notes: 징계사유가 일부 인정되며 그 양정이 과하다고 볼 수 없고 징계절차에 중대한 하자도 발견할 수 없으므로 근로자에 대한 견책은 정당하다고 판정한 사
- `id_405777` [disciplinary_severity]
  - 변경: notes
  - notes: 근신의 징계는 사유, 양정, 절차 모두 정당하며, 구상권 청구는 노동위원회 구제대상이 아니라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 
- `id_405787` [misconduct]
  - 변경: notes
  - notes: 해고사유를 인정하기 어려우므로 시용기간 중 해고가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_40579` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에게 음주방조 및 감사방해의 징계사유가 존재하나, 비위행위의 정도에 비해 정직 2월은 양정이 과도하여 부당하고, 직위해제는 존재하지 않으며
- `id_405797` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 중대한 하자가 없어 해고의 징계가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
