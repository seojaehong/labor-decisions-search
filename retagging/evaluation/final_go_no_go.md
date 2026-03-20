# Final Go/No-Go Decision

## 결론

`GO`

신규 8축 태그(candidate)를 구현/연결 트랙으로 진행한다.

## 기준 문서

- 보조지표 공식 기준:
  - `retagging/evaluation/dry_run_24q/24q_prejudgment_metrics.md`
- 실행 가이드:
  - `retagging/evaluation/phase2_execution_guide.md`
- 1차 점수 집계:
  - `retagging/evaluation/dry_run_24q/24q_scored_summary.md`
- 1차 집계 요약:
  - `retagging/evaluation/dry_run_24q/24q_assistant_eval_summary.md`

## 공식 보조지표

- baseline diversity ratio: `0.49`
- candidate diversity ratio: `0.95`
- baseline top-1 duplicate rate: `0.542`
- candidate top-1 duplicate rate: `0.0`

해석:

- candidate는 baseline보다 훨씬 다양한 결과를 반환한다
- baseline의 반복 top-1 문제는 candidate에서 사실상 제거됐다

## 판정 근거

1. 구조적 개선이 명확하다

- diversity가 `0.49 -> 0.95`로 증가했다
- top-1 duplicate rate가 `0.542 -> 0.0`으로 감소했다

2. dry-run 기준 relevance 집계도 candidate 우세 신호가 강하다

- candidate weighted relevance total: `219`
- baseline weighted relevance total: `112`
- candidate win: `23/24`
- baseline win: `0/24`
- tie: `1/24`

3. 운영 판단

- baseline reason_category 경로는 회귀 기준선으로 유지할 가치가 있다
- 하지만 실제 검색 품질 개선 후보는 candidate 8축 태그 쪽이 더 강하다
- 따라서 다음 단계는 "덮어쓰기"가 아니라 "병행 연결 + 비교 가능 상태"로 구현하는 것이 타당하다

## 다음 단계

다음 작업 트랙은 구현/연결 트랙으로 전환한다.

우선순위:

1. `merged_final_v1.jsonl`를 서비스 투입 기준본으로 고정
2. DB 반영 구조 확정
3. 적재 파이프라인 dry-run -> apply 준비
4. baseline/candidate 병행 검색 경로 추가

## 운영 원칙

- 기준 데이터는 반드시 `retagging/output/merged/merged_final_v1.jsonl`
- reviewed 개별 배치 결과를 서비스 기준본으로 직접 사용하지 않음
- baseline(reason_category)는 유지
- candidate(8축 태그)는 병행 경로로 먼저 연결
- 최종 전환은 compare 결과를 본 뒤 결정
