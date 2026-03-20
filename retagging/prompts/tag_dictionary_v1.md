# 태그 사전 v1

재태깅 JSONL 산출물에서 사용한 필드/enum 기준 정리 문서.

작성 기준:
- 샘플 5배치(100건) draft 산출물 기준
- 검색 적합성(retrieval usefulness) 중심
- 기존 단일 태그의 과잉분류를 줄이기 위해 `issue_type_primary` + `issue_type_secondary` + `exclusion_flags` 조합 사용

---

## 1) 레코드 기본 구조

각 판정례는 아래 필드를 가진다.

- `case_id`: 사건 식별자
- `case_name`: 사건명
- `summary_short`: 1문장 요약
- `holding_summary`: 결론 요약
- `retrieval_note`: 검색/분류 관점의 핵심 메모
- `employment_stage`: 고용 단계
- `issue_type_primary`: 주된 쟁점 1개
- `issue_type_secondary`: 부차 쟁점 0~N개
- `disposition_type`: 처분/종료 유형 1~N개
- `fact_markers`: 사실관계 마커 0~N개
- `legal_focus`: 법리 포인트 0~N개
- `industry_context`: 업종/맥락
- `exclusion_flags`: 검색 노이즈 제어용 플래그 0~N개
- `include_for_queries`: 추천 검색어 예시
- `exclude_for_queries`: 제외 검색어 예시
- `confidence`: high / medium / low
- `notes`: 검수 메모
- `review_status`: pending / reviewed
- `tag_version`: 현재 `v1`

---

## 2) 핵심 설계 원칙

### 2-1. primary는 “판정의 중심 질문” 하나만

예:
- 폭언 사실이 있어도, 판정의 핵심이 징계양정이면 `disciplinary_severity`
- 수습 중 모욕적 발언이 있어도, 핵심이 본채용 거부 적법성이면 `dismissal_validity` 또는 `work_ability`
- 괴롭힘 정황이 있어도, 판정 핵심이 절차 하자면 `procedure`

### 2-2. secondary는 사실 자체보다 “함께 등장한 법적 쟁점”만

예:
- `attendance`
- `misconduct`
- `evaluation`
- `procedure`
- `training_opportunity`

### 2-3. exclusion_flags로 과잉회수 방지

기존 legacy 태그가 붙어 있어도 실질 쟁점이 다르면 제외 플래그를 부여한다.

예:
- `not_really_harassment_case`
- `not_really_absence_case`
- `renewal_expectation_dominant`
- `resignation_dispute`
- `unrelated_to_probation`
- `procedure_dominant`

### 2-4. 검색 관점에서 재사용성 낮은 사건은 notes/exclusion으로 관리

예:
- 사실관계가 지나치게 짧음
- 특정 사정에 강하게 종속됨
- 표면 태그와 달리 실제 검색 효용이 낮음

---

## 3) enum 사전

## 3-1. employment_stage

- `probation`: 수습/시용/본채용 거부 단계
- `regular`: 일반 근로관계 진행 중
- `fixed_term`: 기간제 근로관계
- `renewal_stage`: 계약갱신/갱신기대권 단계
- `unknown`: 불명확

판정 기준:
- “시용기간 중 해고 / 본채용 거부 / 수습평가”가 핵심이면 `probation`
- 기간제 재계약/갱신기대권이 중심이면 `renewal_stage`
- 단순히 수습이라는 단어가 나오더라도 실질 쟁점이 갱신거절이면 `renewal_stage`

---

## 3-2. issue_type_primary

주된 쟁점 하나만 선택.

- `dismissal_validity`: 해고/근로관계 종료/부당해고 여부가 중심
- `work_ability`: 업무능력, 적격성, 성과 부진 자체가 중심
- `misconduct`: 비위행위 존재·중대성이 중심
- `procedure`: 절차 위반이 판정 핵심
- `disciplinary_severity`: 징계양정의 과다/상당성이 핵심
- `workplace_harassment`: 직장내 괴롭힘 성격의 행위가 핵심
- `renewal_expectation`: 갱신기대권 존부/갱신거절 합리성이 핵심
- `unfair_treatment`: 불이익취급/부당노동행위가 핵심

