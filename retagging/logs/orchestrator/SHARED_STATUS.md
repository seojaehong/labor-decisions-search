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
- merged: 1,988건
- 충돌: 3건
- override: 91건
- 진행률: 약 52%
- 최근 기준: probation_batch_022 ~ 024 완료, front / rear queue 동시 진행 가능

## Current Running Queue
- Codex front queue
  - probation_batch_025
  - probation_batch_026
  - probation_batch_027
- Claude rear queue (reserved)
  - workplace_bullying_batch_033
  - violence_batch_033
  - absence_batch_033
  - 다음 묶음: workplace_bullying_batch_032, violence_batch_032, absence_batch_032

## Recently Finished
- probation_batch_022
- probation_batch_023
- probation_batch_024

## PM Check Needed
- `merge_collisions_report.md` 신규 3건 확인 필요
  - `id_30811`
  - `id_30879`
  - `id_32113`
- `probation_batch_021_reviewed.jsonl` validator warning 4건
  - `id_34643`
  - `id_346509`
  - `id_346727`
  - `id_346847`

## Notes
- 실제 최신 숫자는 `status_dashboard.html` 및 `logs/status_dashboard_data.json`도 함께 참고
- merge collision이 발생하면 `merge_collisions_report.md` 우선 확인
- rear queue 대상 033/032는 현재 reviewed/self-review 산출물이 없어 착수 가능 상태
