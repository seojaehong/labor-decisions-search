# worker_status 수기 판단 메모

## 결론

현재 `worker_status`는 **근로자성 자체**와 아래 하위 쟁점이 섞여 있습니다.

- `근로자성 / 당사자적격`
- `상시근로자 수 5인 이상 적용대상`
- `시용/수습/본채용거부`
- `해고 존재 / 해고 절차`

따라서 지금처럼 `worker_status`를 하나의 browse/list reason으로 유지하면
실제 사용자가 기대하는 “근로자성 분쟁”보다 훨씬 넓고 이질적인 사건이 같이 보입니다.

## 샘플 읽고 난 판단

### 1. 유지로 타당한 것

- `근로기준법상 근로자에 해당하지 않아 구제신청의 당사자적격이 없다고 판정`
- `사용종속 관계에서 임금을 대가로 근로를 제공한 근로기준법상 근로자에 해당한다고 보기 어려움`
- `프리랜서들은 근로기준법상 근로자가 아니므로 ... 적용되지 않음`
- `도급/용역/위임 계약 형식보다 실질상 근로자성 판단`

이런 사건은 `worker_status` 정탐으로 보는 것이 맞습니다.

### 2. 유지가 애매하거나 과포함인 것

- `시용근로자에 대한 본채용 거부는 정당`
- `수습평가 결과 본채용 거부`
- `시용근로자 해당 여부`

이 문맥은 `probation`이 1차이고, `worker_status`는 보조 태그로만 붙는 편이 자연스럽습니다.
현재는 `근로자에 해당` 같은 문구 때문에 `worker_status` keep으로 남는 경우가 많습니다.

### 3. 검토필요로 남겨야 하는 것

- `상시근로자 수 5인 미만이어서 구제신청 대상이 아님`
- `상시근로자 수 5명 이상 여부`
- `사용자 적격`, `당사자 적격`만 있고 근로자성 직접 판단은 약한 사건

이건 완전히 제거할 문제는 아니지만, 사용자가 생각하는 “근로자성 분쟁”과도 다릅니다.
따라서 `worker_status` 안에서 별도 `eligibility/applicability` 하위 신호로 보는 쪽이 맞습니다.

### 4. 제거가 맞는 것

- `감봉`, `정직`, `징계양정이 과도`
- `전보`, `인사발령`, `대기발령`
- `직장내괴롭힘`, `성희롱`
- `일반 징계사유 존부`

이건 현재 payload의 `label_mismatch` 판단이 대체로 맞습니다.

## 규칙 수정 제안

### A. worker_status positive를 2단으로 나누기

#### strong_positive

- `근로자성`
- `근로기준법상 근로자`
- `근로자에 해당`
- `사용종속관계`
- `계약의 형식보다 실질`
- `임금을 목적으로`
- `지휘감독`
- `사업소득세`
- `4대보험`

이건 `worker_status` 유지 근거로 바로 사용

#### weak_positive

- `당사자적격`
- `상시근로자 수`
- `5인 미만`
- `사용자 적격`

이건 단독으로는 `worker_status keep`이 아니라 `needs_review`

### B. probation와의 분리

아래 문맥은 `probation` 우선으로 두고 `worker_status`는 보조 또는 제거 검토:

- `시용근로자`
- `수습`
- `본채용 거부`
- `수습평가`

특히 `근로자에 해당` 문구 하나만으로 `worker_status keep`이 되면 과포함이 심해집니다.

### C. no_dismissal / contract_expiry와의 분리

- `사직`, `합의해지`, `해고가 존재하지 않음`은 `no_dismissal`
- `갱신기대권`, `기간만료`, `갱신거절`은 `contract_expiry`

이 쪽이 주쟁점이면 `worker_status`는 보조 태그 또는 제거 검토가 맞습니다.

## 바로 적용하기 좋은 실무 규칙

1. `worker_status keep`
- strong_positive 1개 이상
- 그리고 `양정/전보/괴롭힘/성희롱` negative 없음
- 그리고 `probation / no_dismissal / contract_expiry` 주쟁점이 아님

2. `worker_status needs_review`
- weak_positive만 있고 strong_positive 없음
- 또는 strong_positive와 `probation/no_dismissal/contract_expiry`가 같이 강하게 나옴

3. `worker_status remove`
- strong_positive 없음
- negative만 강함

## 다음 작업 제안

1. `worker_status`를 다시 세분화
- `worker_status_core`
- `eligibility_or_applicability`

2. 최소한 browse/list에서는
- `worker_status_core` 기준으로만 노출
- `상시근로자 수 / 5인 미만 / 당사자적격`만 있는 사건은 `needs_review`로 후순위

3. `probation`과 충돌하는 사건은
- 기본 browse/list에서는 `probation` 쪽으로 보내는 것이 더 자연스럽습니다.
