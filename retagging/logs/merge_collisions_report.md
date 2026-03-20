# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 17:36
충돌 건수: 7건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_14663

소스 A: absence_batch_005_reviewed.jsonl
소스 B: incompetence_batch_001_reviewed.jsonl

충돌 필드: industry_context
  A: "healthcare"
  B: "unknown"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 2. id_11473

소스 A: absence_batch_001_reviewed.jsonl
소스 B: probation_batch_001_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "work_ability"

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---

## 3. id_13323

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: probation_batch_003_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "work_ability"

---

## 4. id_13583

소스 A: absence_batch_004_reviewed.jsonl
소스 B: probation_batch_003_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "misconduct"

---

## 5. id_14469

소스 A: absence_batch_005_reviewed.jsonl
소스 B: probation_batch_004_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "misconduct"

충돌 필드: industry_context
  A: "unknown"
  B: "office"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["probation_termination"]

---

## 6. id_14493

소스 A: absence_batch_005_reviewed.jsonl
소스 B: probation_batch_004_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "work_ability"

충돌 필드: industry_context
  A: "unknown"
  B: "service"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["rejection_of_regular_employment"]

---

## 7. id_16547

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: probation_batch_005_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "work_ability"

충돌 필드: disposition_type
  A: ["probation_termination"]
  B: ["rejection_of_regular_employment"]

---

# 수동 검토 최종 판정 (2026-03-20, 1차 bulk)

## 1. id_14663 최종안
- `issue_type_primary`: disciplinary_severity
- `employment_stage`: regular
- `disposition_type`: ["disciplinary_dismissal"]
- `industry_context`: healthcare
- 근거: 근무태만·업무능력 부족·직원 다툼 등 징계사유 인정되나, 사직권고 3회·전보 검토 없이 해고에 이른 점에서 양정 과다가 핵심 판단구조. 의료/조리 분야이므로 healthcare. 징계사유 전제 해고이므로 disciplinary_dismissal.

## 2. id_11473 최종안
- `issue_type_primary`: dismissal_validity
- `employment_stage`: probation
- `disposition_type`: ["rejection_of_regular_employment"]
- `industry_context`: service
- 근거: 시용근로자 여부 + 본채용 거부 정당성이 중심. 업무능력 자체보다 "시용근로자인지 → 본채용 거부가 정당한지" 법적 구조가 핵심.

## 3. id_13323 최종안
- `issue_type_primary`: dismissal_validity
- `employment_stage`: regular
- `disposition_type`: ["dismissal"]
- `industry_context`: manufacturing
- 근거: 선결쟁점이 "수습기간 만료 후 정식근로자 신분인지"이고, 정식근로자 확인 후 해고 정당성 판단. 이미 정식 전환된 상태에서의 해고이므로 regular + dismissal_validity.

## 4. id_13583 최종안
- `issue_type_primary`: dismissal_validity
- `employment_stage`: probation
- `disposition_type`: ["rejection_of_regular_employment"]
- `industry_context`: transport
- 근거: 시용근로자 확인 후, 잦은 결근·승무계획 거부가 본채용 거절의 합리적 이유인지 판단. 핵심은 본채용 거부 정당성. 승무직 → transport.

## 5. id_14469 최종안
- `issue_type_primary`: disciplinary_severity
- `employment_stage`: probation
- `disposition_type`: ["probation_termination"]
- `industry_context`: education
- 근거: 징계사유 6개 중 4개 인정 + 절차 적법 후, 수습기간 중 해고 양정 적정성이 핵심. 비위 존부보다 양정 판단이 결론 좌우. 교육기관. 수습 중도 해고이므로 probation_termination.

## 6. id_14493 최종안
- `issue_type_primary`: dismissal_validity
- `employment_stage`: probation
- `disposition_type`: ["rejection_of_regular_employment"]
- `industry_context`: service
- 근거: 업무범위(시설관리) 설명 부재 + 계약서 미명시가 핵심. 업무적격성 자체보다 "해고사유로 삼은 업무범위가 계약 내용인지"가 판정 좌우. 관리소 → service.

## 7. id_16547 최종안
- `issue_type_primary`: dismissal_validity
- `employment_stage`: probation
- `disposition_type`: ["rejection_of_regular_employment"]
- `industry_context`: unknown
- 근거: 수습근로자 여부 확인 + 본채용 거부 정당성 판단이 핵심. work_ability보다 dismissal_validity가 판정의 실질 프레임.

## 판정 패턴 요약
- dismissal_validity vs work_ability (4건): 모두 "해고/본채용거부의 법적 정당성"이 판정 프레임 → dismissal_validity
- disciplinary_severity vs misconduct (2건): 비위 존부가 아니라 양정 과다가 결론 좌우 → disciplinary_severity
- dismissal vs disciplinary_dismissal: 징계사유 전제 해고 → disciplinary_dismissal, 해고 존재 다툼 → dismissal
- rejection vs probation_termination: 수습 만료 시 본채용 거부 → rejection, 수습 중도 해고 → probation_termination

