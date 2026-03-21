# misconduct_remaining_batch_062_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_062_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_37751` [disciplinary_severity]
  - 변경: notes, conf:high→medium
  - notes: 품위유지의무 위반, 무단결근 등의 징계사유가 존재하고, 징계양정이 과도하다고 보기 어려우며, 징계절차에도 하자가 없어 해당 해고는 정당하다고 판
- `id_37761` [misconduct]
  - 변경: notes
  - notes: 사용자가 삼은 근로자의 징계사유가 존재하지 않아 부당한 해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_37787` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계 사유가 모두 인정되고 징계처분은 재량권 남용에 해당하지 않으며, 절차상 하자도 없어 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론
- `id_37797` [disciplinary_severity]
  - 변경: notes
  - notes: 조합원 제명처분은 징계사유에 비해 징계양정이 과하고, 절차도 지부 운영규정에 위배되어 부당하다고 의결한 사례 — 징계양정(제재 수위)의 적정성이
- `id_3781` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 재량권을 벗어난 과도한 징계로 보이지 않으며, 징계절차에도 하자가 없어 부당정직이 아니라고 판정한 사례 — 비위행위 존재 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
