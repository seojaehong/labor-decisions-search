# current_status

상태: 작업중

## 지금 내가 하고 있는 것
- 작업 루트 `/mnt/c/dev/labor-decisions-search/retagging` 기준으로 bulk retagging 흐름을 따라가는 중
- 새 reviewed 파일/로그/merge 충돌이 생기면 선조치 후 보고
- 현재는 batch 009 완료 이후 batch 010 진입 가능 상태를 기준으로 팔로우 중

## 현재 단계
- 샘플 단계: 완료
- 1차 bulk: 완료
- 2차 bulk+: 진행 중
- 최신 기준:
  - 누적 input: 1,390건
  - merged: 1,273건
  - override: 66건
  - 충돌: 0건
  - 진행률: 약 33%

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

## 메모
- 기존 status_dashboard.html은 정적 파일이라 자동 갱신되지 않음
- 숫자 갱신이 필요할 때 이 파일과 대시보드 HTML을 함께 업데이트하면 됨
