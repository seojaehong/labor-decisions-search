# Candidate Scoring v2

## 목적

candidate 검색에서 recall과 precision을 분리하고, query-aware scoring을 문서화한다.

이 문서는 구현자가 score 계산을 바꾸지 않고도 왜 결과가 올라왔는지 추적할 수 있게 만드는 것이 목표다.

## 입력값

스코어는 다음 신호를 조합한다.

- query parser 결과
  - `query_scenario`
  - `intended_primary`
  - `intended_stage`
  - `intended_disposition`
  - `must_have_markers`
  - `penalized_markers`
- document tag
  - `issue_type_primary`
  - `employment_stage`
  - `disposition_type`
  - `fact_markers`
  - `legal_focus`
  - `exclusion_flags`
- fallback text
  - `reason_category`
  - `holding_points`
  - `holding_summary`

## Score Model

candidate score는 아래 4개 축으로 본다.

1. intent match
2. document coverage
3. penalty / exclusion
4. scenario bonus

### 1. Intent Match

- query의 `intended_primary`와 문서 `issue_type_primary`가 맞으면 가점
- query의 `intended_stage`와 `employment_stage`가 맞으면 가점
- query의 `intended_disposition`과 `disposition_type`가 맞으면 가점

기본 원칙:

- primary가 가장 중요하다.
- stage와 disposition은 보조 판별이다.
- primary가 맞는데 stage가 조금 어긋나는 경우는 완전 탈락이 아니라 감점만 한다.

### 2. Document Coverage

- `must_have_markers`가 문서의 `fact_markers` 또는 `legal_focus`에 포함되면 가점
- query가 요구한 핵심 사실이 문서에 실제로 드러나야 한다.

예:

- `absence_procedure`
  - `unauthorized_absence`
  - `written_notice_missing`
  - `procedural_due_process`
- `regular_work_ability`
  - `qualitative_evaluation`
  - `quantitative_evaluation`
  - `warning_given`
  - `improvement_opportunity_given`
  - `training_provided`
- `retaliation`
  - `harassment_report_filed`
  - `protection_against_retaliation`
- `severity_excessive`
  - `proportionality`
  - `appropriateness_of_discipline`

### 3. Penalty / Exclusion

- `penalized_markers`가 문서에 있으면 감점한다.
- exclusion은 사실상 강한 감점이다.

대표 예:

- `regular_work_ability`
  - `probation`
  - `rejection_of_regular_employment`
  - `nonrenewal`
- `absence_procedure`
  - `not_really_absence_case`
- `retaliation`
  - `workplace_harassment_only`
  - `union_activity_general_theory`
- `severity_excessive`
  - `dismissed`
  - `settled`
  - `no_relief_interest`

주의:

- `retaliation`은 “불이익 처우”가 아니라 “신고/노조활동 후 보복이 명시적으로 인정된 경우”에만 상위로 둔다.
- `unfair_treatment`와 `retaliation`은 다른 축이다.

### 4. Scenario Bonus

scenario가 명확할수록 bonus를 준다.

- `absence_procedure`
  - 절차 위반이 결론을 갈랐으면 bonus
- `regular_work_ability`
  - 정규직 저성과/업무능력 부족이 핵심이면 bonus
- `retaliation`
  - 신고 후 불이익 조치가 핵심이면 bonus
- `severity_excessive`
  - 징계사유는 인정되나 양정 과다가 핵심이면 bonus

## Recall -> Precision 규칙

### Recall 단계

넓게 회수한다.

- 8축 태그
- reason fallback
- exclusion filter

목표:

- 누락을 줄인다.
- 아직은 순도를 너무 일찍 희생하지 않는다.

### Precision 단계

query parser 결과와 문서 태그를 다시 맞춘다.

권장 우선순위:

1. `primary` 일치
2. `scenario` 일치
3. `stage/disposition` 보조 일치
4. `fact_markers/legal_focus` 확인
5. `penalty/exclusion` 제거

## Known Pitfalls

다음 과잉 패턴은 의도적으로 막아야 한다.

- `절차 언급`만 보고 `procedure`로 모두 올리는 경우
- `노조활동`을 전부 `retaliation`으로 보는 경우
- `비위행위`를 전부 `misconduct`로만 두지 못하고 다른 축으로 과잉 분해하는 경우
- `본채용 거부`와 `정규직 저성과`를 섞는 경우

## Local Model Hook

로컬 모델은 score를 직접 대체하지 않고 보조한다.

가능한 활용:

- scenario 판정 보조
- query-to-tag 보정
- top-N rerank justification
- similar-case explanation

불가능/보류:

- baseline 전체 대체
- final answer generation
- scoring rule의 단일 진실원천화

## Acceptance Notes

- Q2/Q4/Q7/Q8에서 score가 query scenario를 더 잘 반영해야 한다.
- `baseline 0건 / candidate 0건` 같은 shape drift는 없어야 한다.
- candidate top-5에는 query scenario와 무관한 사건이 상위로 많이 뜨면 안 된다.
- `why surfaced`는 검증용으로만 남기고 사용자 UI에는 숨긴다.

