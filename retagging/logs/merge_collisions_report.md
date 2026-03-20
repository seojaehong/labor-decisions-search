# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 19:13
충돌 건수: 4건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_20365

소스 A: absence_batch_012_reviewed.jsonl
소스 B: probation_batch_007_reviewed.jsonl

충돌 필드: employment_stage
  A: "probation"
  B: "regular"

---

## 2. id_26635

소스 A: incompetence_batch_003_reviewed.jsonl
소스 B: probation_batch_012_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

---

## 3. id_20441

소스 A: absence_batch_012_reviewed.jsonl
소스 B: violence_batch_010_reviewed.jsonl

충돌 필드: industry_context
  A: "public"
  B: "unknown"

---

## 4. id_20589

소스 A: absence_batch_012_reviewed.jsonl
소스 B: violence_batch_010_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "absence_without_leave"
  B: "misconduct"

---

