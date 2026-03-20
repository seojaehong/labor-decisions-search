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
- `procedure`: 5건
- `renewal_expectation`: 3건
- `transfer_validity`: 1건
- `work_ability`: 7건
- `worker_status`: 8건

## 주요 경계 사례
- `id_36857`: 배차거부와 징계해고 정당성이 함께 문제된 수습 운전기사 사건.
- `id_37015`: 시용근로관계와 본채용 거부 정당성이 함께 인정된 사건.
- `id_37669`: 부당한 인사발령과 대기발령이 함께 문제된 사건.
- `id_38001`: 근로계약관계 성립 자체가 부정된 당사자적격 사건.
- `id_38337`: 근거자료와 평가기준이 부족했던 본채용 거부 부당 사건.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 모두 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`

## 메모
- probation 배치 안에 renewal, pre_hire, transfer, disciplinary_severity가 섞여 있어 먼저 전단계와 비수습 사건을 분리했다.
- `procedure`는 서면통지·사유 특정·평가기준 문제에, `work_ability`는 평가 객관성과 본채용 적격성 판단에 우선 사용했다.
- `unrelated_to_probation`은 37529, 37669, 37709, 37919, 3801 같은 비수습/비시용 축에서만 제한적으로 적용했다.
