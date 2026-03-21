# sexual_harassment_batch_012_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_012_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_412839` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 양정이 적정하며 절차적 하자가 없다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우
- `id_413013` [misconduct]
  - 변경: notes
  - notes: 이 사건이 각하 사유에 해당하는지 여부 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_413109` [misconduct]
  - 변경: notes
  - notes: 직장 내 성희롱 징계사유가 인정되지 아니하므로 정직 3개월의 징계가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌
- `id_41315` [disciplinary_severity]
  - 변경: notes
  - notes: 성희롱 발언 등 징계사유 대부분이 인정되고, 근로자들의 지위와 책임 등을 고려하면 해고는 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정
- `id_413283` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 비위행위가 징계사유에 해당하고, 징계양정도 적정하며, 징계절차에 하자도 없다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
