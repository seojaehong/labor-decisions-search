# misconduct_remaining_batch_135_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_135_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_5737` [disciplinary_severity]
  - 변경: notes
  - notes: 일부 인정되는 징계사유에 비해 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_57373` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 근로자에 대한 해고가 정당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가
- `id_57377` [unfair_treatment]
  - 변경: notes
  - notes: 정직처분은 징계사유가 정당하고, 징계양정이 적정하며, 징계절차가 적법하여 정당하고, 불이익 취급 및 지배ㆍ개입의 부당노동행위에 해당하지 않는다고
- `id_57385` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 적정하며 징계절차상 하자가 없어 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_5739` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 대부분 인정되고, 징계양정이 과다하지 않으며, 징계절차에 하자가 없어 해고는 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
