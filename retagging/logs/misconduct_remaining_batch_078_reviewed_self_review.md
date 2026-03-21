# misconduct_remaining_batch_078_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_078_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_40527` [misconduct]
  - 변경: notes
  - notes: 비위 행위 중 일부가 존재하나, 사회통념상 고용관계를 유지할 수 없을 정도로 근로자의 책임 있는 사유로 보기 어렵다고 판정한 사례 — 비위행위 
- `id_405271` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 징계사유는 인정되나, 징계양정이 적정하지 않고 징계 절차가 적법하지 않아 부당한 징계에 해당한다고 판정한 사례 — 해고 사실 자체의 존부 또는 
- `id_405277` [misconduct]
  - 변경: notes
  - notes: 경고처분은 구제대상에 해당되나 경고처분의 사유가 인정되고 경고처분 절차도 적정하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직
- `id_405281` [unfair_treatment]
  - 변경: notes
  - notes: 불이익 취급 및 지배ㆍ개입, 단체교섭 해태의 부당노동행위에 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심
- `id_405285` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자들의 '노선 위반’ 징계사유가 인정되고 징계절차도 적법하나, 징계양정이 징계재량권의 일탈 내지 남용에 해당한다고 판정한 사례 — 비위 인정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
