# misconduct_remaining_batch_069_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_069_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_400955` [misconduct]
  - 변경: notes
  - notes: 사용자는 근로자의 실질적인 사용자로서 당사자 적격이 인정되고, 해고가 존재하나 해고사유가 없고 해고절차에 하자가 있어 부당하다고 판정한 사례 —
- `id_400957` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고 징계양정이 적정하나 징계절차에 중대한 하자가 있어 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_400969` [unfair_treatment]
  - 변경: notes
  - notes: 일부 인정되는 징계사유만으로는 사회통념상 타당성을 잃어 징계권자에 맡겨진 징계재량권을 일탈？남용하였다고 볼 수 있으나, 징계처분이 사용자의 부당
- `id_400977` [misconduct]
  - 변경: notes
  - notes: 근로자의 해외 체류 사유로 한 징계는 병가 목적 외 사용이라고 단정하기 어려워 징계사유가 정당하다고 보기 어렵고, 양정도 타당하다고 보기 어려워
- `id_400991` [misconduct]
  - 변경: notes
  - notes: 학교법인 행정직 근로자로서 용역계약을 부적절하게 수행한 일부 징계사유는 인정되나, 인정되는 징계사유에 비하여 정직 3월의 징계양정은 과도하여 부

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
