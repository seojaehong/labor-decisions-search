# 24-Query Search Evaluation Summary (RPC Direct)

- Date: 2026-03-31
- Runner: `scripts/evaluate_search_24q.py`
- Mode: direct `search_similar_cases_hybrid` RPC first, fallback local scorer only if RPC fails
- Baseline source: `evaluation/rubric_haiku_eval_20260330.md`

## Headline

- Baseline total score: `165`
- Upgraded total score: `163`
- Delta: `-2`

## Strong Improvements

- `Q03`: `5 -> 8`
- `Q06`: `8 -> 9`
- `Q11`: `4 -> 5`
- `Q13`: `6 -> 8`
- `Q17`: `10 -> 10`
- `Q18`: `10 -> 9`
- `Q22`: `0 -> 7`
- `Q24`: `0 -> 6`

## Regressions

- `Q05`: `4 -> 3`
- `Q10`: `8 -> 5`
- `Q16`: `8 -> 6`
- `Q20`: `6 -> 4`
- `Q23`: `8 -> 0`

## Readout

- The direct hybrid RPC path now completes successfully in the evaluation flow.
- The biggest wins are:
  - transport-specific absence (`Q03`)
  - worker-status retrieval (`Q22`)
  - composite misconduct (`Q24`)
- The biggest remaining weakness is harassment-retaliation nuance:
  - `Q23` collapsed
  - `Q05` also weakened
- `Q10` suggests regular employee low-performance dismissal is still not being separated cleanly from broader incompetence/misconduct material.

## Next Fix Targets

1. `Q23`, `Q05`
   - strengthen “괴롭힘 불인정 / 미해당 / 신고 후 갈등 / 불이익 / 전보” expansion and rerank keyword boosts
2. `Q10`
   - improve “정규직 저성과 / 업무능력 부족 해고” candidate shaping
3. `Q20`
   - strengthen “폭행 인정 + 해고 과중” proportionality signals
4. `Q16`
   - contract-expiry vs dismissal framing still needs better distinction
