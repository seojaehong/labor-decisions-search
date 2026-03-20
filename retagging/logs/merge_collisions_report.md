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



---

# 수동 검토 최종 제안 (2026-03-20)

## 1. id_10419 최종안
- 최종 제안:
  - `industry_context`: `office`
- 짧은 notes:
  - 관리직 수습평가, 보고·소통 역량 부족, 관리직 평가체계가 핵심이라 `office`가 더 구체적이고 사건 실질에 맞음.

## 2. id_10207 최종안
- 최종 제안:
  - `issue_type_primary`: `disciplinary_severity`
  - `disposition_type`: `disciplinary_dismissal`
- 짧은 notes:
  - 사건의 판단구조는 폭언·폭행 등 징계사유 일부 인정 후에도 해고가 과하다는 것이라, 일반 해고보다 징계해고 사건으로 보는 편이 정확함.

## 3. id_10051 최종안
- 최종 제안:
  - `issue_type_primary`: `disciplinary_severity`
  - `disposition_type`: `disciplinary_dismissal`
- 짧은 notes:
  - 출퇴근카드 대리체크와 괴롭힘이 모두 징계사유로 거론되고, 결론도 해고 양정 과다 여부에 맞춰져 있어 `disciplinary_dismissal`이 더 적절함.

## 4. id_10075 최종안
- 최종 제안:
  - `issue_type_primary`: `disciplinary_severity`
  - `disposition_type`: `disciplinary_dismissal`
- 짧은 notes:
  - 괴롭힘이 중요한 비위이긴 하지만 판정의 중심은 정직 2회 이후 누적 비위에 대한 해고 수위의 정당성이라 `workplace_harassment`보다 `disciplinary_severity`가 적합함.

## 5. id_10555 최종안
- 최종 제안:
  - `issue_type_primary`: `misconduct`
  - `disposition_type`: `disciplinary_dismissal`
- 짧은 notes:
  - 무단결근·물품 유용·퇴사 종용·폭언이 결합된 복합 비위 사건으로, 괴롭힘 단일 사건이라기보다 다수 징계사유를 종합해 해고 정당성을 판단한 구조라 `misconduct`가 더 안정적임.

## 요약 메모
- `dismissal` vs `disciplinary_dismissal` 충돌 2건(id_10207, id_10051)과 복합 충돌 1건(id_10555)은 모두 징계사유를 전제로 한 해고 정당성 판단 구조가 뚜렷하여 `disciplinary_dismissal` 쪽을 채택하는 것이 타당함.
- `workplace_harassment` vs `misconduct` / `disciplinary_severity` 충돌은 "괴롭힘 언급 여부"보다 "위원회가 무엇을 중심으로 결론을 냈는가"를 기준으로 정리함.
