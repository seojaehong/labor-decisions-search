# current_status

상태: 작업중

## 지금 내가 하고 있는 것
- 작업 루트 `/mnt/c/dev/labor-decisions-search/retagging` 기준으로 batch 오케스트레이션 상태를 추적 중
- 완료 기준은 reviewed JSONL + self-review 메모 동시 존재
- merge / override / progress report는 기존 v1 산출물을 존중하는 증분 방식으로 갱신

## 현재 단계
- reviewed 완료: 148 / 148 batch (100%) ✅
- reviewed 건수: 4,332건
- merged 고유 case_id: 3,923건 (merged_final_v2.jsonl) — v1 대비 +84건
- 실행 중: 0개 batch
- 핵심 충돌: 0건
- override 누적: 233건

## 주제군별 진행
- probation: sample+001~033 완료 (34/34) ✅
- incompetence: sample+001~011 완료 (12/12) ✅
- absence: sample+001~033 완료 (34/34) ✅
- violence: sample+001~033 완료 (34/34) ✅
- workplace_bullying: sample+001~033 완료 (34/34) ✅

## 다음 작업
- Supabase DB 업데이트: v2 기준 3,923건 반영 (현재 3,839건 → +84건) — 확인 필요
- notes 경고 61건 backlog 처리 (confidence=medium 공란, exclusion_flags 2개 이상)
- merged_final_v2.jsonl → 새 기준본 확정 후 v1 archive

## 내가 자동으로 보는 것
- `input/batches/*.jsonl`
- `output/reviewed/*_reviewed.jsonl`
- `logs/*_self_review.md`
- `logs/merge_collisions_report.md`
- `output/reviewed/manual_merge_overrides_v1.json`
- `logs/bulk_progress_report.md`

## Watchdog
- last_watchdog_refresh: 2026-03-21 10:18:51
