# misconduct_remaining_batch_025_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_025_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_23267` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유, 양정, 절차 모두 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_23269` [disciplinary_severity]
  - 변경: notes
  - notes: 징계의결이 요구된 근로자에 대한 대기발령은 정당하나 해고는 인정되는 비위행위에 비해 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 
- `id_23289` [misconduct]
  - 변경: notes
  - notes: 이사회 결의의 위법성에 대한 인식 없이 그 결의에 따른 권한을 행사한 것은 징계사유로 삼을 수 없다고 판정한 사례 — 비위행위 존재 및 중대성이
- `id_2329` [disciplinary_severity]
  - 변경: notes
  - notes: 허위사실 유포에 따른 명예훼손, 지시 불이행 등을 이유로 행한 정직 3개월은 부당하다고 보기 어렵고, 부당노동행위에 해당하지 않는다고 판정한 사
- `id_23291` [unfair_treatment]
  - 변경: notes
  - notes: 일부 징계사유가 인정되나 해고에 이를 정도로 중대한 비위행위라고 볼 수 없으며, 부당노동행위로 인정하기도 어렵다고 판정한 사례 — 부당노동행위(

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
