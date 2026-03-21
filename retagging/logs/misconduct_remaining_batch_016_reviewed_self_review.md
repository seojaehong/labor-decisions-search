# misconduct_remaining_batch_016_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_016_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_18507` [disciplinary_severity]
  - 변경: notes
  - notes: 해고무효확인 소송에서 법원이 인정한 징계사유들을 근거로 삼아 근로자에게 행한 강등처분은 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_18525` [disciplinary_severity]
  - 변경: notes
  - notes: 행정기관 직원인 근로자의 도박행위에 대한 징계해고 처분을 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_18547` [misconduct]
  - 변경: notes
  - notes: 인정되는 징계사유에 비해 징계양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_18559` [misconduct]
  - 변경: notes
  - notes: 현금보관증과 지급확인서 임의 발급 등의 징계사유가 인정되고, 징계양정이 적정하여 면직처분이 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이
- `id_18565` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 인정되나 양정이 과하고, 징계절차에도 하자가 있어 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
