# misconduct_remaining_batch_100_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_100_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_4307` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 가지급금 부당사용과 순자본비율 조작 및 허위공시에 관한 징계사유가 인정되나, 가지급금 부당사용으로 금고가 경제적 손실을 입지 않았고 출
- `id_43075` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유 일부가 인정되나 인정되는 징계사유에 비해 해고는 징계양정이 과도하여 부당한 징계라고 판정한 사례 — 징계양정(제재 수위)
- `id_43099` [disciplinary_severity]
  - 변경: notes
  - notes: 첫째, 절대적 해고금지기간에 해당하는지 여부, 둘째, 징계사유의 존재 여부, 셋째, 징계절차의 적법성 여부, 넷째, 징계양정의 적정성 여부에 있
- `id_43105` [misconduct]
  - 변경: notes
  - notes: 사용자가 근로자에게 징계사유가 존재하지 않는 면직처분을 한 것은 부당해고에 해당한다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 
- `id_43123` [unfair_treatment]
  - 변경: notes
  - notes: 근로자에 따라 일부 인정되는 징계사유에 비하여 처분의 양정이 과다하여 부당하나, 사용자에게 부당노동행위 의사가 존재한다고 보기 어려워 부당노동행

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
