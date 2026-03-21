# misconduct_remaining_batch_084_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_084_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_408179` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고, 징계양정도 적정하며, 징계절차에 중대한 하자가 없어 정직 2개월의 징계가 정당하다고 판정한 사례 — 징계양정(제재 수
- `id_408187` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 부정되더라도 인정되는 사유만으로 해고한 것은 징계양정이 적정하고 징계절차도 준수하여 정당하다고 판정한 사례 — 징계양정(제재 수
- `id_408203` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 정당한 징계사유가 인정되고 징계절차에 별다른 하자가 없으나, 징계양정이 형평성을 잃어 징계양정이 과다하다고 판정한 사례 — 징계·해고 절차 하자
- `id_40821` [disciplinary_severity]
  - 변경: notes
  - notes: 견책의 징계는 정당하나, 대기발령은 대기발령사유가 존재하지 않고, 대기발령 기간이 적정하지 않아 부당하다고 판정한 사례 — 비위 인정이나 해고·
- `id_408211` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 공사시공 관리 소홀을 이유로 하는 정직 1월의 징계 처분이 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
