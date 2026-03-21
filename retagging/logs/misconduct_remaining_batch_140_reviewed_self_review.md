# misconduct_remaining_batch_140_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_140_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_5955` [misconduct]
  - 변경: notes
  - notes: 당직 및 야간근무 시 근무장소를 벗어나 정상적으로 근로를 제공하지 않고 부당하게 연장근로수당을 신청하여 수령한 근로자에 대해 행한 정직 3개월의
- `id_59565` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 양정도 적정하며, 절차에도 하자가 없어 근로자에 대한 정직 2개월의 징계가 정당하다고 판정한 사례 — 비위 인정이나 해고·
- `id_5957` [disciplinary_severity]
  - 변경: notes
  - notes: 인정되는 징계사유에 비하여 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_59571` [procedure]
  - 변경: notes, secondary:['misconduct', 'evaluation', 'disciplinary_severity']→['misconduct', 'evaluation', 'disciplinary_severity', 'workplace_harassment'], conf:medium→high
  - notes: 근로자가 부하직원 및 동료 근로자들에게 직장 내 괴롭힘 행위를 하였음이 인정되고, 인정되는 징계사유에 비해 양정이 과하다고 볼 수 없으며, 징계
- `id_59579` [misconduct]
  - 변경: notes
  - notes: 강사들은 근로기준법상 근로자에 해당하지 않아 이들을 제외하면 사업장은 상시 5명 미만의 근로자를 사용하므로 부당해고 구제신청의 법 적용 대상이 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
