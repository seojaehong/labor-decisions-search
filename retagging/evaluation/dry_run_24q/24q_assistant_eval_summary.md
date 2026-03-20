# 24-Query Assistant Eval Summary

주의: 이 문서는 사람 최종 채점 전, 코덱스가 동일 규칙으로 넣은 1차 assistant dry-run 판정이다.

## Aggregate

- candidate win: `23/24`
- baseline win: `0/24`
- tie: `1/24`
- candidate weighted relevance total: `219`
- baseline weighted relevance total: `112`
- candidate precision proxy: `1.0`
- baseline precision proxy: `0.84`
- baseline diversity ratio: `0.49`
- candidate diversity ratio: `0.95`
- baseline top-1 duplicate rate: `0.542`
- candidate top-1 duplicate rate: `0.0`
- provisional verdict: `GO candidate`

## Interpretation

- candidate가 24질의 중 다수 질의에서 우세하게 나왔다.
- diversity와 top-1 중복률은 사람이 채점하기 전에도 candidate 우세 신호가 강하다.
- 다만 공식 판정은 사람 blind 채점 결과를 우선한다.

## Query-Level Reminder

- 상세 질의별 점수는 `24q_scored_summary.md`를 기준으로 본다.
- 실제 채점 입력 원본은 `24q_assistant_scored_judgments.csv`다.
