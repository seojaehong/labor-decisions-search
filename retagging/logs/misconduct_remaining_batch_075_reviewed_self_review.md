# misconduct_remaining_batch_075_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_075_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_403817` [misconduct]
  - 변경: notes
  - notes: 인사명령에 불응하고 5일간 무계결근한 사실이 확인되어 징계사유로 인정되고, 정직 2개월의 징계처분이 정당하다고 판정한 사례 — 비위행위 존재 및
- `id_403821` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자들이 교구ㆍ기관 편성에 따르지 않고 교단총회의 지시에 불응하는 등의 비위행위가 교회 정관이 정한 파면사유에 해당하지 않고, 중대한 절차적 
- `id_403825` [misconduct]
  - 변경: notes
  - notes: 업무소홀 등의 징계사유가 일부 인정되는 사안에서, 정직의 중징계가 양정이 과하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접
- `id_403833` [misconduct]
  - 변경: notes
  - notes: 보안프로그램 미설치의 징계사유가 일부 인정되나 징계양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_403841` [procedure]
  - 변경: notes
  - notes: 징계사유가 일부만 인정되고, 인정되는 징계사유에 비하여 징계양정이 과도하여 징계해고가 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
