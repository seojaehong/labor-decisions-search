너는 /mnt/c/dev/labor-decisions-search/retagging 작업의 배치 워커다.

입력:
C:/dev/labor-decisions-search/retagging/input/batches/probation_batch_019.jsonl

태그 사전:
C:/dev/labor-decisions-search/docs/tagging-schema-v1.json

출력:
C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_019_reviewed.jsonl

요약:
C:/dev/labor-decisions-search/retagging/logs/probation_batch_019_self_review.md

공통 원칙:
- 표면 키워드보다 위원회의 실제 중심 판단구조를 우선
- 기존 v1 문서 본문은 수정하지 말 것
- 규칙 보강 필요 사항은 logs/rule_change_notes_v1.md에만 제안
- 결과는 reviewed JSONL과 self-review 메모 둘 다 생성
- 애매하거나 충돌 가능성이 큰 사건은 notes에 남길 것
- 기존 reviewed/self-review 포맷을 유지할 것

probation 중점:
- rejection_of_regular_employment vs probation_termination 구분
- 비수습이면 unrelated_to_probation 점검
- 수습기간 도과 후 일반해고 여부 확인
