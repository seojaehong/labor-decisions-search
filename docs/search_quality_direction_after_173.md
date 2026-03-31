# Search Quality Direction After 173

작성일: 2026-03-31

## 현재 상태

- 최신 24-query 평가: `173`
- 기준선: `165`
- 총점은 상승했지만, `Q23`, `Q16`, `Q05`, `Q20` 같은 "의도 조합형" 쿼리는 여전히 약함
- 현재 파이프라인:
  - query rewriting
  - hybrid RPC
  - metadata boost
  - AI reranking

## 방향 판단 표

| 영역 | 계속 밀기 | 이유 | 방향 전환/보강 필요 | 이유 |
| --- | --- | --- | --- | --- |
| Query rewriting | 예 | 총점 상승에 직접 기여했고, 약한 쿼리도 검색어 정규화 품질이 좋아짐 | 부분 보강 필요 | 단일 `category`만으로 복합 의도를 표현하기 어려움 |
| Hybrid RPC | 예 | 실제 RPC가 살아났고 text-only보다 표현력이 좋음 | 후보군 전략 개선 필요 | 어려운 쿼리는 rerank 전 후보군이 이미 빗나감 |
| Metadata boost | 예 | Q22, Q24, Q13, Q14 같이 명시적 패턴은 효과가 큼 | 무한 확장 금지 | boost만 계속 붙이면 유지보수와 false positive가 커짐 |
| AI reranking | 예 | top 후보 재정렬에는 분명 효과가 있음 | 1차 해법은 아님 | 후보군이 틀리면 rerank가 구해주지 못함 |
| 카테고리 기반 검색 | 유지 | DB 카테고리와 reason_category는 여전히 유용함 | intent layer 추가 필요 | `괴롭힘 불인정`, `신고 후 보복`, `사실상 해고`, `양정과다`는 category 하나로 부족 |
| 약한 쿼리 대응 방식 | 일부 유지 | 키워드/부스트는 빠른 응급처치엔 좋음 | retrieval 분기 필요 | Q23/Q16/Q20은 "조건 결합형"이라 시나리오 분기가 더 적합 |
| 평가 방식 | 유지 | 같은 24-query 하네스로 전후 비교 가능 | 세부 진단 추가 필요 | 약한 쿼리는 top20 후보군 단계에서 왜 빗나가는지 별도 로그가 필요 |

## 결론

현재 방향은 맞다. 다만 다음 단계는 `부스트 몇 개 더 추가`가 아니라, **어려운 쿼리군을 위한 시나리오별 retrieval 분기**로 전환해야 한다.

## 우선순위 계획

### P1. 의도(intent) 보조 레이어 추가

대상 쿼리군:

- `retaliation_after_report`
- `bullying_not_recognized`
- `severity_excessive`
- `constructive_or_practical_dismissal`
- `improvement_opportunity_after_warning`

적용 방식:

- rewrite 결과에 `intent`를 더 안정적으로 부여
- RPC 전 후보군 검색 전에 intent별 키워드 집합 생성
- 기존 category는 유지하되, category만으로 검색 범위를 고정하지 않음

### P2. Scenario-specific candidate retrieval 추가

우선 구현 대상:

1. `Q23` 계열
   - `workplace_bullying`
   - `불인정/미해당`
   - `신고/요구/문제제기 이후`
   - `갈등/불이익/보복`
   위 조합을 만족하는 후보를 별도 CTE 또는 app-side 후보셋으로 만들기

2. `Q16` 계열
   - `contract_expiry`
   - `갱신거절`
   - `사실상 해고/실질적 해고/부당해고 다툼`

3. `Q20` 계열
   - `violence`
   - `징계사유는 있음`
   - `해고는 과중/양정과다`

### P3. Retrieval 디버그 로그 추가

약한 쿼리 5개에 대해 아래를 남긴다.

- rewrite 결과
- hybrid top20 raw 후보
- boost 적용 전/후 정렬 차이
- rerank 전/후 top5

산출물 위치:

- `evaluation/search_quality_99/debug/`

### P4. Metadata boost는 최소 보강만

계속 추가할 항목:

- `괴롭힘 불인정|미해당`
- `신고 후 불이익|보복`
- `사실상 해고|실질적 해고`
- `양정과다|해고 과중`

하지 않을 항목:

- 카테고리마다 무제한 정규식 추가
- holding_summary 전체 텍스트에 대한 과도한 패턴 매칭

## 바로 실행할 작업

1. retrieval 경로에 `intent-aware candidate expansion` 추가
2. 약한 쿼리 전용 debug artifact 생성
3. 24-query 재평가 재실행

## 이번 단계의 성공 기준

- `Q23`가 더 이상 바닥 점수에 머물지 않을 것
- `Q16`, `Q20`, `Q05` 중 최소 2개는 분명한 개선이 있을 것
- 전체 총점은 `173` 이상 유지하면서 상승할 것
