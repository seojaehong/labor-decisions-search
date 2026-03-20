# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 17:50
충돌 건수: 33건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_10909

소스 A: absence_batch_001_reviewed.jsonl
소스 B: violence_batch_001_reviewed.jsonl

충돌 필드: industry_context
  A: "public"
  B: "manufacturing"

---

## 2. id_11245

소스 A: absence_batch_001_reviewed.jsonl
소스 B: violence_batch_001_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "workplace_harassment"

---

## 3. id_11257

소스 A: absence_batch_001_reviewed.jsonl
소스 B: violence_batch_001_reviewed.jsonl

충돌 필드: industry_context
  A: "service"
  B: "unknown"

---

## 4. id_11877

소스 A: absence_batch_002_reviewed.jsonl
소스 B: violence_batch_002_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 5. id_12371

소스 A: probation_batch_002_reviewed.jsonl
소스 B: violence_batch_002_reviewed.jsonl

충돌 필드: disposition_type
  A: ["disciplinary_dismissal"]
  B: ["probation_termination"]

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "procedure"

충돌 필드: industry_context
  A: "healthcare"
  B: "unknown"

---

## 6. id_12647

소스 A: absence_batch_002_reviewed.jsonl
소스 B: violence_batch_003_reviewed.jsonl

충돌 필드: disposition_type
  A: ["suspension"]
  B: ["suspension", "pay_cut"]

충돌 필드: industry_context
  A: "public"
  B: "unknown"

---

## 7. id_12649

소스 A: absence_batch_003_reviewed.jsonl
소스 B: violence_batch_003_reviewed.jsonl

충돌 필드: disposition_type
  A: ["suspension"]
  B: ["suspension", "transfer"]

---

## 8. id_1293

소스 A: absence_batch_003_reviewed.jsonl
소스 B: violence_batch_003_reviewed.jsonl

충돌 필드: industry_context
  A: "public"
  B: "unknown"

---

## 9. id_13359

소스 A: probation_batch_003_reviewed.jsonl
소스 B: violence_batch_004_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "procedure"

---

## 10. id_13415

소스 A: probation_batch_003_reviewed.jsonl
소스 B: violence_batch_004_reviewed.jsonl

충돌 필드: industry_context
  A: "service"
  B: "healthcare"

---

## 11. id_13419

소스 A: absence_batch_003_reviewed.jsonl
소스 B: violence_batch_004_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "misconduct"

---

## 12. id_1441

소스 A: probation_batch_003_reviewed.jsonl
소스 B: violence_batch_004_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "procedure"

---

## 13. id_15147

소스 A: probation_batch_004_reviewed.jsonl
소스 B: violence_batch_005_reviewed.jsonl

충돌 필드: disposition_type
  A: ["disciplinary_dismissal"]
  B: ["dismissal"]

---

## 14. id_10991

소스 A: absence_batch_001_reviewed.jsonl
소스 B: workplace_bullying_batch_001_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

충돌 필드: issue_type_primary
  A: "unfair_treatment"
  B: "disciplinary_severity"

충돌 필드: industry_context
  A: "public"
  B: "unknown"

---

## 15. id_11137

소스 A: violence_batch_001_reviewed.jsonl
소스 B: workplace_bullying_batch_001_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "misconduct"

---

## 16. id_11339

소스 A: absence_batch_001_reviewed.jsonl
소스 B: workplace_bullying_batch_001_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "dismissal_validity"

---

## 17. id_11387

소스 A: violence_batch_001_reviewed.jsonl
소스 B: workplace_bullying_batch_001_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

충돌 필드: industry_context
  A: "unknown"
  B: "office"

---

## 18. id_11829

소스 A: violence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_001_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

---

## 19. id_11877

소스 A: absence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_001_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

충돌 필드: issue_type_primary
  A: "unfair_treatment"
  B: "workplace_harassment"

---

## 20. id_11911

소스 A: absence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "unfair_treatment"
  B: "misconduct"

충돌 필드: industry_context
  A: "public"
  B: "unknown"

---

## 21. id_11981

소스 A: absence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

충돌 필드: industry_context
  A: "public"
  B: "unknown"

---

## 22. id_12013

소스 A: violence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

---

## 23. id_12171

소스 A: violence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "misconduct"

충돌 필드: industry_context
  A: "unknown"
  B: "public"

---

## 24. id_12189

소스 A: absence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: industry_context
  A: "manufacturing"
  B: "finance"

---

## 25. id_12333

소스 A: absence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 26. id_12383

소스 A: violence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

---

## 27. id_12485

소스 A: absence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["transfer", "dismissal"]

---

## 28. id_12491

소스 A: violence_batch_003_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

---

## 29. id_12497

소스 A: violence_batch_003_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---

## 30. id_12573

소스 A: violence_batch_003_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "procedure"
  B: "unfair_treatment"

---

## 31. id_12685

소스 A: violence_batch_003_reviewed.jsonl
소스 B: workplace_bullying_batch_002_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["other", "dismissal"]

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

---

## 32. id_1521

소스 A: absence_batch_005_reviewed.jsonl
소스 B: workplace_bullying_batch_003_reviewed.jsonl

충돌 필드: industry_context
  A: "public"
  B: "finance"

---

## 33. id_21941

소스 A: incompetence_batch_002_reviewed.jsonl
소스 B: workplace_bullying_batch_003_reviewed.jsonl

충돌 필드: disposition_type
  A: ["disciplinary_dismissal"]
  B: ["dismissal"]

---

