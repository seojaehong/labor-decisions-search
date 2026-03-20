# probation_batch_004 self-review

## 1. batch 개요
- batch: `probation_batch_004`
- reviewed 건수: 30
- 작업 기준:
  - `prompts/tag_dictionary_v1.md`
  - `prompts/tagging_prompt_v1.md`
  - `prompts/review_checklist_v1.md`
  - `prompts/merge_policy_v1.md`

## 2. primary/secondary가 흔들린 대표 사례
- `id_14469`
  - 무단이탈·교육거부·허위신고가 결합되어 있어 `misconduct`를 primary로 두는 편이 자연스러웠음.
- `id_14493`
  - 시설관리 업무 미흡이 문제 되었지만 결국 본채용 거부 사유 부존재 판단이므로 `work_ability` + `rejection_of_regular_employment`로 정리.
- `id_15023`
  - 수습기간 존재 자체의 입증 부족과 해고사유 부존재가 함께 있어 regular 전환 검토가 중요했음.
- `id_15381`
  - 수습평가 문구가 있으나 구조상 갱신기대권 인정 후 갱신거절 합리성 심사라 `renewal_stage`로 보정.

## 3. disposition_type 판단이 애매했던 사례
- `id_14977`, `id_15099`, `id_16089`, `id_16121`
  - 시용기간 중 종료 구조라 `probation_termination` 쪽으로 정리.
- `id_15205`, `id_15525`, `id_15809`, `id_15987`
  - 시용기간 만료 후 본채용 거부 구조라 `rejection_of_regular_employment` 유지.
- `id_14559`, `id_15291`
  - 구제이익 소멸/부재 사건으로 confidence를 보수적으로 유지.

## 4. 이번 배치에서 확인한 운영 메모
- probation 배치 안에서도 renewal_stage 전환이 필요한 사건이 반복적으로 나옴.
- 본채용 거부와 수습 중 해고의 문구가 혼재할 때는 종료 시점과 통지 문구를 함께 봐야 했음.
- 절차 하자 사건은 사유 존부 판단보다 `written_notice_missing`과 `procedural_defect` 정리가 더 중요했음.
