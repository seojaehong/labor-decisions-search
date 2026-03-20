# current_status

상태: 작업중

## 지금 내가 하고 있는 것
- 작업 루트 `/mnt/c/dev/labor-decisions-search/retagging` 기준으로 batch 오케스트레이션 상태를 추적 중
- 완료 기준은 reviewed JSONL + self-review 메모 동시 존재
- merge / override / progress report는 기존 v1 산출물을 존중하는 증분 방식으로 갱신

## 현재 단계
- reviewed 완료: 97 / 143 batch (약 68%)
- reviewed 건수: 2,788건
- merged 고유 case_id: 2,561건 / 4,232건 (약 61%)
- 실행 중: 0개 batch
- 핵심 충돌: 0건
- override 누적: 130건

## 주제군별 진행
- probation: sample+001~014+015~030+032 완료 (31/33), 잔여 `031`, `033`
- incompetence: sample+001~011 완료 (12/12), 완료
- absence: sample+001~014+031~033 완료 (18/33), 잔여 `015~030`
- violence: sample+001~014+031~033 완료 (18/33), 잔여 `015~030`
- workplace_bullying: sample+001~014+031~033 완료 (18/33), 잔여 `015~030`

## 내가 자동으로 보는 것
- `input/batches/*.jsonl`
- `output/reviewed/*_reviewed.jsonl`
- `logs/*_self_review.md`
- `logs/merge_collisions_report.md`
- `output/reviewed/manual_merge_overrides_v1.json`
- `logs/bulk_progress_report.md`

## Watchdog
- last_watchdog_refresh: 2026-03-21 03:58:15
