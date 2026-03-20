# 24-Query Pre-Judgment Metrics

주의: `precision@5`, `weighted relevance score@5`, `first relevant rank`, `win/loss/tie`는 사람 relevance 입력 후 확정한다.
이 문서의 수치는 dry-run 단계에서 자동 계산 가능한 지표만 포함한다.

| query_id | topic | baseline diversity ratio | candidate diversity ratio | top-1 overlap | baseline top1 case | candidate top1 case |
|----------|-------|--------------------------|---------------------------|---------------|--------------------|---------------------|
| Q01 | absence | 0.2 | 0.2 | 0 | id_10561 | id_27267 |
| Q02 | absence | 0.2 | 0.4 | 0 | id_10561 | id_33381 |
| Q03 | absence | 0.2 | 0.2 | 0 | id_10561 | id_23381 |
| Q04 | workplace_bullying | 0.6 | 0.2 | 0 | id_10771 | id_406201 |
| Q05 | workplace_bullying | 0.8 | 0.4 | 0 | id_10479 | id_23343 |
| Q06 | workplace_bullying | 0.6 | 0.2 | 0 | id_10479 | id_344935 |
| Q07 | probation | 0.8 | 0.2 | 0 | id_10575 | id_19817 |
| Q08 | probation | 0.8 | 0.4 | 0 | id_10575 | id_23631 |
| Q09 | probation | 0.8 | 0.2 | 0 | id_10575 | id_1373 |
| Q10 | incompetence | 1.0 | 0.2 | 0 | id_13295 | id_17059 |
| Q11 | incompetence | 1.0 | 0.4 | 0 | id_13295 | id_348399 |
| Q12 | disciplinary_severity | 1.0 | 0.2 | 0 | id_10479 | id_24205 |
| Q13 | disciplinary_severity | 1.0 | 0.2 | 0 | id_10479 | id_10913 |
| Q14 | disciplinary_severity | 1.0 | 0.2 | 0 | id_10479 | id_2951 |
| Q15 | contract_expiry | 0.4 | 0.2 | 0 | id_10621 | id_347015 |
| Q16 | contract_expiry | 0.4 | 0.2 | 0 | id_36593 | id_350961 |
| Q17 | transfer | 1.0 | 0.2 | 0 | id_10613 | id_26243 |
| Q18 | transfer | 0.4 | 0.4 | 0 | id_27603 | id_348033 |
| Q19 | violence | 0.4 | 0.2 | 0 | id_2037 | id_24289 |
| Q20 | violence | 0.6 | 0.2 | 0 | id_10479 | id_11561 |
| Q21 | violence | 1.0 | 0.2 | 0 | id_10479 | id_10901 |
| Q22 | worker_status | 0.2 | 0.2 | 0 | id_11225 | id_18475 |
| Q23 | workplace_bullying | 0.6 | 0.2 | 0 | id_10771 | id_12489 |
| Q24 | dismissal_validity | 1.0 | 0.2 | 0 | id_10479 | id_350303 |

## Aggregate Pre-Metrics

- query count: `24`
- cross-system top-1 same-case count: `0`
- cross-system top-1 same-case ratio: `0.0`
- baseline diversity ratio (global): `0.49`
- candidate diversity ratio (global): `0.95`
- baseline top-1 duplicate rate: `0.542`
- candidate top-1 duplicate rate: `0.0`
- weighted score / precision / FRR / win-loss-tie: human relevance 입력 후 계산
