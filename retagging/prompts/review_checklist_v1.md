# review_checklist_v1

초안(JSONL) 1차 self-review 체크리스트.
기준 문서:
- `prompts/tag_dictionary_v1.md`
- `prompts/tagging_prompt_v1.md`

---

## A. primary 판정 점검

1. `issue_type_primary`가 판정의 중심 질문과 일치하는가?
2. 표면 사실(폭언, 결근, 모욕적 발언)에 끌려 primary를 잘못 잡지 않았는가?
3. 실제 핵심이 양정/절차/갱신기대권인데 `misconduct`나 `workplace_harassment`로 과대포착되지 않았는가?
4. 수습 사건에서 실제 중심이 적격성/본채용 거부인지, 시용기간 중 해고인지 구분했는가?

### 자주 보는 오류
- violence 사건인데 사실은 `disciplinary_severity`가 맞는 경우
- probation 사건인데 `dismissal_validity`와 `work_ability` 경계가 흐린 경우
- 괴롭힘 언급만으로 `workplace_harassment`를 준 경우

---

## B. employment_stage / disposition_type 점검

1. `employment_stage`가 수습/일반/기간제/갱신 단계와 맞는가?
2. `probation_termination`과 `rejection_of_regular_employment`를 혼동하지 않았는가?
3. 사직/합의해지 사건인데 해고 사건처럼 분류하지 않았는가?
4. 갱신거절 사건인데 수습 사건으로 남겨두지 않았는가?

---

## C. secondary / fact_markers 점검

1. secondary가 필요한 만큼만 달렸는가?
2. `evaluation`, `procedure`, `training_opportunity` 같은 법적 보조 쟁점이 누락되지 않았는가?
3. `written_notice`, `written_notice_missing`, `procedural_defect`, `evidence_insufficient` 같은 핵심 사실 마커가 빠지지 않았는가?
4. 단순 반복/중복 태깅은 없는가?

---

## D. exclusion_flags 점검

1. 검색 노이즈가 될 사건인데 exclusion이 빠지지 않았는가?
2. 아래 상황을 적극적으로 걸렀는가?
   - 괴롭힘/폭행 표면 태그지만 실질은 절차/양정 사건
   - 결근 샘플이지만 실제는 결근 중심 사건이 아님
   - 수습처럼 보이지만 실제는 갱신기대권 사건
   - 사직 의사표시 다툼이 핵심
3. exclusion을 너무 많이 달아 검색 가치까지 깎지는 않았는가?

---

## E. queries 점검

1. `include_for_queries`는 실제 사용자가 검색할 표현인가?
2. 사건의 핵심 쟁점을 반영하는가?
3. `exclude_for_queries`는 노이즈를 줄이는 데 실효성이 있는가?
4. 너무 판정문 문구 그대로 복붙하지 않았는가?

---

## F. confidence / notes 점검

1. 사실관계가 빈약한데 `high`를 남발하지 않았는가?
2. 경계선 사례는 `medium` 또는 `low`로 낮추고 이유를 `notes`에 썼는가?
3. 규칙 자체가 애매해 보이는 사례는 별도 규칙 메모로 분리했는가?

---

## G. 배치 우선순위 점검 포인트

### 1) probation_sample
- `probation_termination` vs `rejection_of_regular_employment`
- 수습+사직/합의해지/갱신기대권 혼입 여부
- 평가 객관성/교육·지도/서면통지 누락 여부

### 2) violence_sample
- `disciplinary_severity` 과소부여 여부
- 폭언/폭행이 부수 사유인지 핵심 사유인지 구분
- `not_really_harassment_case` 누락 여부

---

## H. self-review 결과 기록 형식

각 수정 건마다 아래를 남긴다.
- case_id
- 변경 전 핵심 태그
- 변경 후 핵심 태그
- 변경 이유
- 추가/삭제한 exclusion_flags
- confidence 조정 여부

규칙 자체 수정이 필요한 경우는 케이스 메모와 분리해서 `rule_change_notes_v1.md`에 누적한다.
