# misconduct_remaining_batch_059_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_059_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_36325` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 징계절차에 하자는 없으나, 인정되는 징계사유에 비해 징계양정이 과도하여 부당해고로 판정한 사례 — 징계양정(제재 수위)
- `id_36329` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자에 대한 징계사유가 인정되고, 사용자가 징계권 행사의 재량권을 일탈·남용한 것이라고 볼 수 없으며, 절차상의 하자도 없어 정당한 징계라고 
- `id_36351` [misconduct]
  - 변경: notes
  - notes: 징계해고 이전의 대기발령이 무효인 이상 사용자가 징계사유로 삼은 무단결근을 징계사유로 인정할 수 없어 부당해고라고 판정한 사례 — 비위사실 자체
- `id_36367` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 과하다고 볼 수 없으며 징계절차에 하자가 없어 정직 3월의 징계처분은 정당하고, 부당노동행위에도 해당하지 않는다고
- `id_36373` [disciplinary_severity]
  - 변경: notes
  - notes: 은행의 기업대출 담당자인 근로자가 기업에 대출을 실시하고 브로커로부터 120만 원 상당의 상품권을 수수한 행위는 사용자와의 신뢰관계를 심각하게 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
