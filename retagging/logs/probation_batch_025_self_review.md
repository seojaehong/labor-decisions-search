# probation_batch_025 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_025.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_025_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `probation`: 24건
- `fixed_term`: 2건
- `renewal_stage`: 1건
- `regular`: 3건

## primary 분포
- `dismissal_validity`: 10건
- `work_ability`: 10건
- `procedure`: 6건
- `renewal_expectation`: 2건
- `unfair_treatment`: 1건
- `worker_status`: 1건

## rejection vs termination 구분
- `rejection_of_regular_employment`: 17건
- `probation_termination`: 2건
- `dismissal`: 6건
- `contract_termination` / `nonrenewal` / `no_formal_disposition`: 5건

## 주요 경계 사례
1. `id_350529`
   - 수습이 성립하지 않는 정식근로자 해고라 `procedure`와 `dismissal_validity`를 분리했다.
2. `id_350633`
   - 갱신기대권은 인정되지만 갱신거절의 합리성이 있어 `renewal_stage`로 정리했다.
3. `id_350887`
   - 폭행 사안은 실재하지만 해고통지서의 구체성 결여가 결론을 좌우했다.
4. `id_351039`
   - 시용기간 연장 권한과 절차가 적법하지 않아 본채용 거절이 무효로 이어졌다.
5. `id_351167`
   - 반복 계약과 공사중단 조항으로 기간제 계약만료를 우선 보아 `contract_termination`으로 정리했다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`

## 메모
- 025는 probation batch이지만 `regular`, `fixed_term`, `renewal_stage` 경계가 뚜렷해 사안별로 분기했다.
- 노사/괴롭힘/폭행이 섞인 사례는 절차 하자와 보복 여부를 secondary로 분리했다.
- 노출된 사실이 압축된 사례는 `notes`에 이유를 남겨 검색 맥락이 끊기지 않도록 했다.
