# sexual_harassment_batch_011_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_011_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_40937` [misconduct]
  - 변경: notes
  - notes: 성희롱의 징계사유가 존재한다고 인정할 수 없어 부당징계로 판정한 사례 — 비위사실 자체의 입증 여부가 결론을 좌우
- `id_409459` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고 징계양정이 징계재량권 범위 내에 있으며 징계절차도 적법하여 정직처분이 정당하다고 판정한 사례 — 징계양정(제재 수위)의
- `id_409559` [misconduct]
  - 변경: notes
  - notes: 이 사건 사용자가 이 사건 근로자에게 행한 유급휴직 전환 지연 및 이에 따른 임금 지연지급 등은 직장 내 성희롱 피해자에 대한 불리한 처우에 해
- `id_409625` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 양정이 적정하며 절차상 하자도 없다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우
- `id_409629` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 존재하지 않아 부당견책에 해당한다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정을 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
