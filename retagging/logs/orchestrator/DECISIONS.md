# DECISIONS

운영 중 확정된 판단 원칙과 예외를 누적 기록한다.
새 규칙 제안이 아니라, 실제 작업 조율에 바로 쓰는 결정사항을 적는다.

---

## 확정 운영 원칙
- 작업 루트는 `/mnt/c/dev/labor-decisions-search/retagging` 고정
- v1 문서 본문은 수정하지 않음
- 규칙상 한계/공백은 `logs/rule_change_notes_v1.md`에만 누적
- 병렬 워커는 최대 3개
- 코덱스는 앞 배치부터, 클로드는 21시 이후 뒤 배치부터 진행
- PM은 충돌/override/상태판/조율 담당
- PM은 사용자가 따로 재촉하지 않아도 `logs/orchestrator/*.md`, `logs/merge_collisions_report.md`, `logs/current_status.md`, 대시보드 데이터를 먼저 읽고 다음 액션을 선제적으로 실행한다.
- PM의 실제 작업 여부는 말보다 tool 호출과 파일 변경으로 드러나야 하므로, 중요한 후속 조치는 가능한 한 먼저 실행하고 나중에 보고한다.
- PM 우선순위는 `충돌 판정 -> override 반영 -> 상태판 갱신 -> 다음 분배 확인 -> 특이값 리뷰` 순서로 고정한다.
- 아래 조건이 생기면 PM은 별도 지시 없이 후속 조치를 시작한다: SHARED_STATUS 변경, AGENTS_TO_PM에 새 Done/Blocked 추가, merge_collisions_report 신규 충돌 발생, reviewed 파일 신규 생성, 대시보드 수치와 실제 진행 상태 불일치.

## 확정 판정 원칙
- `dismissal_validity` vs `work_ability`
  - 법적 정당성 프레임이 핵심이면 `dismissal_validity`
  - 수습 적격성 판단이 직접 핵심이면 `work_ability`
- `dismissal` vs `disciplinary_dismissal`
  - 징계사유 전제 해고면 `disciplinary_dismissal`
- `rejection_of_regular_employment` vs `probation_termination`
  - 수습 만료 시 거부면 `rejection_of_regular_employment`
  - 수습 중도 해고면 `probation_termination`

## 상태판 규칙
- 상태 확인용 파일:
  - `logs/current_status.md`
  - `status_dashboard.html`
  - `logs/status_dashboard_data.json`
- 대시보드는 반자동 갱신 스크립트로 갱신
- 5분 주기 갱신 크론 사용
