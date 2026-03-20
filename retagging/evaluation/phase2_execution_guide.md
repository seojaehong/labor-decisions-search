# Phase 2 Execution Guide

## 공식 기준

이번 Phase 2 오프라인 평가는 코덱스가 생성한 24질의 dry-run 패키지를 공식 기준으로 사용한다.

보조지표의 공식 숫자는 반드시 아래 문서 하나로 통일한다.

- `retagging/evaluation/dry_run_24q/24q_prejudgment_metrics.md`

다른 세션, 메모, 중간 요약에 있는 숫자는 참고용일 뿐 공식 비교 수치로 인용하지 않는다.

## 현재 공식 dry-run 보조지표

- baseline diversity ratio: `0.49`
- candidate diversity ratio: `0.95`
- baseline top-1 duplicate rate: `0.542`
- candidate top-1 duplicate rate: `0.0`

현재 단계의 해석:

- candidate는 baseline보다 훨씬 다양한 결과를 반환한다
- baseline에서 반복되던 top-1 현상은 candidate에서 사실상 제거됐다
- 다만 최종 결론은 아직 아니다
- 공식 판정은 blind human scoring 이후 확정한다

## 평가 패키지

- blind 비교표:
  - `retagging/evaluation/dry_run_24q/24q_blind_side_by_side.md`
- 사람 채점 템플릿:
  - `retagging/evaluation/dry_run_24q/24q_human_judgment_template.csv`
- blind key:
  - `retagging/evaluation/dry_run_24q/24q_blind_key.json`
- 비공개 top 결과:
  - `retagging/evaluation/dry_run_24q/24q_nonblind_top_results.md`
- 비교 원본 데이터:
  - `retagging/evaluation/dry_run_24q/24q_comparison_data.json`

## 사람 채점 절차

1. `24q_blind_side_by_side.md`를 기준으로 질의별 A/B 결과를 blind 상태에서 검토한다.
2. `24q_human_judgment_template.csv`에 각 결과의 relevance를 `2/1/0`으로 입력한다.
3. 입력이 끝나면 `scripts/score_offline_eval_judgments.py`를 실행한다.
4. 아래 지표를 기준으로 최종 판단한다.

- precision@5
- weighted relevance score@5
- first relevant rank
- query별 win/loss/tie

## relevance 기준

- `2`: highly relevant
  - 질의의 핵심 쟁점과 사건의 실질 판단구조가 직접 일치
- `1`: partially relevant
  - 같은 주제군이지만 핵심 판단구조가 다름
- `0`: not relevant
  - 질의 의도와 무관하거나 명백한 노이즈

판정 원칙:

- 표면 키워드보다 실제 판단구조를 우선한다
- 배경사실만 같으면 `0` 또는 `1`이다
- exclusion 성격의 사건은 원칙적으로 `0`이다

## 운영 원칙

- 지금 단계에서는 "새 태그가 좋아 보인다"를 주장하지 않는다
- 지금 단계의 목적은 "좋아졌는지 검증 가능한 구조"를 유지하는 것이다
- 공식 보고와 판단은 dry-run 패키지와 human scoring 결과만 근거로 삼는다
- 보조지표는 방향성 확인용이고, 최종 go/no-go는 사람 채점 결과까지 포함해 판단한다
