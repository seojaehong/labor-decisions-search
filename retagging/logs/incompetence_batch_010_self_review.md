# incompetence_batch_010_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, incompetence 배치
- 핵심 판별 기준: work_ability vs dismissal_validity 구별, 갱신기대권 혼입 감지

## 유형별 분류

### 시용/수습 본채용 거부 (18건) — 가장 다수
- 정당 판정: id_51659, id_52587, id_52795, id_55031, id_55233, id_56439, id_58019, id_58529, id_60401
- 부당 판정: id_51871, id_52811, id_52959, id_55987, id_57037, id_57135, id_60033
- 공통: issue_type_primary = dismissal_validity, disposition_type = rejection_of_regular_employment
- work_ability는 secondary로 배치 (본채용 거부 정당성 판단의 하위 요소)

### 갱신기대권 혼입 사건 (3건) — exclusion 처리
- id_51829: 기간제 갱신기대권+인사고과 미달 → primary=renewal_expectation, exclusion=renewal_expectation_dominant
- id_52869: 촉탁직 갱신기대권+업무수행능력 평가 → primary=renewal_expectation, exclusion=renewal_expectation_dominant
- id_56155: 고용승계 기대권+정년 도과 → primary=renewal_expectation, exclusion=renewal_expectation_dominant+not_really_performance_case
- 변경 이유: 업무능력 부족이 갱신거절의 합리적 사유로만 기능. work_ability 검색 시 상위 노출 부적절.

### 전보/배치변경 사건 (4건) — unrelated_to_dismissal
- id_52933, id_55563: 전직 인사명령 부존재 (초심+재심 동일 사건)
- id_53173: 근무조 변경 정당
- id_53431: 팀장→팀원 전보 부당
- 변경 이유: incompetence 배치이나 실질은 전보 정당성. exclusion=not_really_performance_case, unrelated_to_dismissal

### 징계양정 과다 사건 (4건) — not_really_performance_case
- id_53309, id_55643: 무단결근 징계면직 양정 과다 (초심+재심 동일 사건)
- id_57761: 징계사유 4개 중 2개만 인정, 해고 과다
- id_55695: 경력 허위기재+업무능력 부족 모두 불인정
- 변경 이유: 업무능력 부족은 부차적 징계사유이거나 불인정됨. 핵심은 징계양정/해고사유 정당성.

### 정규직 업무능력 부족 해고 (3건)
- id_54377: 평가 없이 일방 해지 → 부당
- id_57391: 객관적 근거 없음+서면통지 불충분 → 부당
- id_60677: 사용자 스스로 형식적 기재 인정 → 부당
- 이 3건은 work_ability가 해고 사유로 직접 다뤄지지만, primary는 dismissal_validity (해고 정당성 판단이 핵심 쟁점)

## 초심-재심 동일 사건 쌍
- id_52587 ↔ id_55031 (본채용 거부 정당, 초심유지)
- id_52933 ↔ id_55563 (전직 인사명령 부존재, 초심유지)
- id_53309 ↔ id_55643 (징계양정 과다, 초심유지)

## work_ability vs dismissal_validity 판별 기준
- **dismissal_validity를 primary로 선택한 이유**: 모든 사건에서 "업무능력 부족"은 해고/본채용거부/갱신거절의 *사유*이지 그 자체가 *쟁점*이 아님. 쟁점은 "그 사유로 한 해고/거부가 정당한가"임.
- **work_ability는 secondary**: 업무능력 부족이 해고 사유로 주장된 경우에만 secondary로 배치.
- **갱신기대권 사건은 renewal_expectation이 primary**: 갱신기대권 존부+갱신거절 합리성이 핵심이고, 업무능력은 합리성 판단의 하위 요소.

## 주의 사항
- id_52959: 시용근로자가 아닌 수습기간 정규직으로 판단된 사례. employment_stage=probation 유지하되 notes에 명기.
- id_57037: 평가 자체는 정당하나 서면통지의 구체성이 결정적. exclusion=procedure_dominant 부착.
- id_60033: 일회적 행위+서면통지 부족. exclusion=procedure_dominant 부착.
