# misconduct_remaining_batch_001_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_001_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `2016부해OOO` [misconduct]
  - 변경: notes
  - notes: 청렴의무 준수 지시 이후에도 불법찬조금 임의 사용 등 계속된 규정 위반에 대해 행해진 해고는 정당하다고 판정한 사례 — 비위행위 존재 및 중대성
- `2020부노OOO` [unfair_treatment]
  - 변경: notes
  - notes: 징계는 그 사유가 인정되므로 부당노동행위에 해당되지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심
- `2022부해OOO` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하지 않고, 근로기준법 제27조에서 정한 해고의 서면통지 절차를 위반하여 징계해고가 부당하다고 판정한 사례 — 소명기회 미부여 또
- `2023부해OOO` [unfair_treatment]
  - 변경: notes, conf:medium→high
  - notes: 근로자들은 이 사건 구제신청 당사자로 적법하고, 징계사유가 모두 부당하고, 징계절차에 중대한 하자가 존재하므로 부당해고이며, 불이익 취급 및 지
- `id_10003` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고, 양정이 적정하며, 절차가 적법하여 징계해고는 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
