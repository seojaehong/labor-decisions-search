# probation_batch_028 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_028.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_028_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `absence_without_leave`: 1건
- `attendance`: 1건
- `disciplinary_severity`: 1건
- `dismissal_validity`: 2건
- `misconduct`: 1건
- `procedure`: 4건
- `renewal_expectation`: 3건
- `transfer_validity`: 1건
- `work_ability`: 15건
- `worker_status`: 1건

## 주요 경계 사례
- `id_36857`: 배차거부와 징계해고 정당성이 함께 문제된 수습 운전기사 사건.
- `id_37015`: 시용근로자성보다 평가 부적합이 본론이었던 본채용 거부 사건.
- `id_37665`: 정당한 본채용 거부와 부당노동행위 아님이 함께 인정된 사건.
- `id_38001`: 근로계약관계 성립 자체가 부정된 당사자적격 사건.
- `id_38337`: 근거자료와 평가기준이 부족했던 본채용 거부 부당 사건.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 모두 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`

## 메모
- worker_status는 최종 쟁점일 때만 쓰도록 다시 수축했고, 본채용 거부의 본론이 평가·서면통지·정당사유인 경우는 work_ability / dismissal_validity / procedure로 재정렬했다.
- `procedure`는 사유 특정·서면통지 자체가 결론을 좌우하는 사건에만 유지했고, 실체 판단이 먼저 나오는 사건은 substantive 태그를 우선했다.
- confidence는 genuinely ambiguous한 mootness·계약만료·당사자적격 사건만 낮추고, 나머지는 high로 올렸다.
