# Predicted Collision Patterns

- 작성시각: 2026-03-20 21:47
- 목적: Claude가 남은 `absence/violence/workplace_bullying` 구간을 계속 생산할 때, 기존 corpus와 충돌이 많이 날 패턴을 미리 정리
- 전제: Claude rear 031~033 스타일을 통일 기준으로 가정

## 핵심 결론

앞으로의 충돌은 "형식 오류"보다 아래 4개 경계쌍에서 집중될 가능성이 높다.

1. `misconduct` vs `disciplinary_severity`
2. `dismissal_validity` vs `procedure`
3. `dismissal_validity` vs `worker_status`
4. topic legacy (`absence`, `violence`, `workplace_bullying`) vs 실제 판정축

## 1. absence 계열

가장 흔한 충돌 예상:

- `absence_without_leave` vs `misconduct`
- `absence_without_leave` vs `disciplinary_severity`
- `absence_without_leave` vs `dismissal_validity`

예상 이유:

- Claude 기준은 "무단결근이 핵심이 아닐 때" `not_really_absence_case`를 적극 사용한다.
- 기존 Codex/초기 산출물은 결근 사실이 있으면 absence 축으로 끌려갈 가능성이 더 높다.

일괄 판정 규칙 초안:

- 결근이 여러 비위 중 하나면 `misconduct`
- 결근 인정은 되지만 결론이 양정 과다/정직 과다이면 `disciplinary_severity`
- 해고 존재, 해고 부존재, 복직명령, 구제이익 소멸이 중심이면 `dismissal_validity`
- 이런 경우 `not_really_absence_case`를 같이 유지

## 2. violence 계열

가장 흔한 충돌 예상:

- `misconduct` vs `disciplinary_severity`
- `violence` 성격 레거시 인상 vs 실제 `dismissal_validity`
- `workplace_harassment` vs `disciplinary_severity`

예상 이유:

- 폭행/폭언 사실이 있어도 위원회 판단 중심이 징계양정인 사건이 많다.
- Claude rear는 violence batch에서도 `disciplinary_severity`를 가장 많이 택했다.

일괄 판정 규칙 초안:

- 폭행 사실 인정 자체보다 "해고/정직 수위가 과한가"가 중심이면 `disciplinary_severity`
- 폭행은 징계사유 중 하나일 뿐이면 `misconduct`
- 실질 쟁점이 부당노동행위, 전보, 절차이면 violence primary를 피하고 exclusion flag로 정리

## 3. workplace_bullying 계열

가장 흔한 충돌 예상:

- `workplace_harassment` vs `disciplinary_severity`
- `workplace_harassment` vs `transfer_validity`
- `workplace_harassment` vs `dismissal_validity`

예상 이유:

- 괴롭힘 allegations가 사건 배경일 뿐, 실제 판정은 전보/징계/해고 정당성인 경우가 많다.
- Claude rear는 bullying batch에서도 `disciplinary_severity` 31건, `workplace_harassment` 24건으로 분리해 둠.

일괄 판정 규칙 초안:

- 괴롭힘 성립 여부 자체가 결론이면 `workplace_harassment`
- 성립 여부는 전제이고 징계 수위가 핵심이면 `disciplinary_severity`
- 괴롭힘 신고 후 전보/불이익 배치가 핵심이면 `transfer_validity` 또는 `unfair_treatment`
- 배경 사건이면 `not_really_harassment_case`를 보조로 남김

## 4. probation 교차 충돌

기존 probation 015~030을 보면 다음 두 패턴이 이미 과대표집되어 있다.

- `worker_status` primary 과다
- `procedure` primary 과다

따라서 앞으로 교차 merge에서 자주 맞붙을 축:

- `worker_status` vs `dismissal_validity`
- `procedure` vs `dismissal_validity`
- `procedure` vs `work_ability`

보수 규칙:

- status는 법적 지위 자체가 결론일 때만 primary
- procedure는 절차 흠결이 유일한 결론축일 때만 primary
- 그 외에는 `dismissal_validity` 또는 `work_ability`를 primary로 두고 secondary/flag로 보조

## 통합 운영 기준

한 사람이 끝까지 한 것처럼 보이게 하려면, 앞으로 충돌 판정도 아래 순서로 밀어붙이는 게 좋다.

1. 배치명보다 위원회의 실제 결론축을 먼저 읽기
2. topic mismatch는 primary를 억지로 맞추지 말고 exclusion flag로 처리
3. `worker_status`, `procedure`, `medium`은 보수적으로 쓰기
4. 징계사건은 "사유 인정"과 "양정 과다"를 분리하기
5. 본채용거부/수습 종료는 status보다 `dismissal_validity` 프레임을 우선 검토하기

## 우선 감시할 충돌 후보군

- absence 배치에서 `misconduct`와 `absence_without_leave`가 함께 보이는 사건
- violence/bullying 배치에서 `disciplinary_severity`와 `misconduct`가 함께 보이는 사건
- bullying 배치에서 `transfer_validity`, `unfair_treatment`, `workplace_harassment`가 경쟁하는 사건
- probation 관련 사건에서 `worker_status`, `procedure`, `dismissal_validity`가 동시에 붙은 사건

## Observed QA Snapshot (2026-03-20 22:06)

- 범위: `absence, violence, workplace_bullying` / `batch_015~017`

- `misconduct` vs `disciplinary_severity`: 91건
  사례: `id_22839`, `id_22913`, `id_22973`, `id_23003`, `id_23547`, `id_24565`, `id_24571`, `id_24667`
- `dismissal_validity` vs `procedure`: 9건
  사례: `id_22851`, `id_24281`, `id_24323`, `id_24749`, `id_24965`, `id_24543`, `id_24577`, `id_402045`
- `dismissal_validity` vs `worker_status`: 2건
  사례: `id_22873`, `id_23407`
- topic legacy vs 실제 판정축: 96건
  사례: `id_22839`, `id_22851`, `id_22873`, `id_22913`, `id_22945`, `id_24693`, `id_24699`, `id_24839`
