# probation_batch_016 Self-Review

## 배치 개요
- 입력: `C:/dev/labor-decisions-search/retagging/input/batches/probation_batch_016.jsonl` (30건)
- 출력: `C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_016_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 주요 분류 포인트

### 본채용 거부/수습해지 정당 사례
- id_31867, id_31893, id_31991, id_32003, id_32113, id_32189, id_32441, id_32517, id_32603, id_32847, id_3285, id_32853, id_32941

### 비수습 또는 probation 밖으로 보정한 사례
- id_31883, id_32071, id_32081, id_32245, id_32455, id_32575, id_32741, id_32895

### primary 선택이 흔들렸던 사례
- `id_31867`, `id_31991`, `id_3285`: 평가/증거 부족이 중심이라 `dismissal_validity`로 두고 `evaluation`과 `training_opportunity`를 보조 태그로 뒀다.
- `id_32003`, `id_32359`, `id_32615`, `id_32941`: 단순 평가 미달보다 태도·안전·지시불이행이 강해 `misconduct` 또는 `work_ability`로 나눴다.
- `id_32209`, `id_32223`: 징계양정과 경고 처분이 함께 보여 `disciplinary_severity`를 primary로 유지했다.
- `id_32455`, `id_32741`: probation이 아니라 계약갱신 기대권이 중심이라 `renewal_expectation`으로 정리했다.
- `id_32575`: `at-will` 조항만으로 수습이 성립하지 않아 `worker_status`를 primary로 보정했다.

## rejection vs termination 구분

- `rejection_of_regular_employment`: `id_31867`, `id_31893`, `id_31991`, `id_32033`, `id_32113`, `id_32189`, `id_32441`, `id_32517`, `id_32603`, `id_32847`, `id_3285`, `id_32853`
- `probation_termination`: `id_32003`, `id_32359`, `id_32615`, `id_32941`
- `dismissal`: `id_31883`, `id_32071`, `id_32339`, `id_32575`, `id_32591`, `id_32623`, `id_32705`, `id_32895`
- `no_formal_disposition` / `nonrenewal` / `contract_termination`: `id_32081`, `id_32245`, `id_32455`, `id_32741`

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 모두 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`

## 메모
- warning 성격의 처분은 `reprimand` 또는 `pay_cut`로 정규화해 기록했다.
- 수습이 끝난 뒤의 해고는 `unrelated_to_probation`을 함께 두어 probation 노이즈를 줄였다.
- 계약만료와 갱신기대권 사건은 probation과 분리해 `fixed_term` / `renewal_stage`로 보정했다.
