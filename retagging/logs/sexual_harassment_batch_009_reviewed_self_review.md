# sexual_harassment_batch_009_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_009_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_401505` [misconduct]
  - 변경: notes
  - notes: 이 사건 사용자에게 이 사건 근로자의 비위행위에 대하여 징계 처분을 할 권한이 인정되고, 공소시효가 도과되었다 하더라도 징계가 가능하며, 이 사
- `id_401533` [misconduct]
  - 변경: notes
  - notes: 차별적 처우가 존재하지 않는다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_401857` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계절차가 적법하나, 징계사유에 해당하는 비위행위의 정도에 비하여 징계양정이 과하여 부당하다고 판정한 사례 — 비위 인정이나
- `id_401867` [disciplinary_severity]
  - 변경: notes
  - notes: 직장 내 성희롱을 사유로 한 해고는 징계사유가 존재하고 징계양정이 과다하지 않으며 징계절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정
- `id_401871` [misconduct]
  - 변경: notes, conf:high→medium
  - notes: 징계사유의 존재가 명확하지 않고, 설령 징계사유가 인정된다고 하더라도 징계양정이 과도하여 부당한 것으로 판정한 사례 — 비위행위 존재 및 중대성

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
