# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 19:06
충돌 건수: 6건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_19187

소스 A: absence_batch_011_reviewed.jsonl
소스 B: probation_batch_006_reviewed.jsonl

충돌 필드: employment_stage
  A: "probation"
  B: "renewal_stage"

충돌 필드: disposition_type
  A: ["nonrenewal", "rejection_of_regular_employment"]
  B: ["nonrenewal"]

---

## 2. id_25071

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_011_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---

## 3. id_20925

소스 A: probation_batch_007_reviewed.jsonl
소스 B: violence_batch_011_reviewed.jsonl

충돌 필드: disposition_type
  A: ["disciplinary_dismissal"]
  B: ["disciplinary_dismissal", "probation_termination"]

---

## 4. id_21117

소스 A: probation_batch_008_reviewed.jsonl
소스 B: violence_batch_011_reviewed.jsonl

충돌 필드: disposition_type
  A: ["no_formal_disposition"]
  B: ["dismissal"]

---

## 5. id_21121

소스 A: probation_batch_008_reviewed.jsonl
소스 B: violence_batch_011_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "disciplinary_severity"

---

## 6. id_21165

소스 A: probation_batch_008_reviewed.jsonl
소스 B: violence_batch_011_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "misconduct"

충돌 필드: disposition_type
  A: ["rejection_of_regular_employment"]
  B: ["probation_termination", "rejection_of_regular_employment"]

---

