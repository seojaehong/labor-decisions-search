# contract_expiry_batch_069_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_069_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_404111` [dismissal_validity]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 이 사건 근로자들은 일용 근로자로서 공정이 종료됨에 따라 근로계약 기간 만료로 근로계약이 종료되어 해고가 존재하지 않는다고 판정한 사례 — 해고
- `id_404125` [renewal_expectation]
  - 변경: notes
  - notes: 기간제근로자에게 정규직 전환 기대권이 존재하나, 정규직 전환 거절의 합리적인 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합
- `id_404139` [dismissal_validity]
  - 변경: notes, secondary:['procedure']→['procedure', 'training_opportunity']
  - notes: 근로자는 영어회화 전문강사로 입사일부터 4년을 초과한 시점에 기간의 정함이 없는 근로자로 전환되었으므로 사용자의 계약기간 만료에 따른 근로관계 
- `id_404149` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity'], conf:high→medium
  - notes: 기간제 근로자들에 대하여 갱신기대권이 인정되고, 갱신거절에 합리적인 이유가 없으므로 부당해고라고 판정한 사례 — discrimination 판단
- `id_404155` [renewal_expectation]
  - 변경: notes
  - notes: 해고가 아니라 계약기간 만료로 근로관계가 종료된 사실이 인정되어 노동위원회의 구제신청을 기각 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
