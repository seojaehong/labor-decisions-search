# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 18:36
충돌 건수: 6건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_18321

소스 A: absence_batch_009_reviewed.jsonl
소스 B: probation_batch_006_reviewed.jsonl

충돌 필드: employment_stage
  A: "renewal_stage"
  B: "fixed_term"

---

## 2. id_23379

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_009_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "service"

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

---

## 3. id_2345

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_009_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "office"

---

## 4. id_17909

소스 A: absence_batch_009_reviewed.jsonl
소스 B: violence_batch_008_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 5. id_1807

소스 A: absence_batch_009_reviewed.jsonl
소스 B: violence_batch_008_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "absence_without_leave"
  B: "misconduct"

---

## 6. id_19645

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: violence_batch_009_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "misconduct"

---

