# reason_category 정교화 payload v5

이번 산출물은 `positive + negative + domain gate + review sub-bucket` 기준으로 생성한 검토용 payload입니다.

## probation
- 전체: 3,984
- 유지: 1,418
- 제거 후보: 774
- 검토 필요: 1,792
- 변화량(v2 대비): keep -48 / remove +66 / review -18
- review 세부분류: {'lean_remove': 569, 'ambiguous': 1100, 'lean_keep': 123}
- 인정(구제) 전/후: 1,075 -> 361
- 핵심 정의: positive=8 / context=2 / negative=6
- payload: `probation_updates_v5.jsonl`
- samples: `probation_samples_v5.md`

## misconduct
- 전체: 13,758
- 유지: 6,892
- 제거 후보: 321
- 검토 필요: 6,545
- 변화량(v2 대비): keep +260 / remove +43 / review -303
- review 세부분류: {'lean_remove': 4376, 'ambiguous': 1924, 'lean_keep': 245}
- 인정(구제) 전/후: 3,728 -> 2,080
- 핵심 정의: positive=14 / context=0 / negative=9
- payload: `misconduct_updates_v5.jsonl`
- samples: `misconduct_samples_v5.md`
