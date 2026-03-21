# misconduct_remaining_batch_047_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_047_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_346425` [misconduct]
  - 변경: notes
  - notes: 부서 소속 직원의 비위행위를 장기간 방치한 부서장에 대한 정직 1월의 징계가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을
- `id_346429` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차에 하자가 없어 해고의 징계는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여
- `id_346431` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차에 하자가 없어 정직 3개월의 징계는 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중
- `id_346443` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계사유에 비해 그 양정이 과하다고 보기 어려워 정당한 징계처분이라 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성
- `id_346445` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 양정이 적정하며, 절차에도 하자가 없어 정직은 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
