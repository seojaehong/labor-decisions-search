# sexual_harassment_batch_006_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_006_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_344155` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 동성 후배 직원에게 행한 '팔뚝, 옆구리, 가슴, 귀, 목, 엉덩이를 접촉한 행위’ 및 '성기를 잡으려는 행위’는 '직장 내 성희롱’으
- `id_34419` [disciplinary_severity]
  - 변경: notes
  - notes: 피해자의 손을 잡고 입맞춤 등의 성희롱 행위는 징계사유로 인정되나, 그 비위행위가 우발적이고 단발적으로 이루어진 것으로 보이므로 해고는 양정이 
- `id_344291` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 피해자1에 대한 신체적ㆍ언어적 성희롱 및 법원에서 유죄로 확정된 강제추행은 정당한 징계사유이고, 징계양정이 적정하며, 징계절차가 적법하므로정당한
- `id_344399` [disciplinary_severity]
  - 변경: notes
  - notes: 징계는 징계사유가 존재하고 양정이 적정하며 절차가 적법하여 정당하고, 인사명령도 정당한 인사권의 범위 내에서 이뤄져 정당하다고 판정한 사례 — 
- `id_344755` [misconduct]
  - 변경: notes
  - notes: 이 사건 해고는 채용계약서상에 명시된 계약해지 사유에 해당하지 않으므로 부당해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
