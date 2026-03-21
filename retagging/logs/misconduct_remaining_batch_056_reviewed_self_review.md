# misconduct_remaining_batch_056_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_056_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_351599` [misconduct]
  - 변경: notes
  - notes: 구체적인 지휘ㆍ감독 등 사용 종속적인 관계를 인정하기 어려워, 근로기준법상 근로자가 아니라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정
- `id_351605` [misconduct]
  - 변경: notes
  - notes: 감봉은 구제이익이 없고, 보직해임은 업무상 필요성이 인정되어 정당한 처분이나, 정직은 징계사유가 존재하지 않아 부당하다고 판정한 사례 — 비위행
- `id_351609` [disciplinary_severity]
  - 변경: notes
  - notes: 횡령, 부적정한 예탁금 지급 처리 등 징계사유가 인정되고, 징계 양정도 적정하며, 징계 절차에도 하자가 존재하지 않으므로 징계가 정당하다고 판정
- `id_35161` [disciplinary_severity]
  - 변경: notes
  - notes: 대기발령은 이중징계에 해당하고 회사 공금을 개인용도로 사용한 것은 징계사유로 인정되나 해고는 양정이 과하여 부당해고라고 판정한 사례 — 징계양정
- `id_351617` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유 중 1가지만 정당한 징계사유로 인정되는 데 비하여, 징계해고의 양정은 과도하여 징계가 부당하다고 판정한 사례 — 징계양정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
