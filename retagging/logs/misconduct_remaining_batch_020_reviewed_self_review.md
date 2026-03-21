# misconduct_remaining_batch_020_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_020_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_20537` [misconduct]
  - 변경: notes
  - notes: 불법 리베이트 제공의 징계사유는 인정되나 다른 비위행위자에 대한 징계수준과 비교해 형평성에 어긋나므로 해고는 부당하다고 판정한 사례 — 비위행위
- `id_20539` [disciplinary_severity]
  - 변경: notes
  - notes: 직무관련자로부터 향응을 제공받은 것을 사유로 해임한 것은 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_20549` [disciplinary_severity]
  - 변경: notes
  - notes: 프로젝트 종결에 관한 허위보고서를 제출한 행위는 징계사유에 해당하나, 근로자가 얻을 수 있는 금전적 이득 등의 혜택이 없고, 직원과 협의를 통한
- `id_20551` [misconduct]
  - 변경: notes
  - notes: 근로자들에게 적용된 징계사유가 인정되지 않거나, 징계시효가 지나 징계대상으로 삼을 수 없는 사안을 이유로 행한 징계는 부당하다고 판정한 사례 —
- `id_20561` [misconduct]
  - 변경: notes
  - notes: 근로자의 부적절한 공용차량 사용을 이유로 관련 절차에 따라 행한 견책처분은 부당하지 않다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
