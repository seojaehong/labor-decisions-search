# misconduct_remaining_batch_094_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_094_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_413077` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 사용자의 허가 없이 작업물을 임의로 삭제한 행위, 회사의 자산으로 볼 수 있는 작업물을 외부업체 광고를 삽입하여 개인저장소에 게시한 행
- `id_413079` [misconduct]
  - 변경: notes
  - notes: 사용자가 삼은 업무상 배임 및 횡령에 따른 징계사유가 근로자들의 귀책사유라고 인정할 만한 객관적 자료가 없는 등 징계사유를 인정하기 어려워 해고
- `id_413093` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 존재하고 양정이 적정하며 절차에 하자가 없어 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_4131` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 근로자에 대한 징계 처분은 그 사유가 존재하지 않아 부당하고, 경고 처분은 구제명령의 대상에 해당하지만, 비위행위가 인정되고 비위행위에 비해 처
- `id_413107` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 절차도 적법하나, 징계양정이 과도하여 해고가 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 판정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
