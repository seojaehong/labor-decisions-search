# validation_merge_checklist_v1

reviewed → merged 전환 전 체크리스트.

기준 문서:
- `prompts/merge_policy_v1.md`
- `prompts/tag_dictionary_v1.md`

---

## A. 입력 범위 확인
- [ ] 입력 파일이 `output/reviewed/*_reviewed.jsonl`인지 확인
- [ ] draft 파일이 섞이지 않았는지 확인
- [ ] 대상 reviewed 파일 목록을 기록했는지 확인

## B. 형식 검증
- [ ] 모든 파일이 JSONL 형식인지 확인
- [ ] 각 줄이 JSON parse 가능한지 확인
- [ ] 필수 필드(`case_id`, `issue_type_primary`, `review_status`, `tag_version`)가 존재하는지 확인

## C. enum 검증
- [ ] `issue_type_primary`가 v1 enum 안에 있는지 확인
- [ ] `employment_stage`가 v1 enum 안에 있는지 확인
- [ ] `disposition_type`이 v1 enum 안에 있는지 확인
- [ ] `issue_type_secondary`, `fact_markers`, `legal_focus`, `exclusion_flags`에 enum 밖 값이 없는지 확인
- [ ] enum 실패 건은 validation_report에 기록했는지 확인

## D. case_id 그룹핑
- [ ] 전체 고유 case_id 수를 계산했는지 확인
- [ ] 중복 case_id 목록을 뽑았는지 확인
- [ ] 중복 없는 레코드는 그대로 merged 후보로 분리했는지 확인

## E. 자동 병합 금지 조건 확인
- [ ] `issue_type_primary` 충돌 시 자동 병합하지 않았는지 확인
- [ ] `employment_stage` 충돌 시 수동 검토로 보냈는지 확인
- [ ] `disposition_type` 충돌 시 수동 검토로 보냈는지 확인
- [ ] `pending` 상태 레코드가 merge 입력에 들어오지 않았는지 확인

## F. union 후보 필드 확인
- [ ] `issue_type_secondary`를 union 후보로 처리했는지 확인
- [ ] `fact_markers`를 union 후보로 처리했는지 확인
- [ ] `legal_focus`를 union 후보로 처리했는지 확인
- [ ] `exclusion_flags`를 union 후보로 처리했는지 확인
- [ ] union 결과 중복 제거가 되었는지 확인

## G. 대표값 선택이 필요한 필드
- [ ] `summary_short` 대표값을 정했는지 확인
- [ ] `holding_summary` 대표값을 정했는지 확인
- [ ] `retrieval_note` 대표값을 정했는지 확인
- [ ] `industry_context` 충돌 시 수동 확인했는지 확인
- [ ] `confidence`는 더 보수적인 값으로 유지했는지 확인

## H. notes 작성 조건 확인
- [ ] source 2개 이상 병합 시 notes를 남겼는지 확인
- [ ] 핵심 충돌 해소 시 notes에 근거를 적었는지 확인
- [ ] `other`로 흡수한 disposition이 있으면 notes에 적었는지 확인
- [ ] confidence를 낮춘 경우 notes에 이유를 적었는지 확인

## I. 산출물 확인
- [ ] merged JSONL 파일 경로를 확정했는지 확인
- [ ] merged 레코드의 `review_status`는 `reviewed`로 유지했는지 확인
- [ ] `tag_version`이 `v1`인지 확인
- [ ] merged JSONL 전체 parse 검증을 다시 했는지 확인

## J. 로그/리포트 확인
- [ ] `logs/merge_report.md` 작성
- [ ] `logs/validation_report.md` 작성
- [ ] 필요 시 `logs/merge_conflicts_v1.md` 작성
- [ ] 병합 보류 case_id 목록을 남겼는지 확인

---

## Claude Code 연계 포인트
- merge 자동화 스크립트가 있다면 위 체크리스트 항목을 기계적으로 검증 가능해야 함
- 특히 아래는 자동화 우선 대상:
  - JSON parse 검증
  - enum validation
  - case_id 중복 탐지
  - union 후보 필드 병합
  - 충돌 필드 자동 분리(report 생성)
- 반대로 아래는 수동 판단 영역으로 남겨야 함:
  - `issue_type_primary` 최종 확정
  - `employment_stage` 충돌 해소
  - `disposition_type` 충돌 해소
  - 대표 요약문 선택
