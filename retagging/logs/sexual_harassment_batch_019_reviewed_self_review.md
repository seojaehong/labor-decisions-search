# sexual_harassment_batch_019_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_019_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_59199` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고 비위행위의 정도를 고려하면 징계양정은 적정하며 징계절차상 하자도 없으므로 해고가 정당하다고 판정한 사례 — 징계양정(제
- `id_59227` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 비위행위에 비하여 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_59239` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure', 'harassment_report']→['misconduct', 'procedure', 'harassment_report', 'workplace_harassment']
  - notes: 징계사유가 존재하고 양정이 적정하며 절차에도 하자가 없어 정직처분은 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 
- `id_59295` [misconduct]
  - 변경: notes, conf:high→medium
  - notes: 직장 내 성희롱으로 인한 정신과적 치료 등을 위하여 근로자가 요청한 유급휴가를 사업주가 거부한 것은 직장 내 성희롱 피해근로자에 대한 차별적 처
- `id_59373` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계절차상 하자가 없으나 양정이 과하여 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
