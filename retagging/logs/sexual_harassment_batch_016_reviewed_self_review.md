# sexual_harassment_batch_016_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_016_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_51293` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 정당한 것으로 인정되고 징계양정이 적정하며 징계절차가 적법하므로 해임의 징계는 정당하다고 판정한 사례 — 징계양정(제재 수위)의
- `id_51319` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 근로자를 징계의결 확정시까지 직위해제 및 대기발령 처분한 것은 사용자의 고유권한에 속하는 정당한 인사권 행사에 해당하나 근로자에 대한 징계사유가
- `id_51405` [disciplinary_severity]
  - 변경: notes
  - notes: 비위행위 모두 징계사유로 인정되고 징계절차에도 특별한 하자가 없으나 근로자의 비위행위의 정도에 비해 양정이 과하여 부당하다고 판정한 사례 — 징
- `id_51417` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'workplace_harassment']
  - notes: 징계사유가 대부분 인정되고 비위행위의 정도를 고려할 때 징계양정이 적정하며 징계절차에 하자가 없으므로 해고는 정당하다고 판정한 사례 — 징계양정
- `id_51419` [disciplinary_severity]
  - 변경: notes, secondary:['misconduct', 'procedure']→['misconduct', 'procedure', 'unfair_treatment']
  - notes: 근로자의 징계사유가 모두 정당한 징계사유로 인정되고, 징계양정이 적정하며, 징계절차에 하자가 없어 해고는 정당하다고 판정한 사례 — 징계양정(제

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
