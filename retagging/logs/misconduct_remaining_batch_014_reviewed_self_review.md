# misconduct_remaining_batch_014_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_014_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_17441` [misconduct]
  - 변경: notes
  - notes: 징계사유는 인정되나, 정직 75일의 징계결정은 비위사실에 이른 과실정도에 비해 양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성
- `id_17449` [misconduct]
  - 변경: notes
  - notes: 근로자가 제출한 사직서를 사용자가 수리함으로써 사직서 제출에 따른 근로관계가 종료된 것으로 해고가 아니라고 판정한 사례 — 비위행위 존재 및 중
- `id_17453` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자의 비위행위가 취업규칙상 징계사유에 해당하고, 징계양정이 적정하며 징계절차도 하자가 없어 징계해고가 정당하다고 판정한 사례 — 징계·해고 
- `id_17469` [misconduct]
  - 변경: notes
  - notes: 새로운 비위행위를 사유로 해임하여 일사부재리 원칙에 위배되지 않고, 징계사유가 수년간 지속되어 왔고 이를 사유로 한 해임처분은 양정도 적정하고 
- `id_17479` [misconduct]
  - 변경: notes
  - notes: ‘학력 허위기재’는 징계사유로 인정되나, 근로기간, 업무내용 및 사용자의 피해정도 등을 고려할 때 해고는 양정이 과하여 부당하다고 판정한 사례 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
