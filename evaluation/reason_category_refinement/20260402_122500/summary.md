# reason_category 정교화 payload v2

이번 산출물은 `positive + negative + domain gate` 기준으로 생성한 검토용 payload v2입니다.

## probation
- 전체: 3,984
- 유지: 1,466
- 제거 후보: 708
- 검토 필요: 1,810
- 변화량(v2 대비): keep -308 / remove +216 / review +92
- 인정(구제) 전/후: 1,075 -> 384
- 핵심 정의: positive=8 / context=2 / negative=27
- payload: `probation_updates_v4.jsonl`
- samples: `probation_samples_v4.md`

## misconduct
- 전체: 13,758
- 유지: 6,632
- 제거 후보: 278
- 검토 필요: 6,848
- 변화량(v2 대비): keep -437 / remove -12 / review +449
- 인정(구제) 전/후: 3,728 -> 2,027
- 핵심 정의: positive=14 / context=0 / negative=40
- payload: `misconduct_updates_v4.jsonl`
- samples: `misconduct_samples_v4.md`
