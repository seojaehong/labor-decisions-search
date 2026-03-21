# misconduct_remaining_batch_119_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_119_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_50703` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 적정하며, 징계절차도 적법하여 해고가 정당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_5071` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유 중 감사결과 보고서 허위 작성은 중대한 과실로 인정되나 나머지는 징계사유로 인정하기 어렵고, 강등의 징계는 징계양정이 과
- `id_50719` [dismissal_validity]
  - 변경: notes, secondary:['absence_without_leave', 'misconduct', 'procedure', 'training_opportunity', 'disciplinary_severity']→['absence_without_leave', 'misconduct', 'procedure', 'training_opportunity']
  - notes: 구두로 사직의 의사를 밝히고 회사를 나간 뒤 업무 인수인계도 하지 않고 장기간 무단결근한 근로자를 해고한 것은 정당하다고 판정한 사례 — 해고 
- `id_50721` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자1에 대한 해고는 정당하고, 근로자2에 대한 해고는 징계사유에 비해 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_50723` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계절차는 적법하나 양정이 과하므로 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
