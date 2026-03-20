# rule_change_notes_v1

## 이번 self-review에서 확인된 규칙 보완점

1. **enum validation 단계 필요**
   - draft 산출물에 `emotional_conflict_only`, `repeated_absence`처럼 v1 사전에 없는 `fact_markers`가 섞여 들어감.
   - tagging 단계 이후 자동 검증(허용 enum 외 값 탐지)이 필요함.

2. **해고 부존재 사건의 disposition_type 명확화 필요**
   - `dismissal_validity`를 primary로 두더라도, 실질이 해고 부존재/사직 효력 다툼이면 `disposition_type`은 `dismissal`보다 `no_formal_disposition`이 더 적절함.

3. **수습 사건에서 처분 유형 분기 재강조 필요**
   - 시용기간 내 종료는 `probation_termination`
   - 시용기간 만료 후 본채용 거부는 `rejection_of_regular_employment`
   - 이 분기를 tagging prompt와 review checklist에서 더 강조할 필요가 있음.

## 제안되는 후속 조치
- reviewed/merged 단계 전 JSON Schema 또는 enum validator 스크립트 추가
- `tagging_prompt_v1.md`에 "허용 enum 외 값 금지" 문구를 이미 넣었으나, 후처리 검증 단계도 별도로 둘 것
- `review_checklist_v1.md`에 "disposition_type이 해고 부존재 사건과 맞는지" 점검을 유지
