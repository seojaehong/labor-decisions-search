# worker_status 시범 정제 기준

## 유지 기준
- `근로자성`, `근로자에 해당`, `근로기준법상 근로자`, `당사자적격`, `사용종속관계`, `종속적 관계`, `종속관계` 직접 표현이 있는 경우 유지

## 제거 우선 기준
- `도급`, `위임계약`, `운영계약`만 있고 근로자성 직접 표현이 없는 경우
- `파견`, `근로자파견`만 있고 근로자성 직접 표현이 없는 경우
- `전보`, `인사발령`, `배치전환`, `대기발령` 중심 사건
- `양정`, `과도`, `과중`, `비례원칙`, `감봉`, `정직` 중심 징계양정 사건
- `직장내괴롭힘`, `괴롭힘`, `성희롱` 중심 사건

## 확장 순서
1. worker_status
2. contract_expiry / probation / no_dismissal
3. transfer / incompetence
4. misconduct / violence / embezzlement
5. workplace_bullying / sexual_harassment
6. union_activity / discrimination / redundancy