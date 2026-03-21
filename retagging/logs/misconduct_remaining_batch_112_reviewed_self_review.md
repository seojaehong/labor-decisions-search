# misconduct_remaining_batch_112_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_112_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_47959` [unfair_treatment]
  - 변경: notes
  - notes: 감봉 3월의 징계처분은 징계사유가 인정되지 않아 부당하고, 사용자의 부당노동행위 의사를 확인할 만한 특별한 사정이 없어 불이익 취급 및 지배·개
- `id_47965` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 존재하고 징계절차에 하자가 없으나, 정직 2월의 징계는 징계사유에 비해 양정이 과하여 부당하다고 판정한 사례 — 비위 인정이
- `id_47969` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 인정되고 징계절차가 적법하나 징계양정이 과하여 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부
- `id_4797` [disciplinary_severity]
  - 변경: notes
  - notes: 무단결근, 수차례 사직통보, 부당지시, 업무보고 지시 불이행 등의 징계사유가 인정되고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당한 징
- `id_47977` [disciplinary_severity]
  - 변경: notes
  - notes: 근무시간 외 사업장 밖에서 벌어진 사건이라 하더라도 회사 내 공식 조직에 해당하는 노사협의회 회식 자리의 연장선상에서 근로자위원으로서의 신분을 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
