# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 20:32
충돌 건수: 3건

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

## 1. id_346727

소스 A: probation_batch_021_reviewed.jsonl
소스 B: workplace_bullying_batch_008_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "unfair_treatment"
  B: "dismissal_validity"

---

## 2. id_347233

소스 A: probation_batch_021_reviewed.jsonl
소스 B: workplace_bullying_batch_008_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

---

## 3. id_349463

소스 A: probation_batch_023_reviewed.jsonl
소스 B: workplace_bullying_batch_010_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["probation_termination"]

---



# 수동 검토 최종 판정 (2026-03-20, 21:10)

## 1. id_346727 최종안
- `issue_type_primary`: `dismissal_validity`
- `employment_stage`: `probation`
- `disposition_type`: ["rejection_of_regular_employment"]
- `industry_context`: `unknown`
- 근거: 괴롭힘·성희롱 문제 제기에 대한 보복 주장이 있었지만 인정되지 않았고, 최종 판단은 수습평가와 본채용 거부의 정당성 여부에 맞춰져 있다. 따라서 `unfair_treatment`보다 `dismissal_validity`가 프레임에 맞다.

## 2. id_347233 최종안
- `issue_type_primary`: `work_ability`
- `employment_stage`: `probation`
- `disposition_type`: ["rejection_of_regular_employment"]
- `industry_context`: `unknown`
- 근거: 보복 주장보다 6개월 수습평가, 70점 기준, 근무성적 불량·업무능력 부족이 직접적인 판단 중심이다. 수습 적격성 판단 구조가 명확하므로 `work_ability`를 채택한다.

## 3. id_349463 최종안
- `issue_type_primary`: `workplace_harassment`
- `employment_stage`: `probation`
- `disposition_type`: ["probation_termination"]
- `industry_context`: `healthcare`
- 근거: 시용근로자에 대한 중도 해고로 보아야 하고, 본채용 만료 시점의 거절보다는 수습 중 괴롭힘 비위에 대한 해지가 핵심이다. 따라서 `probation_termination`이 더 정확하다.
