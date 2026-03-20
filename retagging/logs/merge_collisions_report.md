# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 18:57
충돌 건수: 5건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_24147

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_010_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "performance"

충돌 필드: industry_context
  A: "unknown"
  B: "service"

충돌 필드: disposition_type
  A: ["probation_termination"]
  B: ["rejection_of_regular_employment"]

---

## 2. id_24207

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: probation_batch_010_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "performance"

---

## 3. id_1861

소스 A: absence_batch_010_reviewed.jsonl
소스 B: violence_batch_008_reviewed.jsonl

충돌 필드: industry_context
  A: "service"
  B: "retail"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 4. id_1903

소스 A: absence_batch_010_reviewed.jsonl
소스 B: violence_batch_009_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 5. id_20711

소스 A: probation_batch_007_reviewed.jsonl
소스 B: violence_batch_010_reviewed.jsonl

충돌 필드: disposition_type
  A: ["disciplinary_dismissal"]
  B: ["probation_termination"]

---

