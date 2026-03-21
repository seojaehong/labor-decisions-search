# misconduct_remaining_batch_064_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_064_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_38627` [misconduct]
  - 변경: notes
  - notes: 인정되는 징계 사유에 비하여 해고의 양정이 과하지 않으며, 징계 절차가 적법하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접
- `id_38637` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고 징계양정이 적정하며 징계절차에 하자가 없다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_38641` [disciplinary_severity]
  - 변경: notes
  - notes: 개인정보를 무단으로 열람·유용 및 동료 직원들에게 불쾌감을 주었다는 비위행위 등을 이유로 해고한 것은 정당한 해고에 해당한다고 판정한 사례 — 
- `id_38659` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 신청 근로자에게 사회통념상 고용관계를 계속할 수 없을 정도로 책임이 있다고 볼 수 없음에도, 사용자가 재량권을 남용한 것은 징계양정이 과다하여 
- `id_38689` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 공고된 자료 대신 미해당 서류를 수리하는 등의 징계사유가 인정되고, 징계양정 및 절차도 부당하지도 않아 해당 견책처분은 정당하다고 본 사례 — 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
