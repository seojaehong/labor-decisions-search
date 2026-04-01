# worker_status 시범 정제 기준

## 유지 기준
- `근로자성`, `근로자에 해당`, `근로기준법상 근로자`, `당사자적격`, `사용종속관계`, `종속적 관계`, `종속관계` 직접 표현이 있는 경우 유지
- `계약의 형식보다 실질`, `고용계약인지 도급계약인지`, `임금을 목적으로`, `지휘감독`, `출퇴근`, `사업소득세`, `4대보험`처럼 근로자성 판단 문맥이 있는 경우 유지

## 제거 우선 기준
- `도급`, `위임계약`, `운영계약`, `파견`이 있어도 근로자성 판단 문맥이 없으면 제거 후보로 분류
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