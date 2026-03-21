# misconduct_remaining_batch_045_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_045_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_345145` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 노동조합원 제명처분이 징계사유가 명확하지 않고 징계절차에도 하자가 있어 노동조합 규약에 위반된다고 보아 행정관청의 결의ㆍ처분에 대한 시정명령 의
- `id_34515` [disciplinary_severity]
  - 변경: notes
  - notes: 안전 수칙 위반, 허위보고 및 문서위조, 불량한 직무수행 등은 징계사유로 인정되나, 해고는 징계 양정이 과하여 부당하다고 판정한 사례 — 징계양
- `id_345159` [disciplinary_severity]
  - 변경: notes
  - notes: '채용 청탁’의 징계사유가 인정되고, 징계양정이 적정하며, 징계절차에 하자가 없어 정직 6월 처분이 정당하다고 판정한 사례 — 비위 인정이나 해
- `id_345187` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 근로자가 주장하는 해고는 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_345197` [misconduct]
  - 변경: notes
  - notes: 담당 구역 내 특정 지점의 쓰레기를 수거하지 않은 사실이 3년 이상 계속되었음에도 불구하고 구체적으로 해당 구역의 쓰레기를 수거할 것을 지시한 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
