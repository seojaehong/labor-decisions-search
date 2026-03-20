# incompetence_batch_002 self-review

## 1. batch 개요
- batch: `incompetence_batch_002`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. primary 분포
- `work_ability`: 10
- `unfair_treatment`: 1
- `dismissal_validity`: 5
- `disciplinary_severity`: 5
- `procedure`: 2
- `renewal_expectation`: 5
- `misconduct`: 2

## 3. employment_stage 분포
- `probation`: 13
- `fixed_term`: 2
- `regular`: 11
- `renewal_stage`: 4

## 4. 대표 검토 사례
- `id_20247`: `unfair_treatment` / `fixed_term` / `other` — 차별시정 사건으로 저성과/해고 사건이 아니며 v1 disposition 공백으로 other 사용.
- `id_21037`: `procedure` / `probation` / `rejection_of_regular_employment` — 사유 자체는 인정되나 서면통지의 구체성 부족이 결론을 좌우.
- `id_21941`: `disciplinary_severity` / `regular` / `disciplinary_dismissal` — 괴롭힘·폭언 요소가 있어도 결론은 일부 징계사유 인정 + 해고 양정 과다.
- `id_23075`: `work_ability` / `regular` / `dismissal` — 경력직 임원의 영업실적 부진과 불성실 태도, 개선기회 부여 후 해고 정당.
- `id_24195`: `misconduct` / `regular` / `disciplinary_dismissal` — 서술상 결론 표현이 혼재하나 항명 등 전반적 징계사유를 근거로 한 징계해고 정당 취지로 읽힘.

## 5. batch 메모
- 차별시정·대기발령·부당노동행위 부정 사건이 혼재해 incompetence 레거시 태그를 그대로 따르면 과잉회수 위험이 컸다.
- 수습 본채용 거부 사건은 `work_ability`와 `dismissal_validity`를 분리했고, 서면통지 하자가 결론을 좌우하면 `procedure`로 보정했다.
- `id_24195`처럼 결과 표기와 문장 서술이 혼재한 케이스는 confidence를 한 단계 낮춰 보수적으로 처리했다.
