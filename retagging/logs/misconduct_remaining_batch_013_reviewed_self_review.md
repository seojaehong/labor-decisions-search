# misconduct_remaining_batch_013_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_013_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_16839` [disciplinary_severity]
  - 변경: notes
  - notes: 사실상 무기한의 대기발령은 인사권의 남용으로 부당하며, 법인카드 사용 부적정 등 징계사유 중 일부는 인정되나, 인정되는 징계사유에 비해 징계양정
- `id_16841` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자의 비위행위의 정도가 중하여 고용관계를 계속할 수 없을 정도에 이르렀다고 판단되어 해고처분이 정당하다고 판정한 사례 — 징계·해고 절차 하
- `id_16859` [unfair_treatment]
  - 변경: notes
  - notes: 버스 운전기사에게는 운행상 고도의 주의의무가 부여되므로 고의 지연운행 및 무단 배차결행 등을 사유로 해고한 것은 정당하다고 판정한 사례 — 부당
- `id_16871` [disciplinary_severity]
  - 변경: notes
  - notes: 연구비 부적정 집행 등 징계사유는 인정되나, 인정되는 징계사유에 비해 징계양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성
- `id_16875` [unfair_treatment]
  - 변경: notes
  - notes: 교통사고, 보수교육 거부, 지시 불이행 등을 이유로 한 정직 2월의 징계는 정당하고, 불이익취급의 부당노동행위가 아니라고 판정한 사례 — 부당노

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
