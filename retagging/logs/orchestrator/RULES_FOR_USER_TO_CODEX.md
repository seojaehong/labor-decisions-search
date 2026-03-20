# RULES_FOR_USER_TO_CODEX

아래는 사용자가 코덱스에게 그대로 전달할 수 있는 운영 규칙이다.

```text
작업 루트는 반드시 /mnt/c/dev/labor-decisions-search/retagging 기준으로만 사용.

공통 원칙:
- 기존 v1 문서 본문 수정 금지
- 규칙 보강 필요 사항은 logs/rule_change_notes_v1.md에만 누적
- destructive action 금지
- 기존 reviewed/self-review 포맷 유지
- 다른 워커가 만든 파일을 임의로 되돌리거나 갈아엎지 말 것

병렬 운영:
- 동시에 활성 워커는 최대 3개까지만 유지
- 코덱스는 앞 배치부터 진행
- 클로드는 21시 이후 뒤 배치부터 진행 예정
- 같은 배치를 중복으로 잡지 말 것
- 공유 파일(manual_merge_overrides_v1.json, merge_collisions_report.md, bulk_progress_report.md)은 메인 후처리 흐름을 존중할 것

배치 작업 산출물:
- output/reviewed/<batch_name>_reviewed.jsonl
- logs/<batch_name>_self_review.md

작업 후 확인:
- JSONL parse 가능 여부
- 필수 필드 존재 여부
- review_status / tag_version 값 확인
- 애매한 케이스는 notes에 남길 것

중점 판정:
- probation: rejection_of_regular_employment vs probation_termination, 비수습이면 unrelated_to_probation
- absence: 무단결근 핵심 vs 배경, 배경이면 not_really_absence_case
- violence: misconduct vs disciplinary_severity
- workplace_bullying: 괴롭힘 성립 vs 양정 vs 보복, 배경이면 not_really_harassment_case

보고:
- 작업 완료 시 changed file paths
- 대표 보정 사례 3~5개
- 새 규칙 이슈
- PM 확인이 필요한 막힌 점
```
