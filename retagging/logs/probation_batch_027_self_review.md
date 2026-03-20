# probation_batch_027 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_027.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_027_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `disciplinary_severity`: 1건
- `discrimination`: 1건
- `dismissal_validity`: 11건
- `misconduct`: 2건
- `procedure`: 5건
- `transfer_validity`: 1건
- `work_ability`: 5건
- `worker_status`: 4건

## 주요 경계 사례
- `id_35615`: 근로자성은 인정되지만 상시근로자 수 5명 미만이라 실체 판단보다 각하가 먼저 선행된 사례다.
- `id_35979`: 견습/실습이 채용 선발이 아니라 실질 근로관계였는지가 핵심이라 `worker_status`로 정리했다.
- `id_36337`: 요양원 상시근로자 수와 수습 여부가 함께 문제되어 threshold와 probation이 겹친 사례다.
- `id_36533`: 차별시정 신청으로서 probation보다 period-worker 차별 판단이 앞서는 경계 사례다.
- `id_36807`: 감봉 처분을 먼저 해두고 같은 사유로 본채용 거부를 문제 삼은 징계양정 경계 사례다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`

## 메모
- probation 배치지만 `worker_status`, `pre_hire`, `fixed_term`, `discrimination`가 섞여 있어 판단 축을 먼저 분리했다.
- `procedure`는 서면통지·평가기준 고지·절차 공정성 문제에, `work_ability`는 평가 객관성과 적격성 판단에 우선 사용했다.
- `unrelated_to_probation`은 실제로 probation 쟁점이 아닌 `regular` / `fixed_term` / `pre_hire` 경계에서만 제한적으로 두었다.
