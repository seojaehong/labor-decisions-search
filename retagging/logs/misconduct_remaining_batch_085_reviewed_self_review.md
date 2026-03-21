# misconduct_remaining_batch_085_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_085_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_40871` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 수의계약 절차를 위반하고, 납품부수를 줄여주는 등 부적절하게 업무를 처리한 행위, 교육을 실시하지 않았음에도 교육비를 지급한 행위, 직
- `id_408713` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure']
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당한 징계라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여
- `id_408715` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자1,2는 징계사유가 인정되고, 징계양정도 적정하며 징계절차상 하자가 없으므로 해고가 정당하나, 근로자3은 징계사유를 인정할 수 없어 부당하
- `id_408725` [procedure]
  - 변경: notes
  - notes: 징계사유로 삼은 내용 중 직무상 명령 불이행, 품위유지의 의무 위반 등 일부만 징계사유로 인정되고 인정되는 징계사유만으로는 그 양정이 과하므로 
- `id_408731` [misconduct]
  - 변경: notes
  - notes: 부당지시 금지 위반, 부당여신 취급, 복무자세 및 품위유지의무 위반의 징계사유가 대부분 인정되고 징계양정이 적정하며 징계절차에 하자가 없으므로 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
