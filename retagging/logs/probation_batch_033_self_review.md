# probation_batch_033 Self-Review

## 배치 개요
- **입력 건수**: 14건
- **출력 건수**: 14건
- **작업일**: 2026-03-20

## 분류 요약

| 유형 | 건수 | case_id |
|------|------|---------|
| 본채용 거부 정당 (기각/초심유지) | 9 | id_402625, id_402627, id_402675, id_402725, id_402743, id_402819, id_402849, id_403051, id_403109 |
| 본채용 거부 부당 (인용) | 2 | id_402635, id_402865 |
| 해고 부존재 (사직) | 2 | id_403099, id_403119 |
| 구제이익 부존재 (비수습) | 1 | id_402943 |

## rejection vs termination 판단

| case_id | disposition_type | 판단 근거 |
|---------|-----------------|-----------|
| id_402625 | rejection_of_regular_employment | 시용계약 명시, 본채용 여부 결정 구조 |
| id_402627 | rejection_of_regular_employment | 인사복무규정상 수습=시용, 채용 확정 점수 기준 |
| id_402635 | rejection_of_regular_employment | 시용기간 중 평가절차 위반한 본채용 거부 |
| id_402675 | rejection_of_regular_employment | 시용근로자 본채용 거부 |
| id_402725 | rejection_of_regular_employment | 수습기간 업무능력 확인 후 본채용 결정 구조 |
| id_402743 | rejection_of_regular_employment | 수습평가 기준 미달로 본채용 거부 |
| id_402819 | rejection_of_regular_employment | 평가 미달 + 겸직금지 위반 복합 사유 |
| id_402849 | rejection_of_regular_employment | 2차 수습평가 현저 미달 |
| id_402865 | rejection_of_regular_employment | 수습기간 조기 종료 통보 (절차 위반) |
| id_402943 | contract_termination | 단기 계약직으로 계약기간 만료 — **비수습** |
| id_403051 | rejection_of_regular_employment | 80일 평가 결과 기준 미달 |
| id_403099 | no_formal_disposition | 사직원 제출로 해고 부존재 |
| id_403109 | rejection_of_regular_employment | 공무직 수습평가 60점 기준 미달 |
| id_403119 | no_formal_disposition | 본채용 거부 예고 후 근로자 조기 퇴사 — 사직 |

## 비수습(unrelated_to_probation) 판정

- **id_402943**: 채용공고에 단기 계약직 상담원 모집으로 명시. 동일 기수 전원 계약기간 만료 퇴사. 시용관계 형성 여부와 무관하게 계약기간 도과 후 구제신청이라 구제이익 부존재. employment_stage를 fixed_term으로 변경, exclusion_flags에 unrelated_to_probation 부여.

## 해고 부존재 (resignation_dispute) 판정

- **id_403099**: 수습평가 2회 결과 본채용 불가를 인지한 상태에서 자필 사직원 제출. 진의 아닌 의사표시·강요 주장 배척. 수습이 배경이나 핵심 쟁점은 사직 자발성.
- **id_403119**: 수습기간 만료 본채용 거부 예고 후 근로자가 이직처 확보하여 예정일(10.15)보다 먼저(9.30) 퇴사. 근로기간 단축은 근로자 의사. 재심 초심유지.

## 특이 사항 및 주의점

1. **id_402627**: 경영위임계약에 의한 당사자적격 판단이 포함된 복합 쟁점. 복지관 운영 위탁 구조.
2. **id_402635**: 자체 정한 2회 평가를 18일만에 1회로 단축한 절차 위반이 결정적. issue_type_primary를 procedure로 설정.
3. **id_402819**: 겸직금지 위반이라는 misconduct 요소가 평가 미달과 복합. secondary에 misconduct 포함.
4. **id_402849**: IT 업종, Job Offer 단계부터 수습 명시, 위키 페이지 안내 등 사전 고지 충실.
5. **id_402943**: 레거시 태그에 probation이 있으나 실질은 단기 계약직. employment_stage 변경 필요.
6. **id_403109**: 60점 기준에 59.2점(0.8점 차이)으로 경계선 사례이나 절차적 정당성이 인정됨.

## 신뢰도 분포

| confidence | 건수 |
|-----------|------|
| high | 13 |
| medium | 1 (id_402675 — 원문이 요약형) |

## 검증 완료
- 모든 필드가 tagging-schema-v1.json 허용값 범위 내 확인
- review_status: 전건 "pending"
- tag_version: 전건 "v1"
