# misconduct_remaining_batch_033_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_033_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_28349` [unfair_treatment]
  - 변경: notes
  - notes: 차량 미배차는 관행으로 행해진 업무상 조치이나 일부 징계사유는 부적절하고, 징계 재량권을 일탈·남용하여 징계양정이 부당하며 부당노동행위는 일부 
- `id_28429` [disciplinary_severity]
  - 변경: notes
  - notes: 신청인은 근로기준법상의 근로자로 인정되고, 징계사유가 존재하나, 해고는 양정이 과도하고 징계절차도 위법하다고 판정한 사례 — 비위 인정이나 해고
- `id_28431` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 금품수수를 비롯한 8가지 징계사유가 모두 인정되고 징계의 양정과 절차도 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_28443` [procedure]
  - 변경: notes
  - notes: ○ ○ ○의 교무관장은 근로기준법상 근로자이며, 징계사유 중 일부만 인정되어 해고는 양정이 과하여 부당하다고 판정한 사례 — 징계·해고 절차 하
- `id_28451` [unfair_treatment]
  - 변경: notes
  - notes: 근로자의 명예훼손 행위, 업무지시 불응 등을 사유로 한 징계 해고는 정당하고 부당노동행위에 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
