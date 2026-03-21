# misconduct_remaining_batch_006_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_006_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_12565` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 존재하고 징계절차에 하자는 없으나, 정직 45일의 중징계는 징계사유에 비해 양정이 과하여 부당하다고 판정한 사례 — 비위 인
- `id_12575` [unfair_treatment]
  - 변경: notes
  - notes: 불성실·저성과 근로자에 대한 정직은 정당하고, 부당노동행위에 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심
- `id_12581` [misconduct]
  - 변경: notes
  - notes: 해고통지서에 근로자가 위반한 취업규칙의 조문만 나열하여 적법한 서면통지가 아니므로 해고가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 
- `id_12589` [unfair_treatment]
  - 변경: notes
  - notes: 복무규정에 따라 승인없이 외부 공연에 출연한 근로자에 대한 견책처분은 정당하고, 부당노동행위로 보기 어렵다고 판정한 사례 — 부당노동행위(불이익
- `id_12613` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유 및 징계절차가 정당하고, 징계양정 또한 적정하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
