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


## absence / incompetence 추가 검수에서 확인된 보완점

4. **v1 사전에 없는 값이 여러 축에서 유입됨**
   - `issue_type_primary`: `performance`, `attendance`, `transfer_validity`
   - `disposition_type`: `reprimand`, `demotion`
   - `fact_markers`: `repeated_absence`, `warning_given`, `public_institution`, `long_tenure`, `investigation_conducted`
   - `exclusion_flags`: `not_really_performance_case`
   - 초안 생성 후 enum validation이 사실상 필수임.

5. **absence_without_leave의 위상 재검토 필요**
   - 현 v1에서는 secondary에만 있고 primary에는 없음.
   - 하지만 전형적 장기 무단결근 사건(`id_10249`, `id_10411`)에서는 핵심 쟁점으로 쓰고 싶어짐.
   - 제안: v2에서 `issue_type_primary`에 `absence_without_leave` 추가 여부 검토.

6. **performance vs work_ability 경계 명확화 필요**
   - 수습/본채용 거부 사건에서 점수·평가가 핵심 사실이어도, 법적 중심은 대개 "적격성 판단"이므로 `work_ability`가 더 안정적이었음.
   - `performance`는 primary보다 secondary로 두는 편이 v1 구조와 더 잘 맞음.

7. **reprimand / demotion 등 경징계·인사처분의 disposition 공백**
   - v1에는 `reprimand`, `demotion` enum이 없어 `other` 또는 `transfer`로 흡수할 수밖에 없었음.
   - 제안: v2에서 disposition_type 확장 검토.

8. **renewal_stage vs fixed_term 구분 보완 필요**
   - 기간제 사건이라도 핵심이 갱신기대권 존부/갱신거절이면 `employment_stage=renewal_stage`가 일관적이었음.
   - `fixed_term`은 단순 기간만료/계약형태 설명용으로 축소 운용하는 편이 나아 보임.


9. **괴롭힘 신고 후 불이익 사건에서 `retaliation` 공백이 드러남**
   - `id_10281` 같은 전형적 신고 후 보복 전보 사건은 현재 v1에서 `unfair_treatment`로 우회해야 함.
   - 제안: v1.1 또는 v2에서 `retaliation`을 primary enum으로 추가 검토.

10. **괴롭힘 조사·분리조치 사건에서 `transfer_validity` primary 필요성이 큼**
   - `id_10647`처럼 보복이 아니라 행위자/피해자 분리조치의 정당성이 핵심인 사건은 `transfer_validity`를 primary로 두고 싶어짐.
   - 현재는 `unfair_treatment`로 흡수되어 다소 뭉개짐.

11. **조사 수행 여부가 괴롭힘 카테고리에서 반복적으로 중요함**
   - `investigation_conducted`, `duty_of_investigation`이 자주 필요했으나 v1 enum 밖이었음.
   - 조사 미비/보호조치 의무를 다루는 사건을 위해 fact_marker 또는 legal_focus 확장 검토 필요.

12. **괴롭힘 인정 + 양정 과다 사건은 `disciplinary_severity` 우선 원칙이 유효함**
   - `id_10345`, `id_10395` 유형은 괴롭힘 성립 자체보다 제재 수위가 결론을 좌우했음.
   - v1의 "표면 키워드보다 실질 쟁점 우선" 원칙은 유지 가능.

13. **probation 배치에 기간만료/갱신기대권/해고부존재 사건이 상당수 혼입됨**
   - `id_10621`, `id_10737`, `id_1079`, `id_11155`처럼 표면상 수습 태그가 있어도 실질은 `renewal_expectation`, `contract_termination`, `no_formal_disposition` 사건인 경우가 반복됨.
   - 제안: v1.1 또는 v2에서 probation 배치 검수 가이드에 "수습 키워드보다 종료 구조를 먼저 보라"는 문구를 더 강하게 넣을 필요가 있음.

14. **`worker_status`가 선결 쟁점인 probation 사건 처리 공백**
   - `id_11225`처럼 상시근로자 수 5인 미만 적용대상성이나 시용근로자성 자체가 결론을 좌우하는 사건은 현재 v1 primary enum에서 다루기 답답함.
   - 제안: v2에서 `worker_status`를 primary enum으로 승격할지 검토.

15. **absence batch에서도 경징계/인사처분 disposition 공백이 반복됨**
   - absence_batch_001~005에서도 `warning/reprimand`, `demotion` 유형이 계속 등장해 reviewed에서는 `other`로 흡수할 수밖에 없었음.
   - 제안: v1.1 또는 v2에서 `disposition_type`에 `warning(reprimand)`와 `demotion` 별도 enum 추가 검토.

16. **absence 배치 입력 단계의 노이즈 분리 필요**
   - 결근 배치에 `무단이탈/근무지 이탈/지각·조퇴 중심`, `사직/해고부존재`, `괴롭힘 신고 후 불이익` 사건이 상당수 혼입됨.
   - 제안: 배치 생성 시 `absence_without_leave`와 `attendance`, `dismissal_validity`, `unfair_treatment` 후보를 사전 분기하거나, 최소한 self-review 우선점검 대상으로 표시하는 규칙 추가 검토.

## probation_batch_002~005 추가 검수에서 확인된 보완점

15. **probation 배치 안의 부당노동행위 결합 사건 처리 가이드 보강 필요**
   - `id_13103`처럼 수습 적용의 적법성과 동시에 불이익취급·지배개입이 결론을 좌우하는 사건은 `dismissal_validity`와 `unfair_treatment` 경계가 흔들림.
   - 제안: v1.1 가이드에 "조합활동 보복성이 결론의 핵심이면 `unfair_treatment`를 우선 검토" 문구 추가.

16. **구제이익 소멸/부재 사건의 tagging 우선순위 보강 필요**
   - `id_14559`, `id_15291`, `id_17855`처럼 실체 판단보다 구제이익 유무가 결론을 좌우하는 사건은 현재 v1에서 `dismissal_validity`로 흡수할 수밖에 없음.
   - 제안: v2에서 별도 primary 신설 여부를 검토하거나, 최소한 notes 작성 기준을 더 명시할 필요가 있음.


## 2026-03-20 incompetence_batch_001~003 review notes
- `worker_status`가 결론 중심인 사건(당사자적격, 5인 미만 적용대상성, 이미 정식근로자로 전환되었는지 여부)에서 v1 primary enum 공백이 반복적으로 드러남. 현행 v1에서는 `dismissal_validity`/`procedure`/`unfair_treatment`로 우회 가능하지만, v1.1에서는 primary 후보 또는 별도 선결쟁점 필드 신설 검토 가치가 있음.
- 휴직연장·직위해제·대기발령처럼 해고가 아닌 인사처분이 incompetence 배치에 섞이는 경우 `disposition_type`에 `other`로 흡수하게 되므로, 필요시 v1.1에서 `leave_extension`/`standby_order`/`position_removal` 계열 보강 검토.
