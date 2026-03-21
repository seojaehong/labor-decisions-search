# misconduct_remaining_batch_037_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_037_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_31087` [misconduct]
  - 변경: notes
  - notes: 노동조합비 횡령으로 인하여 회사 내 조직질서를 문란케 한 징계사유는 일부 인정되나, 양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 
- `id_31111` [misconduct]
  - 변경: notes
  - notes: 연구 부실 및 과제 관리 부적정이 인정되어 기각 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_31119` [disciplinary_severity]
  - 변경: notes
  - notes: 학원의 행정업무를 총괄하는 교수부장이 잦은 지각을 하고 업무진행 사항의 보고를 게을리한 것에 대하여 정직 8일은 정당하다고 판정한 사례 — 징계
- `id_31127` [disciplinary_severity]
  - 변경: notes
  - notes: 징계해고처분이 취소되어 같은 사유로 다시 징계하더라도 일사부재리 원칙에 위배되지 않으며, 징계사유가 인정되고 징계양정이 적정하며 징계절차에 하자
- `id_31129` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 해고는 징계양정이 과하지 않다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
