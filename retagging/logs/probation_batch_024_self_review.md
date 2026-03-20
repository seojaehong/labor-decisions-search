# probation_batch_024 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_024.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_024_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `work_ability`: 10건
- `dismissal_validity`: 6건
- `misconduct`: 3건
- `procedure`: 3건
- `renewal_expectation`: 3건
- `disciplinary_severity`: 2건
- `worker_status`: 2건
- `unfair_treatment`: 1건

## 주요 경계 사례
- `id_349575`: 노동조합/부당노동행위 주장보다 본채용 거부 정당성과 절차가 결론을 좌우했다.
- `id_349649`: 일부 비위 인정에도 불구하고 징계양정 과다와 절차 하자가 함께 문제된 사례다.
- `id_349993`: 채용내정 성립 여부가 선결이라 `pre_hire`/`worker_status`로 보정했다.
- `id_350245`, `id_350277`: 수습 표기보다 정규직 전환기대권과 갱신거절 합리성이 중심이었다.
- `id_350265`: 수습보다 기간제근로자성과 계약만료가 핵심이라 probation 노이즈를 분리했다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`

## 메모
- 수습/시용·징계·절차·갱신기대권이 혼재한 배치라 primary를 중심으로 secondary와 exclusion_flags를 보강했다.
- `unrelated_to_probation`은 renewal/fixed-term/pre-hire 사건에만 제한적으로 사용했다.
