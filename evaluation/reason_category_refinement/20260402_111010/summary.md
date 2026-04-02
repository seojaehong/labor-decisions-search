# reason_category 정교화 payload v2

이번 산출물은 `positive + negative + domain gate` 기준으로 생성한 검토용 payload v2입니다.

## probation
- 전체: 3,984
- 유지: 1,774
- 제거 후보: 492
- 검토 필요: 1,718
- 변화량(v2 대비): keep +3 / remove +0 / review -3
- 인정(구제) 전/후: 1,075 -> 445
- 핵심 정의: positive=8 / context=2 / negative=15
- payload: `probation_updates_v3.jsonl`
- samples: `probation_samples_v3.md`

## misconduct
- 전체: 13,758
- 유지: 7,069
- 제거 후보: 290
- 검토 필요: 6,399
- 변화량(v2 대비): keep -34 / remove +0 / review +34
- 인정(구제) 전/후: 3,728 -> 2,142
- 핵심 정의: positive=14 / context=0 / negative=29
- payload: `misconduct_updates_v3.jsonl`
- samples: `misconduct_samples_v3.md`
