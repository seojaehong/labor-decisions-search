# misconduct_remaining_batch_155_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_155_reviewed`
- 2차 패스 처리 건수: 12
- 실질 변경 건수: 12
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_9897` [misconduct]
  - 변경: notes
  - notes: 근로자의 징계사유가 모두 인정되지 않고 정직이 부당하다고 판정한 사례 — 비위사실이 명확히 인정되어 해고 정당성 직접 좌우
- `id_9907` [workplace_harassment]
  - 변경: notes
  - notes: 근로자가 행한 대부분의 비위행위가 징계사유에 해당하고 징계양정이 적정하며 징계절차도 적법하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_9915` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계해고가 사유, 양정, 절차에 있어 모두 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_9925` [misconduct]
  - 변경: notes
  - notes: 근로자들의 징계사유는 고의성 및 사익편취가 존재하지 않아 일반징계사유의 소멸시효 3년이 적용되어야 하므로 소멸시효 3년을 도과하여 행한 감봉처분
- `id_9935` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 소속 회사와 거래하는 납품업체를 실질적으로 소유하고 사무를 처리하고 편의 제공을 청탁한 행위로 징계해고한 것이 정당한 지 여부를 판정한 사례 —

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
