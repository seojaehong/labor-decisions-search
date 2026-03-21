# misconduct_remaining_batch_010_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_010_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_15003` [unfair_treatment]
  - 변경: notes, conf:medium→high
  - notes: 택시운전기사가 다수의 교통사고를 발생시킨 행위에 대해 승무정지 25일의 징계처분을 한 것은 정당하고, 부당노동행위도 아니라고 판정한 사례 — 부
- `id_15029` [dismissal_validity]
  - 변경: notes
  - notes: 근로자와 사용자간의 근로계약관계는 사직서 제출과 수리에 의한 합의해지에 따라 종료된 것으로 보이므로 해고가 존재하지 않는다고 판정한 사례 — 해
- `id_15033` [misconduct]
  - 변경: notes
  - notes: 근로자가 비위를 저질러 정당한 대기발령 사유가 있더라도 합리적 이유없이 종기를 정하지 않은 채 장기간의 대기발령조치를 한 행위는 부당하다고 판정
- `id_15043` [unfair_treatment]
  - 변경: notes
  - notes: 근로자들의 행위가 징계사유에 해당하고 징계양정도 적정하여 정당한 징계처분이며, 불이익 취급 및 지배·개입의 부당노동행위로 보기 어렵다고 판정한 
- `id_15049` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 절차에 있어서도 징계 자체를 무효로 할 정도로 흠결이 있다고 보기 어려워 징계해고가 정당하다고 판정한 사례 — 비위행위 존

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
