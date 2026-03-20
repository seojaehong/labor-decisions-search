# 24-Query Pre-Judgment Metrics

주의: `precision@5`, `weighted relevance score@5`, `first relevant rank`, `win/loss/tie`는 사람 relevance 입력 후 확정한다.
이 문서의 수치는 dry-run 단계에서 자동 계산 가능한 지표만 포함한다.

| query_id | topic | baseline diversity ratio | candidate diversity ratio | top-1 overlap | baseline top1 case | candidate top1 case |
|----------|-------|--------------------------|---------------------------|---------------|--------------------|---------------------|
| Q01 | absence | 0.2 | 0.2 | 1 | id_27267 | id_27267 |
| Q02 | absence | 0.2 | 0.4 | 0 | id_2717 | id_33381 |
| Q03 | absence | 0.2 | 0.2 | 1 | id_23381 | id_23381 |
| Q04 | workplace_bullying | 0.6 | 0.2 | 0 | id_38233 | id_406201 |
| Q05 | workplace_bullying | 0.6 | 0.4 | 0 | id_3591 | id_23343 |
| Q06 | workplace_bullying | 0.4 | 0.2 | 0 | id_11717 | id_344935 |
| Q07 | probation | 0.6 | 0.2 | 0 | id_349575 | id_19817 |
| Q08 | probation | 0.2 | 0.4 | 0 | id_40327 | id_23631 |
| Q09 | probation | 0.4 | 0.2 | 0 | id_349649 | id_1373 |
| Q10 | incompetence | 0.4 | 0.2 | 0 | id_40327 | id_17059 |
| Q11 | incompetence | 0.4 | 0.4 | 0 | id_40327 | id_348399 |
| Q12 | disciplinary_severity | 0.2 | 0.2 | 0 | id_29993 | id_24205 |
| Q13 | disciplinary_severity | 0.2 | 0.2 | 0 | id_13989 | id_10913 |
| Q14 | disciplinary_severity | 0.6 | 0.2 | 0 | id_29279 | id_2951 |
| Q15 | contract_expiry | 0.2 | 0.2 | 1 | id_347015 | id_347015 |
| Q16 | contract_expiry | 0.4 | 0.2 | 0 | id_36593 | id_350961 |
| Q17 | transfer | 0.8 | 0.2 | 0 | id_409901 | id_26243 |
| Q18 | transfer | 0.4 | 0.4 | 0 | id_27603 | id_348033 |
| Q19 | violence | 0.4 | 0.2 | 0 | id_2037 | id_24289 |
| Q20 | violence | 0.2 | 0.2 | 1 | id_11561 | id_11561 |
| Q21 | violence | 0.6 | 0.2 | 0 | id_350303 | id_10901 |
| Q22 | worker_status | 0.2 | 0.2 | 0 | id_11225 | id_18475 |
| Q23 | workplace_bullying | 0.4 | 0.2 | 0 | id_399891 | id_12489 |
| Q24 | dismissal_validity | 0.4 | 0.2 | 0 | id_29993 | id_350303 |

## Aggregate Pre-Metrics

- query count: `24`
- top-1 overlap count: `4`
- top-1 overlap ratio: `0.167`
- weighted score / precision / FRR / win-loss-tie: human relevance 입력 후 계산
