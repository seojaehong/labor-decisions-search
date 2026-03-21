# misconduct_remaining_batch_044_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_044_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_344685` [unfair_treatment]
  - 변경: notes
  - notes: 근로자에 대한 징계사유는 존재하나, 징계양정이 과하여 근로자에 대한 해고는 부당하지만, 사용자의 부당노동행위 의사를 추정할 만한 특별한 사정이나
- `id_344689` [unfair_treatment]
  - 변경: notes
  - notes: 일부 징계사유가 인정되나, 징계양정이 과다하여 근로자에 대한 해고는 부당하지만, 해고가 사용자의 부당노동행위 의사에서 이루어진 것으로 볼만할 객
- `id_34469` [unfair_treatment]
  - 변경: notes
  - notes: 작업시작시간을 지연시키고 경위서 제출을 수차례 거부하여 행한 정직처분은 정당하고, 불이익 취급의 부당노동행위에 해당되지 않는다고 판정한 사례 —
- `id_344691` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 제척기간은 도과하지 않았고, 근로자들은 근로기준법상 근로자에 해당하며, 징계사유는 인정되나 징계양정이 과도하고 징계절차에 하자가 있어 부당하다고
- `id_344705` [disciplinary_severity]
  - 변경: notes
  - notes: 판정사항은 인정 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
