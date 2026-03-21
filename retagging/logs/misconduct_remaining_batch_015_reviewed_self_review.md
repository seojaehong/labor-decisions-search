# misconduct_remaining_batch_015_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_015_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_17969` [misconduct]
  - 변경: notes
  - notes: 버스 교통사고의 원인이 근로자의 귀책사유임에도 그 사고원인에 대하여 허위보고를 하고 이를 뒷받침하려는 의도로 적극적으로 조작행위를 한 사실 등이
- `id_17971` [misconduct]
  - 변경: notes
  - notes: 근로자에게 적용된 징계사유가 인정되고 징계절차에 하자가 없지만, 징계사유에 비해 징계양정이 지나쳐 부당징계라고 판정한 사례 — 비위행위 존재 및
- `id_1799` [misconduct]
  - 변경: notes
  - notes: 판정사항: 기각(사용자1), 각하(사용자2)근로자가 상급자의 업무지시를 거부한 사실이 인정되므로 징계사유가 있고, 징계양정 및 절차에 위법함이 
- `id_17993` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 일부 인정되고 징계절차도 적법하나, 징계양정이 과하여 부당해고로 인정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_18007` [unfair_treatment]
  - 변경: notes
  - notes: 일부 인정(부당징계 - 근로자 ○ ○ ○)일부 기각(부당인사초치 - 근로자 고두산, 김성관)부당노동행위 기각 — 부당노동행위(불이익취급·지배개입

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
