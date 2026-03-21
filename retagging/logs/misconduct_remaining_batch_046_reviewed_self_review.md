# misconduct_remaining_batch_046_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_046_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_345909` [disciplinary_severity]
  - 변경: notes
  - notes: 기본적인 근로제공 의무 거절, 정당한 업무지시 거부 및 무단 근무지 이탈 등을 사유로 한 징계해고는 정당하다고 판정한 사례 — 징계양정(제재 수
- `id_345923` [disciplinary_severity]
  - 변경: notes
  - notes: 근무지 복귀 지시 불응 및 근무지 이탈을 사유로 한 징계해고는 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_345935` [misconduct]
  - 변경: notes, secondary:[]→['disciplinary_severity'], conf:high→medium
  - notes: 인정되는 사유에 비하여 양정이 과하여 해고가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_345941` [unfair_treatment]
  - 변경: notes, secondary:['attendance', 'misconduct', 'procedure', 'disciplinary_severity', 'transfer_validity']→['attendance', 'misconduct', 'procedure', 'disciplinary_severity']
  - notes: 대기발령은 구제이익이 있고, 대기발령1은 업무상 필요성이 없어 부당하며, 대기발령2는 징계절차 착수 전 이루어져 곧바로 후속 처분을 하여 정당하
- `id_345997` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자2는 근로기준법상 근로자에 해당하고, 근로자1 내지 3의 징계사유가 인정되며, 징계양정이 적정하고 징계절차상 하자가 없으므로 해고가 정당하

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
