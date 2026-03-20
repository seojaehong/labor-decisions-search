# probation_batch_026 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_026.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_026_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `dismissal_validity`: 16건
- `procedure`: 6건
- `disciplinary_severity`: 3건
- `work_ability`: 3건
- `renewal_expectation`: 2건

## 수습 vs 비수습 분류
- `probation`: 26건
- `fixed_term`: 2건
- `renewal_stage`: 1건
- `regular`: 1건

## rejection vs termination 구분
- `rejection_of_regular_employment`: 21건
- `dismissal`: 4건
- `disciplinary_dismissal`: 1건
- `no_formal_disposition`: 1건
- `suspension`: 1건
- `nonrenewal`: 1건
- `contract_termination`: 1건

## 주요 경계 사례
1. `id_351341`
   - 결근 처리와 퇴직 처리보다 서면통지 흠결이 결론을 좌우한 절차 사건이다.
2. `id_351481`
   - 정식 근로계약 후 수습 절차를 적용한 점이 쟁점이라 probation 노이즈를 분리하고 `procedure`로 정리했다.
3. `id_351757`
   - 징계사유 인정과 양정 적정성이 핵심인 징계해고 사건이라 `disciplinary_severity`를 중심에 뒀다.
4. `id_351851`
   - 사직서 제출과 해고 부존재가 문제된 fixed-term 경계 사례로 `no_formal_disposition`과 `resignation_dispute`가 앞섰다.
5. `id_351871`, `id_35291`
   - 갱신기대권과 계약만료가 핵심이어서 `renewal_expectation`으로 분리했다.
6. `id_35405`
   - 수습 불인정과 징계양정 과다, 소명기회 미부여가 함께 문제된 regular dismissal 사건이라 `unrelated_to_probation`을 부여했다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`
- 로컬 스키마/값 검증: 통과(30/30, 오류 0)

## 메모
- 수습/절차/징계/갱신기대권이 강하게 섞여 있어 primary 기준으로 분리했다.
- `unrelated_to_probation`은 `fixed_term`, `renewal_stage`, `regular` 경계에서만 제한적으로 사용했다.
- `notes`는 전건 채워 검색 맥락이 끊기지 않도록 했다.
