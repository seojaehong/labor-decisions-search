# probation_batch_023 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_023.jsonl`
- 출력: `retagging/output/reviewed/probation_batch_023_reviewed.jsonl`
- 총 30건
- 작업일: 2026-03-20

## 수습/비수습 분류
- 수습(probation) 중심 사건은 22건으로, 대부분 `work_ability`, `dismissal_validity`, `procedure` 축에서 정리했다.
- 비수습/경계 사건은 `id_348825`, `id_349175`, `id_349203`, `id_349395`처럼 fixed-term, pre_hire, regular dismissal로 보정했다.

## rejection vs termination 구분
- `rejection_of_regular_employment`: 21건
- `probation_termination`: `id_348843`
- `dismissal`: `id_348851`, `id_348903`, `id_349175`, `id_349203`, `id_349379`, `id_349463`
- `contract_termination`: `id_348825`
- `nonrenewal`: `id_349041`

## 주요 경계 사례
1. `id_348825`
   - 수습보다 기간제 계약만료와 구제이익 소멸이 핵심이라 `fixed_term`으로 보정했다.
2. `id_349175`
   - 채용내정과 근로관계 성립 여부가 먼저여서 `pre_hire`와 `worker_status` 축으로 정리했다.
3. `id_349203`
   - 시용성이 부정되지만 반복 지각·협조거부가 해고 정당사유가 된 regular dismissal 사례다.
4. `id_349395`
   - 갱신기대권 부존재가 핵심인 기간제 만료 사건으로 probation 노이즈를 제거했다.
5. `id_349463`
   - 의료기관 내 비하 발언과 직장 내 괴롭힘이 직접 해고사유가 된 사례라 `workplace_harassment`를 중심에 뒀다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 모두 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`
