# current_status

상태: 작업중

## 지금 내가 하고 있는 것
- 작업 루트 `/mnt/c/dev/labor-decisions-search/retagging` 기준으로 bulk retagging 흐름을 따라가는 중
- 새 reviewed 파일/로그/merge 충돌이 생기면 선조치 후 보고
- 현재는 batch 007 진행 흐름을 파일 기준으로 팔로우 중

## 현재 단계
- 샘플 단계: 완료
- 1차 bulk: 완료
- 2차 bulk: 진행 중
- 최근 완료:
  - `violence_batch_001 ~ 005`
  - `workplace_bullying_batch_001 ~ 005`
- 최근 충돌 처리:
  - 6건 판정 완료
  - `output/reviewed/manual_merge_overrides_v1.json` 반영 완료

## 내가 자동으로 보는 것
- `output/reviewed/*.jsonl`
- `logs/*_self_review.md`
- `logs/merge_collisions_report.md`
- `output/reviewed/manual_merge_overrides_v1.json`
- `output/merged/*.jsonl`
- `logs/merge_report.md`
- `logs/validation_report.md`

## 상태 해석
- `작업중`: 내가 같은 범위 안에서 다음 수를 계속 두는 중
- `대기`: 새 input 또는 방향 지정이 필요함
- `판정필요`: 충돌/예외에 대한 수동 판단이 필요함
- `외부입력필요`: 네가 뭘 넘겨줘야 다음 단계로 갈 수 있음

## 마지막 업데이트 기준 메모
- 2차 bulk가 계속 진행 중이므로 이 파일은 내가 필요할 때 갱신함
