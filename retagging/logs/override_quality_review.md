# Override Quality Review

- 작성시각: 2026-03-20 21:47
- 범위: `output/reviewed/manual_merge_overrides_v1.json`
- 총량: 130건
- 원칙: override 파일 직접 수정 금지, 품질 점검과 재검토 우선순위만 제안

## 요약

- override는 현재 전반적으로 "자동 merge가 놓친 핵심 프레임"을 보정하는 역할을 잘 수행하고 있다.
- 수정 필드 상위는 `issue_type_primary` 71건, `industry_context` 64건, `disposition_type` 38건, `employment_stage` 14건이다.
- 즉, 충돌의 중심은 단순 포맷 문제가 아니라 "핵심 사건 프레임"과 "산업 맥락" 불일치다.

## 좋은 점

- `disciplinary_severity` vs `misconduct` 구분, `dismissal` vs `disciplinary_dismissal` 보정, `probation` 관련 법적 프레임 보정이 구체적 사유와 함께 적혀 있어 품질이 좋다.
- 최근 PM 판정분은 대부분 case-specific reason이 붙어 있어 재검증 가능성이 높다.

## 우선 재확인 대상

아래 11건은 reason이 `자동 판정` 또는 `원본 정보 부족` 계열이라, 향후 시간이 나면 원문 대조 우선순위로 삼는 편이 좋다.

| case_id | 현재 override | reason | 코멘트 |
|---|---|---|---|
| id_19187 | `industry_context=service` | 수습/시용 사건, 자동 판정 | 산업맥락이 사건 구조에서 직접 드러나지 않으면 generic service 고정은 보수 검토 필요 |
| id_25071 | `industry_context=service` | 수습/시용 사건, 자동 판정 | 동일 패턴 |
| id_20925 | `industry_context=service` | 수습/시용 사건, 자동 판정 | 동일 패턴 |
| id_21117 | `industry_context=service` | 수습/시용 사건, 자동 판정 | 동일 패턴 |
| id_21121 | `industry_context=unknown` | 원본 정보 부족, unknown 유지 | 유지 가능하나 source 확인 전까지는 low-evidence bucket으로 관리 권장 |
| id_21165 | `industry_context=service` | 수습/시용 사건, 자동 판정 | 동일 패턴 |
| id_20441 | `industry_context=unknown` | 원본 정보 부족 | 동일 |
| id_20589 | `industry_context=unknown` | 원본 정보 부족 | 동일 |
| id_21607 | `industry_context=unknown` | 자동 판정 | 자동 판정 사유를 조금 더 구체화하면 추후 검증이 쉬움 |
| id_28511 | `industry_context=unknown` | 자동 판정 | 동일 |
| id_23447 | `industry_context=unknown` | 자동 판정 | 동일 |

## 패턴 해석

### 1. 가장 많이 손대는 필드가 `issue_type_primary`

- 자동 merge가 secondary/notes를 충분히 읽지 못하고 대표 프레임을 과격하게 선택하는 경우가 많다는 뜻이다.
- 특히 아래 경계쌍이 반복된다.
  - `dismissal_validity` vs `work_ability`
  - `misconduct` vs `disciplinary_severity`
  - `workplace_harassment` vs `disciplinary_severity`

### 2. `industry_context` override 비중이 높음

- 현행 태깅에서는 산업맥락이 source text의 얕은 단서에 크게 의존하는 것으로 보인다.
- 앞으로도 merge collision보다 "원문 빈약 + 산업맥락 추정" 충돌이 잔존할 가능성이 높다.

### 3. `disposition_type` 보정은 의미가 큼

- `dismissal`과 `disciplinary_dismissal`, `rejection_of_regular_employment`, `probation_termination`의 혼선은 검색 품질에 직접 영향을 준다.
- 이 필드는 override 우선순위를 계속 높게 둘 가치가 있다.

## 제안

- override 품질 자체는 나쁘지 않다. 다만 `자동 판정`, `원본 정보 부족` 사유는 별도 watchlist로 분리해 두는 편이 좋다.
- 다음 라운드에서는 위 11건처럼 low-evidence override를 먼저 원문 대조 대상으로 잡고,
  나머지 case-specific reason override는 현 상태 유지가 합리적이다.
