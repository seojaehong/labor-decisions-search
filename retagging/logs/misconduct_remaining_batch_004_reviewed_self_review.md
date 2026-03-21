# misconduct_remaining_batch_004_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_004_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_11681` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 비위사실로 볼 때 징계양정도 징계권자에게 맡겨진 재량권을 남용하였다고 볼 수 없으며, 징계절차에 하자도 없으므로 해고 처분
- `id_11683` [misconduct]
  - 변경: notes
  - notes: 직무정지는 법률로써 당연히 효력이 발생하는 잠정적인 인사조치로 노동위원회 구제명령의 대상이 아니라고 판정한 사례 — 비위행위 존재 및 중대성이 
- `id_11685` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 
- `id_1169` [unfair_treatment]
  - 변경: notes
  - notes: 인정된 징계 사유에 비해 양정이 과하여 부당한 해고에 해당하나, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개
- `id_11703` [misconduct]
  - 변경: notes
  - notes: 사납금 21만원 미납을 이유로 택시기사를 해고한 것은 그 사유에 비해 지나치게 가혹하여 사용자의 재량권을 일탈·남용한 것으로 부당하다고 판단한 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
