## Search Quality Next Steps After 204

### Current Best State

- Latest best single-run score: `204`
- Artifact:
  - `evaluation/search_quality_99/20260401_125657/report.json`
  - `evaluation/search_quality_99/20260401_125657/summary.md`

### What Is Already Strong Enough

1. Phase 1
   - sanction / transport / improvement-opportunity metadata boost
2. Phase 2
   - hybrid RPC with vector + trigram candidate merge
3. Phase 3
   - AI query rewriting
   - intent-aware retrieval expansion
   - AI reranking
4. New retrieval branches
   - `constructive_dismissal`
   - `bullying_conflict`
   - `compound_misconduct`

### Remaining Structural Weak Spots

#### Q23: 괴롭힘 불인정 + 신고 후 갈등

현재도 좋아졌지만, 아직 `괴롭힘이 인정된 일반 사건`이나 `전보 일반론 사건`이 섞일 수 있습니다.

다음 개선은 retrieval 부스트 추가보다, DB/태깅 쪽 구조화가 더 효과적입니다.

- 후보 fact marker
  - `harassment_not_recognized`
  - `harassment_report_filed`
  - `post_report_personnel_action`
  - `separation_measure`

#### Q20: 폭행은 있었지만 해고는 과중

지금은 `violence + severity_check` 조합으로 간접적으로 찾고 있습니다. 하지만 실제로는 `폭행 인정`과 `양정과다`가 동시에 구조화되어 있어야 더 안정적으로 올라옵니다.

- 후보 fact marker
  - `violence_recognized`
  - `discipline_recognized_but_excessive`
  - `proportionality_issue`

### Recommended Order

1. 현재 best run(`204`)를 기준선으로 고정
2. `Q23`, `Q20`용 fact marker 설계
3. marker를 `nlrc_decisions` 보강 파이프라인 또는 RPC metadata boost에 반영
4. 24-query 평가 3~5회 반복 실행으로 평균 확인

### What Not To Do Next

- 같은 프롬프트를 계속 길게 늘리기
- generic keyword boost만 더 많이 쌓기
- `Q23`을 `union_activity` 일반론으로 덮어버리는 broad fetch 확대

이제부터는 미세조정보다 `구조화된 신호 추가`가 더 큰 개선을 가져올 가능성이 큽니다.
