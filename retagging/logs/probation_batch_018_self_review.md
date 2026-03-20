# probation_batch_018 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_018.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_018_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `dismissal_validity`: 21건
- `procedure`: 7건
- `misconduct`: 2건
- `no_formal_disposition` 성격의 종료 사례: 4건
- `regular`로 보정한 비수습/도과 사건: 2건

## 수습 vs 비수습 분류
- `id_343839`, `id_34393`, `id_343975`는 수습 도과 또는 계약 하자 때문에 `regular` 쪽으로 보정했다.
- `id_34355`, `id_343783`, `id_343897`, `id_343985`는 합의해지·구제이익 소멸·사직서 수리로 실질적인 본채용 거부 판단을 하지 않았다.

## procedure 중심 사례
- `id_343`, `id_34301`, `id_343731`, `id_343855`, `id_343979`, `id_344041`, `id_344115`, `id_344159`
  - 본채용 거부 사유의 구체성 부족, 서면통지 하자, 평가 공정성 결여, 노조활동 관련 불이익취급이 핵심이어서 procedure 축으로 정리했다.

## misconduct 중심 사례
- `id_343439`, `id_343695`
  - 강의 오답·인신공격, 지시불이행·음주·업무방해 등 직접 비위행위가 본채용 거부 사유의 중심이라 misconduct를 유지했다.

## 주요 판단 포인트
1. 시용/수습 인정 사건이 대부분이라 `dismissal_validity`를 기본값으로 두되, 서면사유 부실이나 평가 구조 하자가 결론을 좌우하면 `procedure`로 올렸다.
2. 계약상 수습기간이 규정상 상한을 넘거나 당초 합의되지 않은 경우는 `regular`로 보정하고 `unrelated_to_probation` 취지로 정리했다.
3. 합의해지·권고사직·구제이익 소멸은 `no_formal_disposition` 계열로 구분해, 본채용 거부의 실질 판단과 분리했다.
4. 노조활동이 결부된 사건은 `procedural_due_process`와 `protection_against_retaliation`을 함께 보고, 지배·개입은 단정하지 않았다.

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`
