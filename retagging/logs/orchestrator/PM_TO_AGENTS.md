# PM_TO_AGENTS

이 파일은 PM(현재 이 에이전트)이 코덱스 / 클로드 / 기타 워커에게 남기는 운영 지시문이다.
작업 시작 전과 배치 묶음 완료 후 우선 확인한다.

---

## 공통 작업 루트
- `/mnt/c/dev/labor-decisions-search/retagging`

## 공통 원칙
1. 기존 v1 문서 본문은 수정하지 않는다.
   - `prompts/tag_dictionary_v1.md`
   - `prompts/tagging_prompt_v1.md`
   - `prompts/review_checklist_v1.md`
   - `prompts/merge_policy_v1.md`
2. 규칙상 답답한 점, enum 공백, 구조적 한계는 `logs/rule_change_notes_v1.md`에만 제안한다.
3. destructive action 금지. 삭제/대규모 덮어쓰기 금지.
4. 다른 워커가 만든 파일을 되돌리거나 포맷을 임의 변경하지 않는다.
5. 출력 포맷은 기존 reviewed / self-review 스타일을 유지한다.

## 병렬 운영 규칙
- 동시에 활성 워커는 최대 3개까지만 유지한다.
- 기본 분담:
  - 코덱스: 앞 배치부터 진행
  - 클로드: 21시 이후 뒤 배치부터 진행
  - PM: 충돌 판정, override, 상태판, 후속 조율
- 같은 배치를 두 워커가 중복으로 잡지 않는다.
- 공유 파일(`manual_merge_overrides_v1.json`, `merge_collisions_report.md`, `bulk_progress_report.md`)은 메인 후처리 담당만 수정하는 것을 원칙으로 한다.

## PM 우선순위
1. 충돌이 있으면 먼저 판정하고 override에 반영
2. 충돌이 없으면 현재 진행 큐/완료 배치 상태를 갱신
3. 그 다음 대시보드/상태판 갱신
4. 그 다음 특이값/규칙 이슈 리뷰

## PM 자율 행동 규칙
PM은 별도 지시가 없어도 아래 조건이면 후속 조치를 시작한다.
- `SHARED_STATUS.md` 변경
- `AGENTS_TO_PM.md`에 새 Done / Waiting / Blocked 추가
- `merge_collisions_report.md`에 신규 충돌 발생
- reviewed 파일 신규 생성
- 대시보드 수치와 실제 진행 상태 불일치

즉, PM은 관찰만 하지 말고 실제로 다음 액션(충돌 판정/override/상태판 반영)을 수행해야 한다.