운용 메모:
- `misconduct`는 “비위 사실 인정 여부”가 핵심일 때
- `disciplinary_severity`는 비위 사실은 대체로 인정되고, 해고/정직/감봉 수위가 쟁점일 때
- `procedure`는 서면통지, 징계절차, 소명기회 등 절차 하자가 결론을 좌우할 때
- `workplace_harassment`는 반복적 폭언·지위 이용 괴롭힘 등 행위 유형 자체가 중심일 때

---

## 3-3. issue_type_secondary

보조 쟁점 다중 선택.

- `attendance`: 지각, 결근, 근태
- `absence_without_leave`: 무단이탈, 근무지 이탈
- `misconduct`: 폭언, 폭행, 지시불이행, 허위기재 등 일반 비위
- `work_ability`: 업무수행능력, 적응, 성과
- `performance`: 실적/성과 저조
- `evaluation`: 평가 기준, 평가자 구성, 평가점수
- `procedure`: 해고/징계 절차, 소명기회, 통지
- `training_opportunity`: 교육, 지도, 개선기회 부여 여부
- `worker_status`: 사용자 적격, 근로자성/지위 관련 쟁점
- `disciplinary_severity`: 징계 수준 문제
- `harassment_report`: 괴롭힘 신고와 불이익 여부
- `transfer_validity`: 전보 정당성
- `unfair_treatment`: 부당노동행위/불이익취급

주의:
- primary와 secondary가 중복될 수는 있으나, 가능하면 secondary는 primary를 보완하는 방향으로 최소화한다.

---

## 3-4. disposition_type

사건에서 다투는 인사처분/종료 형태.

- `dismissal`: 일반 해고
- `disciplinary_dismissal`: 징계해고
- `probation_termination`: 수습/시용기간 중 종료
- `rejection_of_regular_employment`: 본채용 거부
- `nonrenewal`: 계약갱신 거절
- `contract_termination`: 계약종료/계약만료 처리
- `no_formal_disposition`: 해고 부존재/사직 등으로 처분성 약함
- `suspension`: 정직
- `pay_cut`: 감봉
- `transfer`: 전보
- `other`: 기타

판정 팁:
- 시용기간 “중” 종료면 `probation_termination`
- 시용기간 “만료 후” 본채용 거부면 `rejection_of_regular_employment`
- 사직/합의해지 다툼이면 `no_formal_disposition` 또는 `contract_termination` 검토

---

## 3-5. fact_markers

사실관계 신호를 짧게 표시하는 보조 태그.

- `probation_period`: 수습/시용기간 관련
- `quantitative_evaluation`: 점수/등급 등 계량 평가 존재
- `qualitative_evaluation`: 정성 평가 중심
- `improvement_opportunity_given`: 개선기회 부여
- `written_notice`: 서면통지 존재
- `written_notice_missing`: 서면통지 흠결
- `evidence_sufficient`: 사용자 입증 충분
- `evidence_insufficient`: 사용자 입증 부족
- `procedural_defect`: 절차상 하자
- `short_tenure`: 극단적으로 짧은 근속기간
- `mutual_agreement`: 합의해지 정황
- `resignation_dispute`: 사직서 진정성/자발성 다툼
- `disciplinary_committee`: 징계위원회/인사위 존재
- `prior_sanction_history`: 기존 징계 전력
- `comparative_employee_case`: 형평 비교 대상 존재
- `harassment_report_filed`: 괴롭힘 신고 선행
- `unauthorized_absence`: 무단결근/무단이탈
- `witness_statement`: 진술증거 중심

원칙:
- 사실을 장황하게 다 적지 말고, 검색 필터로 쓸 만한 것만 남긴다.

---

## 3-6. legal_focus

판정문의 법리 포인트.

- `just_cause`: 정당한 이유 존재 여부
- `social_norm_reasonableness`: 사회통념상 상당성
- `procedural_due_process`: 절차적 정당성
- `evidentiary_sufficiency`: 입증 정도의 충분성
- `employer_burden_of_proof`: 사용자 입증책임
- `suitability_for_regular_employment`: 시용·본채용 적격성 판단
- `proportionality`: 비위와 징계수준의 비례성
- `appropriateness_of_discipline`: 징계양정 상당성
- `expectation_of_renewal`: 갱신기대권
- `protection_against_retaliation`: 신고/노조활동 등에 대한 불이익 금지

