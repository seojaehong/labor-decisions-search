# misconduct_remaining_batch_127_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_127_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_53995` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 비위행위의 정도를 고려할 때 감봉의 징계는 징계양정이 적정하며 징계절차상 하자가 없으므로 정당하다고 판정한 사례 — 비위행위
- `id_54005` [workplace_harassment]
  - 변경: notes
  - notes: 근로자의 징계사유가 일부 인정되고, 비위행위 정도에 비해 징계양정이 적정하며, 징계절차에 하자가 없으므로 해고가 정당하다고 판정한 사례 — 직장
- `id_5401` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로기준법상 근로자에 해당하나, 근로자에게 행한 징계(면직)는 징계사유도 인정되고 양정도 적정하며 절차상 하자도 없어 정당하다고 판정한 사례 —
- `id_54011` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 정직 20일의 징계는 양정이 적정하며 징계절차상 하자도 없으므로 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 
- `id_54023` [unfair_treatment]
  - 변경: notes
  - notes: 근로자들에 대한 징계사유 중 일부는 인정되나 징계양정이 과다하여 징계처분이 부당하나, 징계처분이 사용자의 부당노동행위 의사에 의한 것으로 볼 만

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
