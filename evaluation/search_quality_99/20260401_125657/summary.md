## 24-query Reevaluation Summary

- Baseline total: `165`
- Upgraded total: `204`
- Delta: `+39`
- Duration: `845.31s`

### Overall

이번 라운드는 `Q23`의 `괴롭힘 불인정 + 신고 후 갈등/분리조치` 축과 `Q24`의 `복합비위 종합판단` 축을 retrieval 단계에서 더 직접적으로 끌어올린 뒤 재평가한 결과입니다. 현재까지 나온 단일 실행 기준으로는 가장 높은 총점입니다.

### Focus Query Results

- `Q05`: `4 -> 7`
- `Q10`: `8 -> 8`
- `Q16`: `8 -> 9`
- `Q20`: `6 -> 7`
- `Q23`: `8 -> 6`
- `Q24`: `0 -> 8`

### What Changed

- `Q23`
  - query expansion에 `괴롭힘이 아니라는 조사 결과`, `분리조치`, `접촉금지`, `근무장소 변경`을 추가
  - `bullying_conflict` 시나리오에서 `괴롭힘 인정` 사건을 더 강하게 감점
  - `불인정 조사 결과 + 신고 후 인사조치` 조합을 더 직접적으로 가점
- `Q24`
  - `compound_misconduct` 시나리오를 새로 분리
  - `징계사유가 모두 인정`, `양정이 적정`, `절차상 하자 없음`, `사유 양정 절차` 같은 종합판단 표현을 query expansion에 추가
  - 복수 사유 + 사유/양정/절차 3축 종합판단 구조에 추가 가점
- reranker prompt
  - `불인정/미해당`
  - `여러 비위/복합 비위/정당성 전체`
  맥락을 더 명시적으로 평가하도록 보강

### Interpretation

- `Q24`는 사실상 구조적 약점이 해소된 상태에 가깝습니다.
- `Q16`도 기준선보다 조금 더 나아졌습니다.
- `Q23`은 여전히 완전 회복 전이지만, 상위권에 `불인정 + 신고/분리조치` 사건이 더 안정적으로 들어오기 시작했습니다.
- `Q20`은 유지 또는 소폭 개선 수준이고, 더 큰 점프를 위해서는 `폭행 인정 + 양정과다`를 구조화된 메타데이터로 잡는 쪽이 더 유력합니다.

### Suggested Next Step

다음 단계가 필요하다면, 단순 프롬프트/부스트 추가보다 아래 두 가지가 더 효과적입니다.

1. `Q23`용 구조화 신호 추가
   - `harassment_not_recognized`
   - `post_report_personnel_action`
   - `separation_measure`
   같은 fact marker를 DB 쪽에 별도 보강
2. `Q20`용 구조화 신호 추가
   - `discipline_recognized_but_excessive`
   - `violence_recognized`
   - `proportionality_issue`
   같은 메타 신호를 RPC에서 직접 활용
