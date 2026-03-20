# probation_batch_020 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_020.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_020_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `dismissal_validity`: 10건
- `work_ability`: 13건
- `worker_status`: 3건
- `misconduct`: 1건
- `renewal_expectation`: 2건
- `redundancy`: 1건

## 수습 vs 비수습 분류
- 수습(probation) 중심 사건이 다수였고, `worker_status`, `renewal_expectation`, `redundancy` 경계 사건을 함께 정리했다.
- `id_345355`, `id_345929`, `id_345855`, `id_346315`, `id_346379`는 probation 바깥 또는 probation 노이즈 정리에 중점을 두었다.

## rejection vs termination 구분
- `rejection_of_regular_employment`: 17건
- `probation_termination`: 3건
- `dismissal`: 6건
- `no_formal_disposition`: 2건
- `nonrenewal`: 2건

## 주요 경계 사례
1. `id_344971`
   - 강제추행 신고 이후 경고장과 해임 발언이 겹쳐, 본채용 거부의 객관성과 보복성 여부를 함께 봤다.
2. `id_345151`, `id_345213`
   - 사직서 수리와 해고 철회로 인해 해고 존부가 먼저 정리되는 no-formal-disposition 성격의 사례로 보정했다.
3. `id_345271`, `id_346379`
   - probation 표기가 섞여 있어도 실질은 갱신기대권 또는 기간만료라서 renewal 축으로 분리했다.
4. `id_345355`, `id_345929`, `id_346315`
   - 시용 여부 부인 또는 통상해고 프레임이 핵심이라 probation 노이즈로 남기지 않았다.
5. `id_345837`, `id_345841`
   - 프로젝트·부상·업무불가 사정이 결합된 경계 사례라 일반 dismissal과 probation termination 사이를 신중히 보았다.

## 신뢰도 분포
- high: 28건
- medium: 2건

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`

## 메모
- 수습평가가 중심인 사건은 `dismissal_validity`보다 `work_ability`를 우선해 정리했다.
- 해고 철회, 사직서 수리, 구제이익 소멸은 `no_formal_disposition` 계열로 분리했다.
- probation 외 사건은 `unrelated_to_probation`과 함께 `worker_status`, `renewal_expectation`, `redundancy`로 정리했다.
