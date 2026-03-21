# misconduct_remaining_batch_089_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_089_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_410613` [misconduct]
  - 변경: notes
  - notes: 외교관 서명 모사 및 공관장 직인 무단 날인 등 징계사유가 모두 인정되므로 재외공관 행정직원에 대한 징계해고가 정당하다고 판정한 사례 — 비위사
- `id_410615` [misconduct]
  - 변경: notes
  - notes: 사용자가 주장하는 징계사유가 모두 인정되나 비위의 정도와 과실이 징계기준에 부합하지 않아 양정이 과하므로 해고는 부당하다고 판정한 사례 — 비위
- `id_410617` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 모두 인정되고 양정이 적정하며 절차상 하자가 존재하지 않으므로 징계해고는 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직
- `id_410647` [misconduct]
  - 변경: notes
  - notes: 징계사유 중 일부가 인정되나 감봉 6개월의 징계양정이 과도하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_41065` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 대기발령은 업무상 필요성이 인정되고 근로자의 생활상 불이익도 크지 않으므로 정당하며, 정직의 징계는 징계 사유, 양정 및 절차 모두 정당하다고 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
