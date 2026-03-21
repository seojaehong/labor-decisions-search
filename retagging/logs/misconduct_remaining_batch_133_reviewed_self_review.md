# misconduct_remaining_batch_133_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_133_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_56547` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 모두 인정되지만, 양정이 과다하여 해고처분은 부당하고, 불이익 취급 및 지배·개입의 부당노동행위에는 해당하지 않는다고 판정한 사례 —
- `id_56569` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유 중 일부가 인정되고, 인정되는 징계사유의 비위정도가 중대하여 해고의 양정은 적정하며, 징계절차에 하자가 존재하지 않아 징계가 정당하다고
- `id_5657` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 근로관계 종료의 원인이 징계해고이고, 인정되는 징계사유에 비하여 징계양정이 과하여 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 
- `id_56583` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 인정되고, 양정이 적정하며, 절차에 하자가 없어 해고는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중
- `id_56591` [workplace_harassment]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 존재하지 않아 부당한 징계라고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
