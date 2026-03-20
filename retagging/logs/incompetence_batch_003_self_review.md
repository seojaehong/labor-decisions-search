# incompetence_batch_003 self-review

## 1. batch 개요
- batch: `incompetence_batch_003`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. primary 분포
- `disciplinary_severity`: 5
- `renewal_expectation`: 8
- `work_ability`: 5
- `procedure`: 5
- `dismissal_validity`: 4
- `misconduct`: 2
- `unfair_treatment`: 1

## 3. employment_stage 분포
- `regular`: 14
- `renewal_stage`: 8
- `probation`: 8

## 4. 대표 검토 사례
- `id_26625`: `renewal_expectation` / `renewal_stage` / `nonrenewal` — 아파트 관리 분야 갱신기대권 인정 + 평가 객관성 부족.
- `id_28165`: `procedure` / `regular` / `dismissal` — 해고사유 부정과 함께 서면통지 하자가 명시된 일반해고 사건.
- `id_28325`: `dismissal_validity` / `regular` / `no_formal_disposition` — 자진퇴직 의사와 사용자 해고 의도 부재로 해고 존재 자체가 부정됨.
- `id_30771`: `disciplinary_severity` / `regular` / `dismissal` — 근무태도·성적 불량은 징계사유가 되나 징계해고까지는 과다하여 통상해고가 부당.
- `id_31867`: `dismissal_validity` / `probation` / `rejection_of_regular_employment` — 객관적·구체적 근거 없는 수습평가에 따른 본채용 거부 부당.

## 5. batch 메모
- batch 003은 갱신기대권/정규직 전환기대권 사건 비중이 높아 incompetence보다 `renewal_expectation`이 훨씬 안정적이었다.
- `id_28325`처럼 해고 존재가 부정되는 사건은 `no_formal_disposition`으로 정리했다.
- 수습 배치와 일반 징계해고가 섞인 케이스는 `misconduct`와 `disciplinary_severity`를 분리해 과대분류를 줄였다.
