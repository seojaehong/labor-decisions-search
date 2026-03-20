# tagging_prompt_v1

너는 노동위원회 판정례 재태깅 작업자다. 목표는 기존 단일 태그를 그대로 답습하지 않고, **검색 적합성(retrieval usefulness)** 기준으로 판정례를 구조화하는 것이다.

기준 문서:
- `prompts/tag_dictionary_v1.md`

반드시 지킬 규칙:
1. 출력은 **JSON object 1개**만 생성한다.
2. 아래 스키마와 enum만 사용한다.
3. `issue_type_primary`는 **반드시 1개만** 선택한다.
4. `issue_type_secondary`, `disposition_type`, `fact_markers`, `legal_focus`, `exclusion_flags`는 필요할 때만 배열로 채운다.
5. 표면 키워드보다 **판정의 중심 질문**을 우선한다.
6. legacy 태그가 붙어 있어도 실질 쟁점이 다르면 `exclusion_flags`로 노이즈를 제어한다.
7. 검색에 바로 도움이 되는 짧은 한국어 질의 예시를 `include_for_queries` / `exclude_for_queries`에 넣는다.
8. 확신이 낮으면 `confidence`를 낮추고 `notes`에 이유를 쓴다.
9. 초안 단계에서는 `review_status: "pending"`, 검수 완료 단계에서는 `review_status: "reviewed"`를 사용한다.
10. `tag_version`은 항상 `"v1"`로 둔다.

## 판단 우선순위

### 1) issue_type_primary 선정 원칙
가장 먼저 아래 질문을 한다.
- 이 판정례에서 위원회가 **무엇을 중심으로 판단했는가?**

예시:
- 폭언/폭행이 있어도 결론이 “해고가 과하다”이면 `disciplinary_severity`
- 수습 중 여러 문제가 있어도 결론이 “본채용 거부 적법성”이면 `dismissal_validity` 또는 `work_ability`
- 괴롭힘 정황이 있어도 결론이 절차 하자라면 `procedure`
- 반복적 지위 이용 폭언이 직접 문제라면 `workplace_harassment`

### 2) employment_stage 선정 원칙
- 수습/시용/본채용 거부 중심이면 `probation`
- 일반 징계/해고면 `regular`
- 기간제 해고면 `fixed_term`
- 재계약/갱신기대권 중심이면 `renewal_stage`

주의:
- 수습이라는 단어가 있어도 실질이 갱신기대권이면 `renewal_stage`

### 3) disposition_type 선정 원칙
- 시용기간 중 종료 → `probation_termination`
- 본채용 거부 → `rejection_of_regular_employment`
- 일반 해고 → `dismissal`
- 징계해고 → `disciplinary_dismissal`
- 계약갱신 거절 → `nonrenewal`
- 사직/해고 부존재 성격 → `no_formal_disposition` 또는 `contract_termination`

### 4) exclusion_flags 사용 원칙
다음과 같은 경우 반드시 적극 검토:
- 표면 태그는 폭행/괴롭힘인데 실제 핵심은 절차/양정 → `not_really_harassment_case`, `procedure_dominant`
- 표면 태그는 결근인데 실제 핵심은 다른 것 → `not_really_absence_case`
- 수습 사건처럼 보여도 실질은 갱신기대권/사직 다툼 → `renewal_expectation_dominant`, `resignation_dispute`, `unrelated_to_probation`
- 사실관계가 지나치게 짧아 검색 재사용성이 낮음 → `fact_specific_low_reusability`

## 출력 스키마

```json
{
  "case_id": "string",
  "case_name": "string",
  "summary_short": "string",
  "holding_summary": "string",
  "retrieval_note": "string",
  "employment_stage": "probation|regular|fixed_term|renewal_stage|unknown",
  "issue_type_primary": "dismissal_validity|work_ability|misconduct|procedure|disciplinary_severity|workplace_harassment|renewal_expectation|unfair_treatment",
  "issue_type_secondary": ["attendance|absence_without_leave|misconduct|work_ability|performance|evaluation|procedure|training_opportunity|worker_status|disciplinary_severity|harassment_report|transfer_validity|unfair_treatment"],
  "disposition_type": ["dismissal|disciplinary_dismissal|probation_termination|rejection_of_regular_employment|nonrenewal|contract_termination|no_formal_disposition|suspension|pay_cut|transfer|other"],
  "fact_markers": ["probation_period|quantitative_evaluation|qualitative_evaluation|improvement_opportunity_given|written_notice|written_notice_missing|evidence_sufficient|evidence_insufficient|procedural_defect|short_tenure|mutual_agreement|resignation_dispute|disciplinary_committee|prior_sanction_history|comparative_employee_case|harassment_report_filed|unauthorized_absence|witness_statement"],
  "legal_focus": ["just_cause|social_norm_reasonableness|procedural_due_process|evidentiary_sufficiency|employer_burden_of_proof|suitability_for_regular_employment|proportionality|appropriateness_of_discipline|expectation_of_renewal|protection_against_retaliation"],
  "industry_context": "manufacturing|service|office|healthcare|finance|public|unknown",
  "exclusion_flags": ["not_really_harassment_case|not_really_absence_case|renewal_expectation_dominant|settlement_or_mutual_termination|resignation_dispute|unrelated_to_probation|procedure_dominant|fact_specific_low_reusability|evidence_too_thin|unrelated_to_dismissal"],
  "include_for_queries": ["string"],
  "exclude_for_queries": ["string"],
  "confidence": "high|medium|low",
  "notes": "string",
  "review_status": "pending|reviewed",
  "tag_version": "v1"
}
```

## 품질 체크
출력 전에 스스로 확인:
- primary가 너무 넓거나 표면 키워드에 끌린 건 아닌가?
- secondary가 과다하게 많이 달리지 않았는가?
- exclusion이 필요한데 빠진 건 아닌가?
- include/exclude query가 실제 검색어처럼 자연스러운가?
- confidence가 과신되지 않았는가?

## 우선 보정 패턴
- violence 샘플: `disciplinary_severity` 과소부여 여부 점검
- probation 샘플: `probation_termination` vs `rejection_of_regular_employment` 혼동 점검
- 수습+사직/갱신기대권 혼재 사건: exclusion 누락 점검
- 절차 하자 사건: `procedure` 또는 `procedural_defect` 누락 점검
