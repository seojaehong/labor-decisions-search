# sexual_harassment_batch_005_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_005_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_31741` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 만취한 피해자의 손을 잡고 입맞춤 등의 성희롱을 한 행위는 징계사유로 인정되나, 그 비위행위가 우발적이고 단발적으로 이루어진 것으로 보
- `id_31745` [disciplinary_severity]
  - 변경: notes
  - notes: 인사관리를 담당하는 관리자가 부하직원들을 성희롱하여 사용자의 명예 또는 신용에 손상을 입힌 행위는 취업규칙을 위반한 행위로 해고는 정당하다고 판
- `id_31827` [misconduct]
  - 변경: notes
  - notes: 징계사유(성희롱)가 인정되고, 그 비위의 정도가 중대하며, 징계처분의 효력을 부인할 만한 절차상 하자가 존재하지 않아 정당하다고 판단한 사례 —
- `id_31851` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하며, 징계양정이 과도하다고 보기 어렵고, 징계절차에도 하자가 없어 해고가 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수
- `id_31891` [disciplinary_severity]
  - 변경: notes
  - notes: 성추행(성희롱) 등이 징계사유로 인정되고, 징계사유를 볼 때 징계양정이 과하지 않으며, 징계절차상 하자도 없어 정당하다고 판정한 사례 — 징계양

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
