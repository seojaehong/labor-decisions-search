# sexual_harassment_batch_015_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_015_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_48871` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'workplace_harassment']
  - notes: 징계사유가 대부분 인정되고 비위행위의 정도를 고려할 때 징계양정이 적정하며 징계절차에 하자가 없으므로 해고는 정당하다고 판정한 사례 — 징계양정
- `id_48939` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'workplace_harassment']
  - notes: 징계사유가 모두 인정되며 징계양정이 적정하고 징계절차상 하자가 없으므로 감봉 1월의 징계처분이 정당하다고 판정한 사례 — 징계양정(제재 수위)의
- `id_48971` [disciplinary_severity]
  - 변경: notes
  - notes: 해고처분은 징계사유가 존재하고 징계양정이 적정하며 징계절차도 적법하여 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가
- `id_49007` [dismissal_validity]
  - 변경: notes
  - notes: 근로자는 시용근로자에 해당하고, 본채용 거부에 합리적인 이유가 있으며 절차상 하자가 없으므로 본채용 거부가 정당하며, 이 경우 보직해임과 견책처
- `id_49053` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 과거 성희롱으로 인한 ‘정직 2월’의 징계 이력이 있음에도, 또다시 성희롱의 비위행위를 하여, 사용자가 단체협약 등 관련 규정에 따라 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
