# misconduct_remaining_batch_128_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_128_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_54415` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차도 적법하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우
- `id_54435` [misconduct]
  - 변경: notes
  - notes: 사용자가 삼은 징계사유가 존재하지 않아 정직이 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_54439` [disciplinary_severity]
  - 변경: notes
  - notes: 일부 징계사유가 존재하고 절차상 하자는 없으나 양정이 과다하여 부당한 해고라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 
- `id_54453` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 존재하고, 양정이 적정하며, 징계절차가 적법한바, 감봉 3개월은 적법하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_54463` [workplace_harassment]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'disciplinary_severity']
  - notes: 근로자3에 대한 정직 3개월 처분은 과도한 처분으로 부당하며, 근로자1에 대한 해고 및 근로자2에 대한 정직 3개월의 처분은 사유가 인정되고, 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
