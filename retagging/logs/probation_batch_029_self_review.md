# probation_batch_029 Self-Review

## 배치 개요
- 입력: `C:/dev/labor-decisions-search/retagging/input/batches/probation_batch_029.jsonl` (30건)
- 출력: `C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_029_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `dismissal_validity`: 9건
- `work_ability`: 6건
- `procedure`: 5건
- `worker_status`: 3건
- `renewal_expectation`: 1건
- `disciplinary_severity`: 2건
- `unfair_treatment`: 1건
- `discrimination`: 1건
- `absence_without_leave`: 1건

## 수습 vs 비수습 분류
- `probation`: 26건
- `renewal_stage`: 1건
- `regular`: 2건
- `pre_hire`: 1건

## rejection vs termination 구분
- `rejection_of_regular_employment`: 16건
- `probation_termination`: 1건
- `dismissal`: 5건
- `disciplinary_dismissal`: 2건
- `nonrenewal`: 1건
- `no_formal_disposition`: 5건

## 주요 경계 사례
1. `id_38361`
   - 구두 해고와 서면통지 위반이 결론을 좌우한 절차 사건이다.
2. `id_38433`
   - 갱신기대권이 인정되는 반면 갱신거절의 합리성은 부정된 renewal 사건이다.
3. `id_39041`
   - 근로계약 성립 자체가 부정되어 probation보다 `pre_hire`/`worker_status`가 먼저다.
4. `id_39135`
   - 수습 종료 후 정식근로자에 대한 징계해고 양정 과다 사건이다.
5. `id_39219`
   - 배차거부와 징계해고는 정당하고 부당노동행위 의사도 인정되지 않았다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`
- 로컬 스키마/값 검증: 별도 실행 예정

## 메모
- batch 029는 구두 해고, 본채용 거부, 갱신기대권, 차별시정이 한 묶음에 섞여 있어 primary를 먼저 분리했다.
- probation 외 `renewal_stage`, `regular`, `pre_hire` 경계 사례를 함께 보정했다.
- `unfair_treatment`와 `discrimination` 사건은 probation 표면태그보다 실질 쟁점을 우선했다.
