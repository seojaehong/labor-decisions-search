# probation_batch_022 Self-Review

## 배치 개요
- 입력: `C:/dev/labor-decisions-search/retagging/input/batches/probation_batch_022.jsonl` (30건)
- 출력: `C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_022_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `work_ability`: 16건
- `worker_status`: 5건
- `dismissal_validity`: 4건
- `procedure`: 3건
- `renewal_expectation`: 1건
- `disciplinary_severity`: 1건

## 수습 vs 비수습 분류
- `probation`: 23건
- `fixed_term`: 4건
- `renewal_stage`: 1건
- `pre_hire`: 1건
- `regular`: 1건

## confidence 낮춘 사례
- `id_347625`: 직장 내 괴롭힘 메일이 평가 이후라 평가와의 직접 연결성이 약하다.
- `id_348301`: 시용기간 연장과 2차 평가 하락의 근거가 충분히 보강되지 않았다.
- `id_348307`: confidence를 `medium`로 낮춰 경계성을 남겼다.
- `id_348371`: holding_points가 상태 인식만 담고 있어 source_text 기준으로 본채용 거부 부당성을 반영했다.

## 주요 경계 사례
- `id_348371`: holding_points와 source_text가 어긋나 source_text를 우선했다.
- `id_348647`: 채용내정 성립 후 취소라 probation보다 pre_hire에 가깝게 정리했다.
- `id_347873`: 감봉과 본채용 거부가 함께 있어 `disciplinary_severity`와 `rejection_of_regular_employment`를 같이 반영했다.
- `id_348705`: 수습 배경이 있지만 실제 결론은 본채용 확정 후 일반해고였다.

## 검증 사항
- review_status: 전건 `pending`
- tag_version: 전건 `v1`
- 필수 필드 19개 전부 포함
- JSONL 형식으로 전수 생성
- validator 경고 0건을 목표로 허용값만 사용

## 메모
- 수습 본채용 거부, 절차 하자, 사직/합의해지, 채용내정, 기간제 만료가 한 배치 안에 섞여 있어 `stage`와 `disposition`을 분리해 기록했다.
- `id_348371`처럼 holding_points가 축약된 건 source_text를 우선했다.
- fixed_term, renewal_stage, pre_hire, regular 사건은 `unrelated_to_probation`으로 분리해 probation batch 노이즈를 줄였다.
