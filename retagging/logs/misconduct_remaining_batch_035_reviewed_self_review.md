# misconduct_remaining_batch_035_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_035_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_29821` [misconduct]
  - 변경: notes
  - notes: 근로자의 부주의로 인한 교통사고에 대하여 승무정지 10일의 징계처분은 정당하고 불이익 처분의 부당노동행위라고 볼 수 없다고 판정한 사례 — 비위
- `id_29837` [procedure]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'disciplinary_severity'], conf:medium→high
  - notes: 직위해제는 업무상 필요성이 인정되지 않아 부당하고, 해고는 징계절차를 거치지 않았고, 이중징계에 해당하며, 사유에 비하여 양정이 과하여 부당하다
- `id_29841` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유에 비해 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_29843` [disciplinary_severity]
  - 변경: notes
  - notes: 법인카드를 개인적 용도로 사용한 것으로 볼 수 없고, 직무관련자로부터 향응수수 행위는 징계사유로 인정되나 파면처분은 비위의 정도에 비하여 양정이
- `id_29849` [misconduct]
  - 변경: notes
  - notes: 징계사유는 존재하나, 그에 따른 해고는 징계양정이 과도하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
