# misconduct_remaining_batch_110_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_110_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_47167` [disciplinary_severity]
  - 변경: notes
  - notes: 교육용 차량을 사적으로 무단 사용한 행위 및 수강생에 대한 불친절한 태도 등 일부 행위는 징계사유로 인정되나, 그 사유에 비해 양정이 과도하여 
- `id_47185` [misconduct]
  - 변경: notes
  - notes: 해고사유가 인정되지 않아 근로자에게 사회통념상 고용관계를 유지할 수 없을 정도의 책임 있는 사유가 있다고 보기 어려워 해고가 부당하다고 판정한 
- `id_47189` [disciplinary_severity]
  - 변경: notes
  - notes: 일부 징계사유가 인정되고 징계절차의 적법성은 인정되나, 인정되는 징계사유에 비해 해고는 양정이 과하여 부당하다고 판정한 사례 — 비위 인정이나 
- `id_47191` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 채용비리와 관련하여 업무방해죄의 유죄판결(벌금 200만원, 집행유예 1년)을 받은 근로자들에 대한 직권면직에 있어 직권면직의 사유 및 절차가 정
- `id_47193` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당한 징계라고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
