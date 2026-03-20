# incompetence_batch_001 self-review

## 1. batch 개요
- batch: `incompetence_batch_001`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. primary 분포
- `procedure`: 5
- `dismissal_validity`: 6
- `renewal_expectation`: 5
- `work_ability`: 7
- `misconduct`: 2
- `disciplinary_severity`: 5

## 3. employment_stage 분포
- `regular`: 17
- `renewal_stage`: 5
- `probation`: 8

## 4. 대표 검토 사례
- `id_13295`: `procedure` / `regular` / `transfer` — 업무능력 부족보다 과장보직 박탈·강임 과정의 규정 위반과 인사권 남용이 중심.
- `id_13323`: `dismissal_validity` / `regular` / `dismissal` — 수습을 거쳐 이미 정식근로자 지위가 형성된 뒤 일반해고가 문제 된 사례.
- `id_14007`: `renewal_expectation` / `renewal_stage` / `nonrenewal` — 저성과 태그보다 촉탁직 재고용 기대권과 재고용거절 합리성이 중심.
- `id_14663`: `disciplinary_severity` / `regular` / `disciplinary_dismissal` — 근무태만 등 징계사유는 일부 인정되나 양정 과다가 결론을 좌우.
- `id_15427`: `procedure` / `regular` / `other` — 일방적 휴직연장 정당성이 쟁점인 인사처분 사건. v1 disposition 공백으로 other 사용.

## 5. batch 메모
- incompetence 배치에도 전보·강임, 휴직연장, 직위해제처럼 해고가 아닌 인사처분이 섞여 있어 `unrelated_to_dismissal` 또는 `other` 처리가 필요했다.
- 수습 사건 일부는 이미 정식근로자 전환 후 일반해고 구조(`id_13323`)라 `regular + dismissal`로 보정했다.
- 무기계약 전환/촉탁 재고용 사건은 `renewal_expectation`으로 이동시켜 검색 노이즈를 줄였다.
