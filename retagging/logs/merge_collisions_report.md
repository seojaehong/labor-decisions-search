# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 15:44
충돌 건수: 5건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_10419

소스 A: incompetence_sample_reviewed.jsonl
소스 B: probation_sample_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "office"

---

## 2. id_10207

소스 A: absence_sample_reviewed.jsonl
소스 B: violence_sample_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 3. id_10051

소스 A: absence_sample_reviewed.jsonl
소스 B: workplace_bullying_sample_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

## 4. id_10075

소스 A: violence_sample_reviewed.jsonl
소스 B: workplace_bullying_sample_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "disciplinary_severity"

---

## 5. id_10555

소스 A: absence_sample_reviewed.jsonl
소스 B: workplace_bullying_sample_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "workplace_harassment"
  B: "misconduct"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---

