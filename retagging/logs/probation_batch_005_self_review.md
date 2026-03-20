# probation_batch_005 self-review

## 1. batch 개요
- batch: `probation_batch_005`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. primary/secondary가 흔들린 대표 사례
- `id_16299`
  - 수습 적용 부당 주장도 있으나 결론은 소명기회 미부여 등 절차 하자가 좌우하여 `procedure`를 primary로 둠.
- `id_16935`
  - 동료 간 불화와 업무지시 불이행이 함께 있어 `misconduct`와 `work_ability` 경계를 점검함.
- `id_1719`
  - 시용근로자성은 인정되지만 합리적 이유 부재로 본채용 거부가 부당한 전형 사례라 `dismissal_validity`/`work_ability` 구분을 재검토함.
- `id_17893`
  - 수습기간 만료 통지서만 교부된 절차형 사건이라 `procedure` primary가 명확했음.

## 3. disposition_type 판단이 애매했던 사례
- `id_16541`, `id_16785`, `id_17187`, `id_17675`
  - 수습기간 중 해고/채용취소 구조라 `probation_termination`이 적절했음.
- `id_16419`, `id_16463`, `id_17275`, `id_17429`, `id_17913`
  - 시용평가 후 본채용 거부 구조라 `rejection_of_regular_employment` 유지.
- `id_16729`, `id_17513`, `id_17855`
  - 기간만료·구제이익 소멸 사건으로 probation 검색 노이즈 제어가 중요했음.

## 4. 이번 배치에서 확인한 운영 메모
- 비위성 사유가 강한 수습 사건은 `misconduct` primary가 더 선명할 때가 있었음.
- 절차 하자가 명확한 사건은 수습 적격성 판단을 길게 끌지 않고 `procedure`로 정리하는 편이 일관적이었음.
- probation 배치 안에 징계해고·기간만료·당사자적격 사건이 혼입되어 있어 exclusion과 notes가 계속 중요했음.
