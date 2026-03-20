# Offline Retrieval Evaluation Design

## 목적

이 패키지는 다음 두 검색 체계를 같은 질의셋으로 비교하기 위한 오프라인 평가 프레임이다.

- baseline: 기존 `reason_category` 기반 검색
- candidate: 신규 8축 태그 기반 검색

현재 단계의 목적은 "새 태그가 더 좋다"를 주장하는 것이 아니라, "좋아졌는지 반복 가능하게 검증할 구조"를 만드는 것이다.

## 비교 대상

### Baseline

현재 서비스에서 사용 중인 `reason_category` 배열 검색.

- 예: `absence`, `violence`, `probation`, `workplace_bullying`, `transfer`, `contract_expiry`
- 구현 기준 참고:
  - [retrieval.ts](C:\dev\labor-decisions-search\src\lib\ai\retrieval.ts)
  - [page.tsx](C:\dev\labor-decisions-search\src\app\search\page.tsx)

### Candidate

신규 재태깅 merged JSONL의 다축 필드 기반 검색.

이번 오프라인 평가에서 candidate 검색축은 아래 8개로 고정한다.

1. `employment_stage`
2. `issue_type_primary`
3. `issue_type_secondary`
4. `disposition_type`
5. `fact_markers`
6. `legal_focus`
7. `industry_context`
8. `exclusion_flags`

참고:
- `include_for_queries`, `exclude_for_queries`, `summary_short`, `holding_summary`는 랭킹 보조 신호로만 사용 가능
- core comparison은 위 8축 매칭 성능 중심으로 본다

## 평가 단위

평가 단위는 `query`다.

각 query마다 다음 두 결과를 나란히 비교한다.

- baseline top-k
- candidate top-k

기본 비교 컷은 `top-5`로 고정한다.

필요시 보조 확인용으로 `top-10`을 열람할 수 있지만, 공식 score 계산은 `top-5` 기준으로 한다.

## relevance 판정 기준

사람이 각 결과 문서를 보고 `2 / 1 / 0`으로 판정한다.

- `2 = highly relevant`
  - 질의의 핵심 쟁점과 사실구조가 직접 맞는다
  - 예: "수습 본채용 거부 정당성" 질의에 `probation + dismissal_validity + rejection_of_regular_employment`
- `1 = partially relevant`
  - 같은 주제군이나 일부 쟁점은 맞지만, 핵심 판단구조가 다르다
  - 예: "괴롭힘 성립 여부" 질의에 괴롭힘이 배경이고 실제 핵심은 징계양정인 사건
- `0 = not relevant`
  - 주제 또는 핵심 판단구조가 질의와 실질적으로 맞지 않는다

판정 원칙:
- 표면 키워드 일치보다 실제 판단구조를 우선한다
- 배경 사실만 같은 경우는 `1` 또는 `0`으로 낮춘다
- 검색 의도와 정반대 exclusion이 걸린 사건은 원칙적으로 `0` 또는 낮은 `1`

## 비교 지표

각 query마다 다음 4개 지표를 계산한다.

### 1. Precision@5

`top-5` 중 relevance가 `1` 또는 `2`인 결과 비율.

공식:

`precision@5 = (relevance >= 1 인 문서 수) / 5`

### 2. Weighted Relevance Score@5

상위 5개 결과의 relevance 총합.

공식:

`weighted_score@5 = sum(relevance_i), i=1..5`

범위:
- 최소 `0`
- 최대 `10`

이 지표는 `2점짜리 진짜 정답`을 더 높게 반영한다.

### 3. First Relevant Rank

처음으로 relevance `>= 1`이 나온 순위.

- relevant 결과가 없으면 `NR`
- 숫자가 낮을수록 좋음

권장 기록:
- `1`, `2`, `3`, `4`, `5`, `NR`

### 4. Query-level Win/Loss/Tie

query별로 baseline과 candidate를 직접 비교한다.

기본 판정 순서:

1. `weighted_score@5`가 높은 쪽 승
2. 동점이면 `precision@5`가 높은 쪽 승
3. 그것도 동점이면 `first relevant rank`가 낮은 쪽 승
4. 모두 동일하면 `tie`

## 질의 유형 구성 원칙

대표 질의셋은 아래를 섞는다.

- 단일축 질의
  - 예: "반복 무단결근 해고"
- 복합축 질의
  - 예: "수습인데 업무능력 부족으로 본채용 거부"
- 자연어형 질의
  - 예: "직장내괴롭힘 신고했다가 불이익 받은 사건 보고 싶다"

반드시 포함할 주제:

- 무단결근
- 직장내괴롭힘
- 수습/본채용거부
- 징계양정
- 갱신기대권
- 전보/대기발령
- 폭행/욕설/비위

## 오프라인 비교 절차

### Step 1. Query set 고정

`representative_queries_v1.json`의 query 목록과 기대 의도를 freeze 한다.

### Step 2. Baseline 결과 추출

기존 DB 또는 기존 서비스 로직에서 각 query별 top-5를 추출한다.

필수 저장 포맷:
- `query_id`
- `system = baseline`
- `rank`
- `case_id`
- `title`
- `reason_category`
- `snippet`

### Step 3. Candidate 결과 추출

`merged_final_v1.jsonl` 기준으로 query별 top-5를 산출한다.

candidate 랭킹은 아래 우선순위를 권장한다.

- `issue_type_primary` exact match
- `employment_stage` exact match
- `disposition_type` exact match
- `issue_type_secondary` overlap
- `fact_markers` overlap
- `legal_focus` overlap
- `industry_context` exact match
- `exclusion_flags` penalty
- `include_for_queries` phrase bonus
- `exclude_for_queries` phrase penalty

### Step 4. Side-by-side 평가표 작성

각 query에 대해 baseline과 candidate 결과를 나란히 배치한다.

평가자는 각 결과에 `2/1/0`을 기록하고, score를 합산한다.

### Step 5. Aggregate summary 작성

최종 요약은 아래 3단계로 본다.

- 전체 win/loss/tie
- 주제군별 win/loss/tie
- 실패 query의 패턴 분석

## 해석 가이드

candidate가 개선이라고 보려면 최소한 아래 중 다수를 만족해야 한다.

- `weighted_score@5` 평균이 baseline보다 높다
- `first relevant rank`가 더 빠르다
- 복합 질의에서 baseline보다 명확하게 낫다
- "배경 사실만 같은 노이즈"가 줄어든다

반대로 아래 현상이 보이면 candidate 개선이라고 말하면 안 된다.

- 단일축 질의만 좋아지고 복합 질의가 악화
- 괴롭힘/무단결근처럼 배경 사건이 많은 주제에서 노이즈가 그대로
- 상위 1개는 좋아졌지만 top-5 전체 precision이 나빠짐

## 이번 단계의 산출물

- 평가 설계 문서: 이 파일
- 대표 질의셋: `representative_queries_v1.json`
- 비교 템플릿: `comparison_template.md`
- 오프라인 비교 초안 스크립트: `scripts/offline_reason_vs_tag_eval.py`

## 다음 단계

이 패키지를 만든 뒤 해야 할 일은 아래다.

1. baseline top-5를 실제 DB/사이트에서 export
2. candidate top-5를 merged JSONL에서 생성
3. 사람 판정
4. query별 win/loss/tie 집계
5. 개선 여부 판단
