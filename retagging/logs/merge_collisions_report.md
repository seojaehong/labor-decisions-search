# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 15:35
충돌 건수: 9건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_10181

소스 A: absence_sample_output.jsonl
소스 B: incompetence_sample_output.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "performance"

---

## 2. id_10293

소스 A: incompetence_sample_output.jsonl
소스 B: probation_sample_output.jsonl

충돌 필드: issue_type_primary
  A: "performance"
  B: "work_ability"

---

## 3. id_10419

소스 A: incompetence_sample_output.jsonl
소스 B: probation_sample_output.jsonl

충돌 필드: issue_type_primary
  A: "performance"
  B: "work_ability"

충돌 필드: industry_context
  A: "unknown"
  B: "office"

---

## 4. id_10207

소스 A: absence_sample_output.jsonl
소스 B: violence_sample_output.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 5. id_10237

소스 A: absence_sample_output.jsonl
소스 B: violence_sample_output.jsonl

충돌 필드: issue_type_primary
  A: "misconduct"
  B: "disciplinary_severity"

---

## 6. id_10465

소스 A: probation_sample_output.jsonl
소스 B: violence_sample_output.jsonl

충돌 필드: disposition_type
  A: ["probation_termination"]
  B: ["rejection_of_regular_employment"]

---

## 7. id_10051

소스 A: absence_sample_output.jsonl
소스 B: workplace_bullying_sample_output.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 8. id_10075

소스 A: violence_sample_output.jsonl
소스 B: workplace_bullying_sample_output.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "misconduct"

---

## 9. id_10555

소스 A: absence_sample_output.jsonl
소스 B: workplace_bullying_sample_output.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "misconduct"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

