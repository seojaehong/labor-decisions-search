# misconduct_remaining_batch_123_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_123_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_52461` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되나, 인정되는 비위행위에 비해 해고의 징계는 징계양정이 과도하고, 근로자의 재심청구권을 박탈하여 징계절차에 중대한 하자가 존재하
- `id_52479` [unfair_treatment]
  - 변경: notes
  - notes: 사용자가 개인정보 보호법을 위반하였다고 단정할 수 없고, 근로자의 지속적인 교통법규 위반 및 지시 위반행위를 이유로 행한 징계(정직 5일)가 부
- `id_52481` [misconduct]
  - 변경: notes
  - notes: 근로자의 징계사유는 징계시효가 도과되어 절차상 위법한 징계라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_52485` [procedure]
  - 변경: notes, secondary:['misconduct', 'disciplinary_severity']→['misconduct', 'disciplinary_severity', 'workplace_harassment'], conf:medium→high
  - notes: 징계사유에 비하여 양정이 과하여 부당강등이라고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_52491` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유가 일부 존재하고, 징계절차에 중대한 하자가 있어 근로자에 대한 해고는 부당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
