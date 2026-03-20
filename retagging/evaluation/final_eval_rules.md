# 최종 검색 품질 평가 규칙

## 평가 구조

### 본판정: 24질의 side-by-side blind 비교
- 코덱스 질의셋(representative_queries_v1.json) 24개 사용
- 각 질의별 baseline top-5 vs candidate top-5
- 개별 결과에 2/1/0 relevance 채점
- query-level win/loss/tie 집계

### 보조지표 (자동 산출)
- diversity score: top-5 고유 case_id 비율
- top-1 중복률: baseline/candidate 각각의 질의 간 top-1 반복 비율
- C등급(노이즈) 카운트: Phase 1에서 이미 측정 완료

## Blind 원칙

평가 시 반드시 지킬 것:
1. 각 질의별로 baseline top-5와 candidate top-5의 **소속을 숨김**
2. 10건을 랜덤 순서로 제시하거나, System A / System B로만 표기
3. 평가자는 각 건에 2/1/0만 매기고, 소속은 집계 시 밝힘
4. **"어느 쪽이 새 태그인지" 모르는 상태에서 판단**

blind가 현실적으로 어려우면 (평가자가 1명뿐):
- 최소한 **개별 건 채점 → 집계 → 비교** 순서 유지
- "baseline 5건 보고 → candidate 5건 보고 → 비교"는 금지 (순서 편향)

## Relevance 판정 기준

| 점수 | 의미 | 기준 |
|------|------|------|
| **2** | highly relevant | 질의의 핵심 쟁점과 사건의 실질 판단구조가 직접 일치. 실무자가 바로 인용 가능 |
| **1** | partially relevant | 같은 주제군이지만 핵심 판단구조가 다름. 배경 지식으로 유용 |
| **0** | not relevant | 질의 의도와 무관하거나 명백한 노이즈 |

판정 원칙:
- 표면 키워드 일치보다 **실제 판단구조** 우선
- 배경사실만 같으면 0 또는 1
- exclusion에 해당하는 사건은 원칙적으로 0

## 정량 지표

### 1. Precision@5
`(relevance >= 1인 건수) / 5`

### 2. Weighted Relevance Score@5
`sum(relevance_i), i=1..5` (범위: 0~10)

### 3. First Relevant Rank
처음으로 relevance >= 1이 나온 순위 (1~5, 없으면 NR)

### 4. Query-level Win/Loss/Tie
1순위: weighted score 높은 쪽 승
2순위: precision 높은 쪽 승
3순위: first relevant rank 낮은 쪽 승
모두 동일: tie

### 5. Diversity Score (보조)
`(고유 case_id 수) / (총 결과 수)` — 전체 질의 합산 기준

### 6. Top-1 중복률 (보조)
`(동일 case_id가 top-1로 나온 질의 수) / (전체 질의 수)` — 낮을수록 좋음

## B단계 Go/No-Go 기준

### Go 조건 (4개 중 3개 이상 충족)

| 조건 | 기준 |
|------|------|
| win/loss 승률 | candidate가 **16/24 이상 승리** (2/3+) |
| regression | candidate 패배 **2건 이하** |
| diversity 개선 | candidate diversity가 baseline 대비 **1.5배+ 증가** |
| top-1 중복률 감소 | baseline 대비 **50%+ 감소** |

### Conditional (부분 반영 검토)
- 승률 12~15/24
- regression 3~4건
- 특정 주제에서만 효과

### No-Go
- 승률 12/24 미만
- regression 5건+
- diversity 악화

### Stop
- candidate가 baseline보다 전반적으로 나쁨
- 같은 주제 내에서 regression이 반복

## 해석 시 주의

1. "candidate가 이겼다"는 것이 "태그가 좋다"와 같지 않음. 검색 로직(스코어링 가중치)이 달라서 이긴 것일 수 있음
2. baseline이 특정 질의에서 0건(해당 reason_category가 merged에 없음)이면 해당 질의는 비교 대상에서 제외
3. 단일축 질의에서만 이기고 복합/자연어에서 지면 실제 UX 개선은 제한적
4. Phase 1에서 확인된 "baseline top-1 반복" 현상이 Phase 2에서도 확인되면, 이것 자체가 가장 강한 개선 근거

## 산출물

평가 완료 후 생성할 것:
1. `offline_eval_scored.md` — 24질의 × 채점 결과
2. `eval_summary.md` — 집계 + go/no-go 판정
3. `diversity_analysis.md` — 보조지표 분석
