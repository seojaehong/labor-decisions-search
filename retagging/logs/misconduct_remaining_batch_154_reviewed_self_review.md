# misconduct_remaining_batch_154_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_154_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_9553` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고 절차상 하자는 없으나, 징계양정이 과하여 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_9559` [misconduct]
  - 변경: notes
  - notes: 임금을 목적으로 사용종속적인 관계에서 근로를 제공하는 근로기준법상 근로자에 해당함. 법인의 산하시설 지도점검 결과 지적된 6건의 비위행위는 징계
- `id_9561` [misconduct]
  - 변경: notes
  - notes: 징계사유, 양정 및 절차의 정당성이 모두 인정되어 해고는 정당하다고 판정한 사례 — 비위사실이 명확히 인정되어 해고 정당성 직접 좌우
- `id_957` [unfair_treatment]
  - 변경: notes
  - notes: 근로자의 비위행위에 대한 징계해고는 정당하고, 이는 부당노동행위에 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵
- `id_9577` [misconduct]
  - 변경: notes
  - notes: 징계사유는 인정되나 사용자가 근로자에게 행한 정직 1개월의 징계처분은 그 양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
