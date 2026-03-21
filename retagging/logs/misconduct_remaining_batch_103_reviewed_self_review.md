# misconduct_remaining_batch_103_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_103_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_44263` [misconduct]
  - 변경: notes
  - notes: 민원인과 전화 상담 중 욕설을 한 전화상담원에 대한 감봉 1회의 징계처분은 징계사유가 인정되고, 징계양정도 과하지 않으며, 징계절차에 하자가 없
- `id_44275` [misconduct]
  - 변경: notes
  - notes: 대기발령에 대한 사유가 정당하지 않고 해당 비위행위가 명백히 드러나지 않으며 업무상 필요성에 비해 생활상 불이익이 과도하므로 대기발령은 인사권을
- `id_44305` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 비위행위는 정당한 징계사유로 인정되나, 그 비위행위에 비하여 징계양정이 과하여 징계해고는 부당하다고 판정한 사례 — 징계양정(제재 수위
- `id_44307` [misconduct]
  - 변경: notes
  - notes: 배차시간을 준수하지 않은 근로자에 대한 정직은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_44321` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 일부가 인정되나, 징계양정이 과하고, 징계절차의 적법성이 인정되지 않은 해고는 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
