# misconduct_remaining_batch_051_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_051_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_348935` [misconduct]
  - 변경: notes
  - notes: 업무배제는 존재하지 않으며, 대기발령은 불이익이 없고 효력이 상실되어 구제이익이 없다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을
- `id_34895` [disciplinary_severity]
  - 변경: notes
  - notes: 정당한 징계사유로 인정되는 업무태만의 비위에 대해 해고를 제외하고 가장 중한 정직의 징계를 한 것은 양정이 과하여 부당하다고 판정한 사례 — 징
- `id_348963` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당한 징계라고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여
- `id_348975` [misconduct]
  - 변경: notes
  - notes: 대기발령의 필요성은 인정되나, 장기간 대기발령 조치를 유지하는 것은 정당하다고 볼 수 없으므로 부당하다고 판정한 사례 — 비위행위 존재 및 중대
- `id_34899` [disciplinary_severity]
  - 변경: notes
  - notes: 해고처분 시 새로운 강등 및 직책박탈 처분이 있었다고 볼 수 없고, 해고처분은 사회통념상 고용관계를 계속할 수 없을 정도에 이르렀다고 보기 어려

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
