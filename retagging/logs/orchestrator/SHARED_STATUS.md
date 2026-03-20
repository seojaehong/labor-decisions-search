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
- reviewed: 97 / 143 batch (약 68%)
- reviewed records: 2,788건
- merged unique cases: 2,561건 / 4,232건 (약 61%)
- 핵심 충돌: 0건
- override: 130건
- 최근 기준: probation은 `032`까지, rear queue는 `031~033` 완료

## Current Running Queue
- 현재 실행 중 batch 없음
- 다음 잔여 큐
  - probation: `031`, `033`
  - absence: `015~030`
  - violence: `015~030`
  - workplace_bullying: `015~030`

## Recently Finished
- probation_batch_028
- probation_batch_029
- probation_batch_030
- probation_batch_032
- absence_batch_031 ~ 033
- violence_batch_031 ~ 033
- workplace_bullying_batch_031 ~ 033

## PM Check Needed
- 핵심 merge collision 없음
- 필요 시 `probation_batch_021_reviewed.jsonl` validator warning 4건 별도 점검
  - `id_34643`
  - `id_346509`
  - `id_346727`
  - `id_346847`

## Notes
- 실제 최신 숫자는 `logs/bulk_progress_report.md`와 `logs/status_dashboard_data.json`을 우선 기준으로 본다
- `merge_collisions_report.md`의 신규 3건(`id_30811`, `id_30879`, `id_32113`)은 PM 판정 후 override/리포트 동기화 완료
- 즉시 착수 가능 잔여 작업은 absence/violence/workplace_bullying `015~030`, probation `031`, `033`
