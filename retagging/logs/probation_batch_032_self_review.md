# probation_batch_032 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_032.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_032_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `dismissal_validity`: 11건
- `misconduct`: 1건
- `procedure`: 4건
- `renewal_expectation`: 1건
- `work_ability`: 12건
- `worker_status`: 1건

## 수습 vs 비수습 분류
- `probation`: 27건
- `fixed_term`: 1건
- `regular`: 2건

## 처분 유형 요약
- `rejection_of_regular_employment`: 23건
- `dismissal`: 5건
- `contract_termination`: 1건
- `no_formal_disposition`: 1건

## 신뢰도 요약
- `high`: 25건
- `medium`: 5건
- `low`: 0건

## 주요 경계 사례
- `id_401681`: 3개월 시용계약과 계약기간 종료가 겹쳐 구제범위가 갈린 사례
- `id_401701`: 출퇴근기록 조작과 징계양정이 명확한 misconduct 사례
- `id_401719`: 해고사유 서면통지 부재가 결론을 좌우한 procedure 사례
- `id_402439`: 권고사직 합의로 해고 부존재가 정리된 no_formal_disposition 사례
- `id_402605`: 시용근로관계 부정이 결론을 좌우한 worker_status 사례

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`
- 로컬 스키마/값 검증: 30/30, 오류 0, 경고 0

## 메모
- `worker_status`는 실제로 최종 쟁점인 `id_402605`에만 primary로 두었다.
- `procedure`는 서면통지 미비가 결론을 좌우하는 경우에만 primary로 두었다.
- `confidence=medium`은 상태·절차·구제범위가 함께 얽힌 경계 사례에만 제한적으로 사용했다.
