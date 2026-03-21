# misconduct_remaining_batch_117_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_117_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_50019` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되지 않아 정직은 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_50039` [misconduct]
  - 변경: notes
  - notes: 근로자의 비위행위가 징계사유로 인정되나 징계양정이 과다하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_50043` [misconduct]
  - 변경: notes
  - notes: 징계사유가 모두 정당한 징계사유로 인정되고 징계절차가 적법하나 징계양정이 과도하여 징계해고는 정당하다고 판정한 사례 — 비위행위 존재 및 중대성
- `id_50057` [procedure]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 징계양정이 과도하여 해고는 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_50093` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 인정되지 않으므로 감봉처분이 부당하다고 보았지만, 불이익 취급 및 지배ㆍ개입의 부당노동행위에 해당하지는 않는다고 판정한 사례 — 부당

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
