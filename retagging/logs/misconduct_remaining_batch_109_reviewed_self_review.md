# misconduct_remaining_batch_109_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_109_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_46751` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자가 정당한 인사명령에 불응하여 결근한 것은 무단결근에 해당하는 등 정당한 징계사유가 인정되고, 징계양정이 적정하며 징계절차상 하자도 없어 
- `id_46757` [disciplinary_severity]
  - 변경: notes
  - notes: 인정되는 징계사유에 비해 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_46765` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유는 인정되나, 비위행위의 정도에 비하여 직무정지 및 부서이동의 징계처분은 양정이 과도하므로 부당하다고 판정한 사례 — 징계
- `id_46787` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 정당한 것으로 인정되고, 해고의 징계양정이 사회통념상 현저하게 타당성을 잃어 징계권자의 재량권을 일탈？남용한 것이라고 보기 어려우며,
- `id_46789` [misconduct]
  - 변경: notes
  - notes: 사용자가 선행 징계처분과 동일한 징계혐의사실을 사유로 하여 근로자들을 징계한 것은 이중징계에 해당하여 부당하다고 판정한 사례 — 비위행위 존재 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
