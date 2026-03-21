# misconduct_remaining_batch_113_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_113_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_48367` [workplace_harassment]
  - 변경: notes, conf:high→medium
  - notes: 징계사유 중 일부만 인정되고 인정되는 징계사유에 비해 면직처분은 양정이 과하여 부당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_48379` [disciplinary_severity]
  - 변경: notes
  - notes: 대기발령은 업무상 필요성이 있는 정당한 인사명령이며, 해고는 사유, 양정 및 절차 모두 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_48381` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 해고사유들이 취업규칙의 징계사유에 해당함에도 취업규칙의 징계절차를 거치지 않은 것은 해고절차의 하자이므로 부당한 해고라고 판정한 사례 — 징계·
- `id_48387` [misconduct]
  - 변경: notes, secondary:['attendance', 'disciplinary_severity']→['attendance', 'procedure', 'disciplinary_severity']
  - notes: 상사에게 부적절한 언행, 근무 위반 등은 징계사유에 해당되고, 그 정도가 중하여 해고한 것은 양정이 적정하고, 징계절차도 적법하다고 판정한 사례
- `id_4839` [unfair_treatment]
  - 변경: notes
  - notes: 성실 근로 의무 위반으로 정직 처분한 것은 징계사유는 정당하나 징계양정이 과하여 부당하고, 부당노동행위 의사가 있다고 단정하기 어려워 불이익 취

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
