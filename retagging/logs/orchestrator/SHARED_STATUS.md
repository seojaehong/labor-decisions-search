# SHARED_STATUS

이 파일은 PM / 코덱스 / 클로드 / 오픈클로가 공통으로 보는 현재 운영 상태판이다.
숫자는 대략 최신 기준으로 갱신하고, 세부 산출물은 대시보드/리포트를 따른다.

---

## Current Mode
- 상태: 작업중
- 운영 방식: batch 단위 bulk retagging
- 병렬 제한: 최대 3개

## Work Split
- 코덱스: 앞 배치부터 진행
- 클로드: 21시 이후 뒤 배치부터 진행
- 오픈클로: 코덱스/클로드 산출물 리뷰 및 검토
- PM: 충돌 판정 / override / 상태판 / 운영 조율

## Latest Known Progress
- reviewed: 148 / 148 batch (100%) ✅ ALL COMPLETE
- reviewed records: 4,332건
- merged unique cases: 3,923건 (`merged_final_v2.jsonl`) — v1(3,839) 대비 +84건
- 핵심 충돌: 0건
- override: 233건
- merge 실행: 2026-03-21 (all 148 files)

## Current Running Queue
- 현재 실행 중 batch 없음
- 잔여 reviewed 배치: 없음 (모두 완료)

## Recently Finished
- merged_final_v2.jsonl 생성 완료 (148개 파일 전체 재merge)
- absence/violence/workplace_bullying batch_001 ~ 033 전체 완료
- probation batch_001 ~ 033 전체 완료

## PM Check Needed
- **Supabase DB 업데이트 승인 필요**: v2 기준 3,923건 → 현재 DB 3,839건 → +84건 반영 예정
  - 실행: `python scripts/load_merged_tags_to_supabase.py --input retagging/output/merged/merged_final_v2.jsonl --apply --snapshot-version merged_final_v2`
- notes 경고 61건 backlog (confidence=medium 공란, exclusion_flags 2개 이상 공란)
- probation_batch_021 validator warning 4건 (id_34643 등) — 낮은 우선순위

## Notes
- `merged_final_v2.jsonl`이 실질 최신 기준. v1은 archive 대상
- notes 경고 61건은 `merge_report.md` 참조
- v2 dry-run 완료, apply는 PM 확인 후 진행
