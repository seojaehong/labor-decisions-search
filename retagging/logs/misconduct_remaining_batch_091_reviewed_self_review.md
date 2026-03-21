# misconduct_remaining_batch_091_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_091_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_411549` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고, 징계양정이 적정하며, 징계절차상 하자가 없으므로 해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵
- `id_411555` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하지 않으므로 해고가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_411561` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 양정이 재량권을 일탈ㆍ남용하지 않았으며, 절차도 적법하여 기각 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접
- `id_411569` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 무단결근 2일 등 징계사유는 존재하나 사회통념상 고용관계를 계속할 수 없을 정도로 중대하다고 볼 수 없어 징계양정이 과도하다고 판정한 사례 — 
- `id_411581` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 승강기 안전 검사 업무 소홀로 중대재해를 발생시킨 비위행위에 대한 징계해고가 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
