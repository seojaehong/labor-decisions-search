# Search Purity v2 Strict

## 목적

잔여 purity 이슈가 남은 질의에 대해 recall을 크게 희생하지 않으면서 precision을 높인다.

대상 질의:

- `Q4` 괴롭힘 신고 후 보복
- `Q7` 정규직 저성과 / 업무능력 부족

## 전략

### 1. strict scenario는 query-aware penalty를 더 강하게 적용

`regular_work_ability`

- `probation`
- `rejection_of_regular_employment`
- `nonrenewal`
- `해고가 존재하지 않음`
- `사직서 제출`
- `복직명령`

이런 noise는 강하게 감점한다.

`retaliation`

- `전보 일반론`
- `정당한 징계 일반론`
- `괴롭힘 성립 사건 일반론`
- `노조/쟁의행위 일반론`

이런 문서는 보복 구조가 명시되지 않으면 감점한다.

### 2. dev-only 관측성

개발 모드에서만 아래를 노출한다.

- scenario
- candidate top ids
- candidate top score reasons

사용자 UI에는 계속 비노출한다.

## 기대 효과

- `Q7`에서 `probation / nonrenewal / no_dismissal` 혼입 감소
- `Q4`에서 `transfer_validity 일반론 / misconduct 일반론` 혼입 감소
- 라이브 검증 시 노이즈 원인을 더 빠르게 확인 가능
