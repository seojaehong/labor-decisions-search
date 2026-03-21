# misconduct_remaining_batch_012_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_012_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_16221` [misconduct]
  - 변경: notes, secondary:['unfair_treatment']→['procedure', 'unfair_treatment']
  - notes: 총회 소집 공고규정과 징계절차를 위반한 현장발의 형식의 조합원 제명처분은 「노동조합 및 노동관계조정법」제19조 및 규약 위반으로 무효라고 의결한
- `id_16255` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유에 비해 양정이 과다하여 부당해고인 반면, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵
- `id_16263` [misconduct]
  - 변경: notes
  - notes: 의료인에게 금지된 편의 제공 및 허위 경쟁입찰을 수락한 근로자에 대한 정직 6개월의 처분은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이
- `id_16271` [unfair_treatment]
  - 변경: notes, conf:high→medium
  - notes: 형사상 유죄판결을 사유로 징계해고 한 것은 정당하고, 부당노동행위에 해당하지 않는다고 판단한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 
- `id_16277` [unfair_treatment]
  - 변경: notes
  - notes: 징계양정이 과다하여 부당한 정직에 해당하나, 부당노동행위의 의사가 있었다고 보기는 어렵다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