구분 팁:
- `proportionality` / `appropriateness_of_discipline`는 같이 붙는 경우가 많음
- 수습/시용 사건은 `suitability_for_regular_employment`가 중심 법리

---

## 3-7. industry_context

업종 맥락.

- `manufacturing`
- `service`
- `office`
- `healthcare`
- `finance`
- `public`
- `unknown`

원칙:
- 업종 특성이 판단에 의미 있을 때만 구체화
- 아니면 `unknown`

---

## 3-8. exclusion_flags

검색 노이즈 제어용 플래그.

- `not_really_harassment_case`: 폭언/갈등 언급은 있으나 실질은 괴롭힘 사건 아님
- `not_really_absence_case`: 결근 태그가 있으나 실질 쟁점은 다른 것
- `renewal_expectation_dominant`: 수습보다 갱신기대권 법리가 중심
- `settlement_or_mutual_termination`: 합의해지/화해 중심
- `resignation_dispute`: 사직 의사표시 효력이 핵심
- `unrelated_to_probation`: 표면상 수습이지만 수습 검색에는 노이즈
- `procedure_dominant`: 행위보다 절차 하자가 결정적
- `fact_specific_low_reusability`: 사실이 지나치게 짧거나 재사용성 낮음
- `evidence_too_thin`: 증거가 너무 빈약해 일반화 어려움
- `unrelated_to_dismissal`: 해고 검색에는 노이즈

중요:
- exclusion은 “삭제”가 아니라 “검색 정밀도 향상” 목적임

---

## 4) 배치별 운영 메모

### 4-1. probation_sample
- 핵심 분리축은 `probation_termination` vs `rejection_of_regular_employment`
- 수습이 붙어 있어도 실질이 갱신기대권/사직 다툼이면 exclusion 필요
- 평가 객관성, 서면통지, 개선기회가 자주 갈림포인트

### 4-2. violence_sample
- 폭행/폭언 사실 자체보다 `disciplinary_severity`가 primary인 경우가 많음
- 단순 폭언 언급만 있다고 violence 계열로 몰지 말 것
- 반복적 지위이용 폭언은 `workplace_harassment` 검토

### 4-3. workplace_bullying_sample
- “괴롭힘” 용어 유무보다 반복성, 지위 이용, 관계구조를 봄
- 신고 불이익/보복 문제는 `harassment_report` 또는 `unfair_treatment` 보조 검토

### 4-4. absence_sample
- 무단결근이 표면상 쟁점이어도 실제로는 절차, 비위 복합, 본채용 적격성 판단일 수 있음
- 진짜 결근 중심 사건만 남기고 나머지는 `not_really_absence_case` 고려

### 4-5. incompetence_sample
- legacy incompetence 태그는 실제로 평가, 절차, 수습, 징계와 혼재
- 업무능력 저조 자체가 핵심인지, 입증/평가 절차가 핵심인지 분리해야 함

---

## 5) confidence 기준

- `high`: 핵심 쟁점과 태그 매핑이 명확함
- `medium`: 사실관계가 간략하거나 경계선 사례
- `low`: 판정문 정보 부족, 다중 해석 가능성 큼

실무 원칙:
- 억지로 high 주지 말 것
- 경계선은 notes에 이유를 남길 것

---

## 6) review_status 기준

- `pending`: 초안 완료, 미검수
- `reviewed`: 사람 검수 완료

권장 흐름:
1. draft 생성
2. reviewed 폴더로 검수본 이동
3. merged에서 최종 병합

---

## 7) 현재까지 확인된 v1 성과

샘플 100건 기준:
- 기존 단일 태그 정확도 약 40%
- `exclusion_flags`로 과잉분류 제어 가능
- enum 범위 내 안정적 출력 확인
- 5개 배치 / 100건 초안 생성 완료
- `output/reviewed`, `output/merged`는 아직 비어 있음

---

## 8) 다음 작업 제안

1. `prompts/tagging_prompt_v1.md` 작성
   - 위 enum만 허용
   - primary 하나, secondary 다중 선택 규칙 명시

2. `prompts/review_checklist_v1.md` 작성
   - primary 과대포착 여부
   - exclusion 누락 여부
   - include/exclude query 품질 점검

3. `output/reviewed/` 검수 시작
   - probation, violence부터 우선 검수

4. 최종 병합 스키마 확정
   - reviewed → merged 변환 규칙 정의
