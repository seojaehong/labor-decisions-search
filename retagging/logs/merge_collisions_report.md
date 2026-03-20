# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 19:26
충돌 건수: 2건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_22373

소스 A: absence_batch_014_reviewed.jsonl
소스 B: violence_batch_012_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "absence_without_leave"
  B: "misconduct"

---

## 2. id_22773

소스 A: absence_batch_014_reviewed.jsonl
소스 B: violence_batch_013_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "misconduct"
  B: "disciplinary_severity"

---

