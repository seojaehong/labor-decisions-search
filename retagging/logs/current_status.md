# current_status

상태: 판정필요

## 지금 내가 하고 있는 것
- 작업 루트 `/mnt/c/dev/labor-decisions-search/retagging` 기준으로 batch 오케스트레이션 상태를 추적 중
- 완료 기준은 reviewed JSONL + self-review 메모 동시 존재
- merge / override / progress report는 기존 v1 산출물을 존중하는 증분 방식으로 갱신

## 현재 단계
- 누적 reviewed 완료: 69개 batch
- 실행 중: 0개 batch
- 대기 중: 73개 batch
- 입력 미도착: 357개 slot
- 수동 개입 필요: 1개 batch

## 주제군별 진행
- probation: 완료 18 / 입력존재 33 / 실행중 0 / 진행률 54.5%
- incompetence: 완료 9 / 입력존재 11 / 실행중 0 / 진행률 81.8%
- absence: 완료 14 / 입력존재 33 / 실행중 0 / 진행률 42.4%
- violence: 완료 14 / 입력존재 33 / 실행중 0 / 진행률 42.4%
- workplace_bullying: 완료 14 / 입력존재 33 / 실행중 0 / 진행률 42.4%

## 내가 자동으로 보는 것
- `input/batches/*.jsonl`
- `output/reviewed/*_reviewed.jsonl`
- `logs/*_self_review.md`
- `logs/merge_collisions_report.md`
- `output/reviewed/manual_merge_overrides_v1.json`
- `logs/bulk_progress_report.md`

## Watchdog
- last_watchdog_refresh: 2026-03-20 21:27:26
