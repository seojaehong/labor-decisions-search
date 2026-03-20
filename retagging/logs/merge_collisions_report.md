# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 18:14
충돌 건수: 5건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_20035

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_007_reviewed.jsonl

충돌 필드: industry_context
  A: "service"
  B: "education"

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "performance"

---

## 2. id_20159

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_007_reviewed.jsonl

충돌 필드: industry_context
  A: "service"
  B: "manufacturing"

---

## 3. id_20753

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_007_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "attendance"

---

## 4. id_20815

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_007_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---

## 5. id_17591

소스 A: incompetence_batch_001_reviewed.jsonl
소스 B: violence_batch_007_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "public"

충돌 필드: employment_stage
  A: "renewal_stage"
  B: "fixed_term"

---

