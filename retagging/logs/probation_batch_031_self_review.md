# probation_batch_031 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_031.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_031_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약 (issue_type_primary)
- `work_ability`: 18건
- `dismissal_validity`: 5건
- `procedure`: 3건
- `misconduct`: 1건
- `worker_status`: 1건
- (비수습 제외 2건 포함)

## 수습 vs 비수습 분류
- `probation`: 25건
- `fixed_term`: 2건 (id_400981, id_401669)
- `regular`: 1건 (id_400599)
- `pre_hire`: 1건 (id_401427)
- `unknown`: 1건 — 해당 없음, 전건 분류 완료

### 비수습 사유
- **id_400981**: holding_points에 "시용근로자가 아닌 기간제근로자"로 명시. `unrelated_to_probation` 부여.
- **id_401669**: 근로계약서상 1년 기간제, 업무적격성 평가 조항 부재로 시용근로계약 부정. `unrelated_to_probation` 부여.
- **id_400599**: 수습기간 3개월 이미 경과하여 정규직으로 전환 인정. employment_stage를 `regular`로 설정.
- **id_401427**: 1주일 시험근무 후 채용 거절. 근로계약 미성립. `pre_hire`로 설정, `unrelated_to_probation` 부여.

## rejection vs termination 구분 (disposition_type)
- `rejection_of_regular_employment`: 18건
- `probation_termination`: 3건 (id_40055, id_400551, id_401571)
- `dismissal`: 4건 (id_400599, id_400981, id_401175, id_401669)
- `no_formal_disposition`: 3건 (id_400799, id_401249, id_401427)

### 구분 기준
- **rejection_of_regular_employment**: 수습기간 종료 시점에 평가 기반으로 본채용을 거부한 경우
- **probation_termination**: 수습기간 도중에 해약권을 행사하여 근로관계를 종료한 경우
- **dismissal**: 수습이 아닌 일반 해고이거나, 수습기간 경과 후 정규직 상태에서의 해고
- **no_formal_disposition**: 해고 부존재(사직, 근로계약 미성립 등)

## 주요 경계 사례
- **id_400595**: 수습기간 종료일 면담 후 주말/공휴일로 영업일에 통지. 본채용 거부 인정하되 사유 미기재로 절차 위반.
- **id_400599**: 인턴기간 포함 수습기간 이미 경과 → 정규직 전환 인정. 사직서의 진의 부재 인정.
- **id_400981**: 수습 태그가 있었으나 실제 기간제근로자. employment_stage를 `fixed_term`으로 변경.
- **id_401427**: 1주일 시험근무 후 채용 거절. 근로계약 미성립으로 해고 부존재. `pre_hire`로 분류.
- **id_401571**: 수습 해고와 부당노동행위(불이익취급, 지배개입) 주장이 병합된 사건.
- **id_401599**: 징계해고 vs 본채용 거부 성격 구분이 쟁점. 본채용 거부로 판단.
- **id_401669**: 근로계약서에 수습기간 조항 없이 1년 기간제. 시용근로계약 부정.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`
- exclusion_flags `unrelated_to_probation`: 3건 (id_400981, id_401427, id_401669)
- 비수습 사건 4건 식별 및 적절한 employment_stage 부여
