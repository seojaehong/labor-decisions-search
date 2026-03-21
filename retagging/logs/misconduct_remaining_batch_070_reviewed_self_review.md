# misconduct_remaining_batch_070_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_070_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_401531` [misconduct]
  - 변경: notes
  - notes: '물품 무단 매각 및 매각대금 임의 보관ㆍ사용한 행위’, '물품 임차계약 부적정하게 체결한 행위’는 징계사유로 인정되나, 해고 처분은 징계로 달
- `id_401581` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 과도하지 않으며 징계절차도 적법하여 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_401585` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 적정하며 징계절차의 하자도 없어 정당한 해고라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 
- `id_401591` [misconduct]
  - 변경: notes
  - notes: 관리자를 무시하는 발언 및 회사에 대한 명예실추 행위 등의 징계사유가 모두 인정되고, 징계양정도 과도하지 않으며 징계절차도 적법하여 정당하다고 
- `id_401593` [misconduct]
  - 변경: notes
  - notes: 서울고등법원 확정 판결에 따라 과거 징계처분 사유 4개 중 2개가 징계사유로 인정되고, 징계양정이 과도하지 아니하며, 징계절차상 하자도 없어 정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
