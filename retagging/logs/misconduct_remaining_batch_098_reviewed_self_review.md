# misconduct_remaining_batch_098_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_098_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_42209` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고 징계절차에 하자는 없으나, 징계양정이 과도하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_42231` [dismissal_validity]
  - 변경: notes
  - notes: 사용자1은 부설기관에 불과하여 당사자 적격이 없고, 사용자2에 대하여는 근로자가 사용자에게 해약권이 유보된 시용근로자에 해당하나, 본채용 거절은
- `id_42237` [disciplinary_severity]
  - 변경: notes
  - notes: 일부 징계사유의 징계시효를 연장한 인사규정의 개정은 무효이며, 직권면직 처분은 사실상 징계해고이고, 일부 징계사유는 인정되며 징계절차는 정당하나
- `id_42239` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 동료직원과의 다툼, 시말서(경위서) 제출 거부는 징계사유에 해당하나, 다툼으로 인한 사업장 영업손실이 크지 않고, 근로자가 시말서(경위서)를 제
- `id_42259` [disciplinary_severity]
  - 변경: notes
  - notes: 신용협동조합 인장 부당 사용, 이사회 결의 없이 직원연봉 인상 품의 등을 한 실무책임자를 징계면직한 것은 부당하지 않다고 판정한 사례 — 징계양

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
