# misconduct_remaining_batch_076_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_076_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_404277` [disciplinary_severity]
  - 변경: notes
  - notes: 근무지시는 정당하며, 정직은 징계사유가 존재하고, 양정도 적정하며, 절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수
- `id_404283` [disciplinary_severity]
  - 변경: notes
  - notes: 관리자로서 주의를 다하지 않은 책임은 징계사유로 인정되고, 징계양정이 적정하며 징계절차도 준수하여 해고가 정당하다고 판정한 사례 — 징계양정(제
- `id_404289` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계 양정도 적정하며, 징계 절차에도 하자가 존재하지 않으므로 해고가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이
- `id_404297` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 인정되나, 징계사유에 비해 '해고’의 징계양정이 사회통념상 현저하게 타당성을 잃어 징계권자의 재량권을 일탈？남용한 것이라고 
- `id_404307` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 근로자는 카페 매니저로 판매물품 반출 및 현금 횡령과 관련한 비위행위에 대해 사업주와 면담을 통해 사직서를 제출한 것은 사용자들의 강요 혹은 강

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
