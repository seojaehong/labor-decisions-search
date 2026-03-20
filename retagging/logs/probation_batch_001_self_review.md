# probation_batch_001 self-review

## 1. batch 개요
- batch: `probation_batch_001`
- reviewed 건수: 31
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. primary/secondary가 흔들린 대표 사례
- `id_11111`
  - 평가 요소도 있으나 실제 중심은 의료기관 내 지시 거부·월권행위 등 비위성 행위라 `misconduct`를 primary로 선택.
- `id_11473`
  - 결근/조퇴가 핵심 사실이지만 정규직 징계가 아니라 수습 적격성 판단 구조라 `attendance`보다 `work_ability`를 primary로 유지.
- `id_10917`
  - 목디스크 사유는 성과가 아니라 직무수행 가능성 판단 문제라 `work_ability`를 primary로 두는 편이 더 안정적이었음.
- `id_11371`
  - 평가 공정성과 통지 문제, 사유 부존재가 모두 있지만 시용기간 중 조기 종료 사건이라 `dismissal_validity` + `probation_termination` 조합으로 정리.

## 3. disposition_type 판단이 애매했던 사례
- `id_10603`, `id_11149`, `id_11301`
  - 본채용 거부 통지/절차 하자 중심 사건이라 `rejection_of_regular_employment`를 유지하되 `procedure` primary를 부여.
- `id_11371`
  - 시용기간 만료 후 본채용 거부가 아니라 시용기간 중 급박한 종료 통지이므로 `probation_termination`으로 처리.
- `id_11183`, `id_1119`
  - probation 배치지만 실제로는 시용 종료 후 또는 본채용 후의 일반해고 구조라 `dismissal`로 보정.
- `id_1083`
  - 해고 존재 자체가 입증되지 않아 `no_formal_disposition` 검토가 필요했고, 최종적으로 그렇게 반영.

## 4. enum 밖 값이 필요했던 사례
- `worker_status`가 primary로 쓰고 싶은 사례가 있었음 (`id_11225` 등).
  - 현재 v1 primary enum에 없어 `notes`로 보완하거나 `dismissal_validity`/기타 구조로 흡수해야 했음.
- 수습 배치 안의 기간만료/갱신기대권 사건들(`id_10621`, `id_10737`, `id_1079`, `id_11155`)은 `renewal_expectation`으로 충분히 처리 가능했으나, probation 배치 내 노이즈 제어를 위해 exclusion을 적극 사용함.

## 5. v1 유지 가능 규칙
- 수습/본채용거부 사건은 성과 수치가 있어도 `work_ability` primary가 더 안정적임.
- 시용근로자성 부정 후 일반해고 판단으로 넘어가는 사건은 `regular + dismissal`로 정리하는 원칙이 유효함.
- 서면통지 하자만으로 결론이 나는 사건은 `procedure` primary가 잘 맞음.
- 기간만료/갱신기대권 사건은 probation 배치에 섞여 있어도 `renewal_stage`로 이동시키는 것이 검색 품질상 유리함.

## 6. v1.1 후보 제안
- `worker_status`를 primary enum에 둘지 검토할 가치가 있음. 5인 미만 적용대상성, 시용근로자성 자체가 결론을 좌우하는 사건에서 필요성이 보임.
- `fixed_term`와 `renewal_stage` 경계는 현행 v1로도 어느 정도 처리 가능하지만, probation 배치에 섞이는 기간만료 사건을 위해 guide 문구를 더 강화할 필요가 있음.

## 7. 새로 발견한 규칙 이슈
- probation 배치에 실제로는 `renewal_expectation`, `contract_termination`, `no_formal_disposition`, `regular dismissal` 성격 사건이 상당수 혼입됨.
- 시용기간 만료 후 일반해고인지, 시용기간 중 종료인지, 본채용 거부인지 구분이 반복적으로 중요함.
- `worker_status`가 핵심인 사건은 현재 v1에서 다소 답답하게 처리됨.
