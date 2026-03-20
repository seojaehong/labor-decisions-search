# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 19:20
충돌 건수: 9건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_21607

소스 A: absence_batch_013_reviewed.jsonl
소스 B: probation_batch_008_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---

## 2. id_28511

소스 A: incompetence_batch_003_reviewed.jsonl
소스 B: probation_batch_013_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

충돌 필드: industry_context
  A: "office"
  B: "service"

---

## 3. id_29041

소스 A: incompetence_batch_003_reviewed.jsonl
소스 B: probation_batch_013_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

충돌 필드: industry_context
  A: "unknown"
  B: "healthcare"

---

## 4. id_29137

소스 A: incompetence_batch_003_reviewed.jsonl
소스 B: probation_batch_013_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "misconduct"
  B: "dismissal_validity"

충돌 필드: industry_context
  A: "service"
  B: "transport"

---

## 5. id_21523

소스 A: absence_batch_013_reviewed.jsonl
소스 B: violence_batch_011_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "absence_without_leave"
  B: "misconduct"

---

## 6. id_21785

소스 A: absence_batch_013_reviewed.jsonl
소스 B: violence_batch_011_reviewed.jsonl

충돌 필드: industry_context
  A: "education"
  B: "unknown"

---

## 7. id_22869

소스 A: probation_batch_009_reviewed.jsonl
소스 B: violence_batch_013_reviewed.jsonl

충돌 필드: disposition_type
  A: ["probation_termination", "suspension"]
  B: ["suspension", "reprimand", "probation_termination"]

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "disciplinary_severity"

---

## 8. id_23179

소스 A: probation_batch_009_reviewed.jsonl
소스 B: violence_batch_013_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "misconduct"

충돌 필드: industry_context
  A: "education"
  B: "unknown"

---

## 9. id_23447

소스 A: probation_batch_009_reviewed.jsonl
소스 B: violence_batch_013_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "misconduct"

---

