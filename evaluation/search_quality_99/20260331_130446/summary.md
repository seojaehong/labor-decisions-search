# 24-Query Search Evaluation Summary

- Date: 2026-03-31
- Baseline source: `evaluation/rubric_haiku_eval_20260330.md`
- Evaluation runner: `scripts/evaluate_search_24q.py`
- Results JSON: `evaluation/search_quality_99/20260331_130446/results.json`
- Report JSON: `evaluation/search_quality_99/20260331_130446/report.json`

## Headline

- Baseline total score: `165`
- Upgraded total score: `156`
- Delta: `-9`

## Improved Queries

- `Q02`: `6 -> 7`
- `Q03`: `5 -> 6`
- `Q05`: `4 -> 5`
- `Q06`: `8 -> 9`
- `Q08`: `8 -> 9`
- `Q13`: `6 -> 8`
- `Q14`: `8 -> 9`
- `Q22`: `0 -> 7`

## Regressed Queries

- `Q16`: `8 -> 4`
- `Q20`: `6 -> 1`
- `Q17`: `10 -> 8`
- `Q18`: `10 -> 7`
- `Q19`: `8 -> 6`
- `Q12`: `6 -> 4`

## Notes

- The original `search_similar_cases` and `search_similar_cases_hybrid` RPC paths timed out over REST during evaluation.
- This run used a local fallback evaluator:
  - query rewriting
  - embedding generation
  - candidate fetch through `nlrc_decisions` REST reads
  - local hybrid scoring
  - AI reranking
  - Haiku-based top-5 grading
- Because of that fallback, this report is suitable for directional comparison, but it is not yet a production-grade benchmark of the deployed RPC.

## Next Moves

1. Fix RPC timeout at the database layer so the live hybrid path can be evaluated directly.
2. Target low-performing queries:
   - `Q16` contract expiry vs dismissal framing
   - `Q20` violence recognized but dismissal too severe
   - `Q24` composite misconduct holistic dismissal validity
3. Add better candidate expansion for:
   - retaliation after harassment report
   - disciplinary severity without explicit category
   - mixed-misconduct cases with proportionality review
