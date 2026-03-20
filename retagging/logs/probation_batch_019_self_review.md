# probation_batch_019 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_019.jsonl`
- 출력: `retagging/output/reviewed/probation_batch_019_reviewed.jsonl`
- 총 30건
- 작업일: 2026-03-20

## 분류 요약
- `dismissal_validity`: 15건
- `work_ability`: 9건
- `renewal_expectation`: 2건
- `worker_status`: 2건
- `disciplinary_severity`: 1건
- `procedure`: 1건

## 수습 vs 비수습 분류
- `probation`: 22건
- `regular`: 5건
- `renewal_stage`: 1건
- `fixed_term`: 1건
- `pre_hire`: 1건

## disposition 분포
- `rejection_of_regular_employment`: 18건
- `dismissal`: 4건
- `no_formal_disposition`: 3건
- `probation_termination`: 2건
- `nonrenewal`: 2건
- `disciplinary_dismissal`: 1건

## 주요 경계 사례
1. `id_344209`, `id_344359`
   - 복직명령이나 종료 의사표시 부재로 merits 판단이 사실상 닿지 않아 `fact_specific_low_reusability` 성격으로 정리했다.
2. `id_344317`, `id_344587`
   - probation 표면 태그보다 갱신기대권과 기간제 구조가 더 강해 renewal 쪽으로 보정했다.
3. `id_344509`
   - 근로조건 합의와 근로제공이 확인되지 않아 근로계약 성립 자체를 부정했다.
4. `id_344699`
   - 사용자 적격과 시용성 판단이 결합된 경계 사례라 `worker_status`를 primary로 두었다.
5. `id_344953`
   - 2차 시용계약과 경미한 사유만으로는 본채용 거부 정당성이 약한 사례로 보았다.
6. `id_344819`
   - 인정되는 비위에 비해 징계해고 양정이 과도한지 본 사건이라 `disciplinary_severity`로 정리했다.
7. `id_344865`
   - 평가자 규정 위반으로 객관적 근무평가가 아니라고 보아 `procedure`로 유지했다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`
- JSONL parse: OK
- enum / 배열값 검증: OK

## 메모
- 평가점수와 수습평가 하자가 드러나는 사건은 `work_ability`와 `procedure`를 함께 살렸다.
- 본채용 거부가 실제로는 수습종료인지, 정규해고인지, 갱신거절인지 먼저 분리했다.
- `no_formal_disposition` 성격 사건은 구제이익 소멸 또는 해고 존부 부정으로 notes에 분명히 남겼다.
