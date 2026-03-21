# sexual_harassment_batch_017_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_017_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_53853` [misconduct]
  - 변경: notes, secondary:['procedure', 'harassment_report']→['procedure', 'harassment_report', 'unfair_treatment']
  - notes: 근로자가 직장 내 성희롱 신고자에 해당하지 않는다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_53899` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'workplace_harassment']
  - notes: 근로자의 성희롱 및 직위를 이용한 직장 내 괴롭힘의 행위는 징계사유로 인정되며, 비위행위의 정도에 비해 징계양정이 과하다고 볼 수 없고, 징계절
- `id_53951` [disciplinary_severity]
  - 변경: notes
  - notes: 직장 내 성희롱 행위의 징계사유가 인정되고, 징계양정이 적정하며, 징계절차의 적법성이 인정되어 견책은 정당하다고 판정한 사례 — 비위 인정이나 
- `id_54019` [disciplinary_severity]
  - 변경: notes
  - notes: 징계 사유는 존재하나, 비위에 이르기까지의 사정 및 그 정도, 타 징계자와의 형평 등을 고려할 때 정직의 징계는 양정이 과하여 부당하다고 판정한
- `id_54063` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'workplace_harassment']
  - notes: 근로자의 비위행위 중 직장 내 성희롱 등 일부가 징계사유로 인정되고, 인정되는 징계사유만으로도 해고는 양정이 과도하지 않으며, 징계절차에 하자도

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
