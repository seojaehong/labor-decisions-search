# misconduct_remaining_batch_126_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_126_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_53567` [misconduct]
  - 변경: notes, secondary:['procedure']→['procedure', 'disciplinary_severity']
  - notes: 일부 해고사유가 인정되나, 해고사유에 비하여 양정이 과도하여 부당해고로 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_53569` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유 일부가 인정되고, 인정되는 징계사유만으로도 징계양정이 과하다고 볼 수 없으며, 징계절차에 중대한 하자가 없어 감봉 1월의 징계
- `id_53597` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 다수의 사고를 유발하고 과태료 처분을 받은 사실이 인정되므로 근로자에 대한 승무정지 30일의 징계는 정당하다고 판정한 사례 — 징계양정
- `id_53609` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 정직 1개월의 징계는 사회통념상 현저하게 타당성을 잃은 처분이라고 보기 어려우며 징계절차상 하자가 없으므로 정당하다고 판정한
- `id_5361` [unfair_treatment]
  - 변경: notes
  - notes: 이 사건 근로자들의 징계사유는 인정되나, 인정되는 징계사유가 정직에 이를 정도라고 보기 어려워 정직처분은 부당하나, 정직처분이 사용자의 부당노동

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
