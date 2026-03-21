# misconduct_remaining_batch_011_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_011_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_1565` [disciplinary_severity]
  - 변경: notes
  - notes: 공문서 위조 및 허위 공문서 작성은 징계사유로 인정하기 어렵고, 설령 징계사유가 인정되더라도 징계양정이 과하다고 판정한 사례 — 비위 인정이나 
- `id_15689` [unfair_treatment]
  - 변경: notes, conf:medium→high
  - notes: 징계사유에 비해 양정이 과다하여 부당한 반면, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심
- `id_15701` [misconduct]
  - 변경: notes
  - notes: 법원의 유죄판결에 따른 당연 퇴직처분으로 해고가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_15709` [procedure]
  - 변경: notes, secondary:['misconduct', 'work_ability', 'evaluation', 'training_opportunity', 'disciplinary_severity']→['misconduct', 'work_ability', 'evaluation', 'training_opportunity'], conf:medium→high
  - notes: 경고처분이 근로자의 업적평가에 대한 인사규정 및 조직 관리에 따른 정당한 인사권의 행사라고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 
- `id_15713` [misconduct]
  - 변경: notes
  - notes: 일부 징계사유는 인정되나 징계양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
