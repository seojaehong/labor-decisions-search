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

