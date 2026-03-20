# Offline Comparison Template

이 템플릿은 query별로 baseline과 candidate를 나란히 놓고 사람이 relevance를 판정하기 위한 기록지다.

## Query Metadata

- `query_id`:
- `query`:
- `query_type`:
- `topic`:
- `baseline_reason_categories`:
- `candidate_profile_summary`:

## Baseline Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

## Candidate Top-5

| rank | case_id | title | why surfaced | relevance (2/1/0) | memo |
|------|---------|-------|--------------|-------------------|------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

## Query-level Summary

- baseline precision@5:
- candidate precision@5:
- baseline weighted relevance score@5:
- candidate weighted relevance score@5:
- baseline first relevant rank:
- candidate first relevant rank:
- win/loss/tie:
- summary memo:

## 판정 메모

- `2`: 질의의 핵심 판단구조와 사실관계가 직접 맞음
- `1`: 주제는 맞지만 핵심 판단구조가 어긋나거나 일부만 맞음
- `0`: 실질적으로 관련 없음

## Aggregate Summary Template

| query_id | baseline p@5 | candidate p@5 | baseline wrs@5 | candidate wrs@5 | baseline FRR | candidate FRR | outcome | memo |
|----------|--------------|---------------|----------------|-----------------|--------------|---------------|---------|------|
| Q01 |  |  |  |  |  |  |  |  |
| Q02 |  |  |  |  |  |  |  |  |
| Q03 |  |  |  |  |  |  |  |  |

권장 outcome 규칙:

- candidate win
- baseline win
- tie

권장 해석:

- 복합 질의에서 candidate win 비율이 높으면 태그 구조 개선 신호
- 단일 질의만 좋아지고 자연어형에서 tie/loss가 많으면 추가 튜닝 필요
