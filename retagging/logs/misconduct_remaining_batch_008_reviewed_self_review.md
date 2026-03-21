# misconduct_remaining_batch_008_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_008_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_13771` [disciplinary_severity]
  - 변경: notes
  - notes: 불특정 다수인이 볼 수 있는 민원 등을 수차례 제기한 것을 사유로 출근정지 3월 처분한 것은 정당하다고 판정한 사례 — 징계양정(제재 수위)의 
- `id_13787` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 일부는 인정되나, 근로자에게 비위행위 관련 결정적 책임이나 고의성이 없어 파면처분은 징계양정이 과하다고 판정한 사례 — 징계양정(제재 
- `id_13795` [misconduct]
  - 변경: notes
  - notes: 기타 불량한 근무수행의 징계사유가 인정되고, 징계양정 또한 적정하여 정당한 정직이라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 
- `id_13809` [misconduct]
  - 변경: notes
  - notes: 근로자의 과실로 발생한 교통사고 등을 이유로 징계한 것은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_1381` [unfair_treatment]
  - 변경: notes
  - notes: 징계는 인정되는 징계사유에 비하여 양정이 과하여 부당하고, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
