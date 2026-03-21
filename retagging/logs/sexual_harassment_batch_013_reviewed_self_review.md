# sexual_harassment_batch_013_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_013_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_42653` [disciplinary_severity]
  - 변경: notes, secondary:['procedure']→['misconduct', 'procedure']
  - notes: 다수의 피해자에게 성희롱 및 성추행을 한 공영방송사 관리자에 대한 해고처분이 과하지 않다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심
- `id_42755` [unfair_treatment]
  - 변경: notes
  - notes: 징계 사유가 인정되고, 징계 양정도 적정하며, 징계 절차에도 하자가 없어 정당한 해고라고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부
- `id_42777` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 인정되고, 사용자의 재량권을 벗어난 과도한 징계로 보이지 않으며, 징계절차상 하자도 없어 징계해고처분이 정당하다고 판정
- `id_42819` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 폭언 및 성희롱 등 징계사유는 모두 정당한 징계사유로 인정되고, 비위행위의 양태, 피해자가 다수인 점 등을 고려하면 해임 처분의 양정은
- `id_4287` [misconduct]
  - 변경: notes
  - notes: 감봉 3개월 처분 건은 이 사건 사용자가 처분을 취소하고 임금차액분을 지급하였으므로 구제이익이 소멸되었고, 성희롱 예방교육 이수 건 등은 구제대

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
