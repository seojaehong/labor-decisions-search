# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 18:07
충돌 건수: 6건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_19041

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: probation_batch_006_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "work_ability"

충돌 필드: industry_context
  A: "unknown"
  B: "transport"

---

## 2. id_19061

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: probation_batch_006_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "finance"

---

## 3. id_19179

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: probation_batch_006_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "misconduct"

충돌 필드: industry_context
  A: "unknown"
  B: "public"

---

## 4. id_19235

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: probation_batch_006_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "retail"

---

## 5. id_16613

소스 A: probation_batch_005_reviewed.jsonl
소스 B: violence_batch_006_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "misconduct"

충돌 필드: employment_stage
  A: "probation"
  B: "regular"

---

## 6. id_16649

소스 A: probation_batch_005_reviewed.jsonl
소스 B: violence_batch_006_reviewed.jsonl

충돌 필드: industry_context
  A: "office"
  B: "service"

---

