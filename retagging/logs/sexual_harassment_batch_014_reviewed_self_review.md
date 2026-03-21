# sexual_harassment_batch_014_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_014_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_46505` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'workplace_harassment']
  - notes: 징계사유가 인정되고, 징계양정도 적정하며, 징계절차도 적법하여 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을
- `id_46567` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 양정이 적정하며, 절차의 적법성이 인정되어 정직은 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부
- `id_46639` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'workplace_harassment']
  - notes: 근로자에 대한 징계사유가 상당수 인정되고, 그 비위행위 정도에 비해 징계양정이 과하다고 보기 어려우므로 징계가 정당하다고 판정한 사례 — 징계양
- `id_46643` [misconduct]
  - 변경: notes, secondary:['procedure', 'training_opportunity', 'disciplinary_severity']→['procedure', 'training_opportunity', 'disciplinary_severity', 'workplace_harassment']
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차도 하자가 없어 징계해고가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을
- `id_4673` [misconduct]
  - 변경: notes
  - notes: 근로자의 직장 내 성희롱 및 갑질 행위, 회사 공금 횡령 등 비위행위가 모두 징계사유로 인정되고, 인사·노무관리자이자 회계업무전담자로서 행한 비

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
