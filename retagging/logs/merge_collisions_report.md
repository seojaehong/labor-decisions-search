# 재태깅 병합 충돌 리포트

날짜: 2026-03-20 22:08
충돌 건수: 36건 (전건 PM 판정 완료)

이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 서로 다른 값이 발견되어 자동 병합되지 않았습니다.
수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.

---

PM 메모: 아래 36건은 모두 수동 판정이 완료되었고, 확정 값은 `output/reviewed/manual_merge_overrides_v1.json`에 반영했다.

추가 메모: `SHARED_STATUS.md` / `AGENTS_TO_PM.md`에 남아 있던 신규 3건(`id_30811`, `id_30879`, `id_32113`)도 override 반영 사실을 본 리포트에 동기화했다.

## 1. id_34737

소스 A: absence_batch_032_reviewed.jsonl
소스 B: probation_batch_021_reviewed.jsonl

충돌 필드: disposition_type
  A: ["disciplinary_dismissal", "probation_termination"]
  B: ["disciplinary_dismissal"]

---


### PM 판정
- disposition_type: ["disciplinary_dismissal", "probation_termination"]
- reason: 무단결근 3회를 이유로 한 수습 중 징계해고 구조라 disciplinary_dismissal과 probation_termination을 함께 유지

## 2. id_347949

소스 A: absence_batch_032_reviewed.jsonl
소스 B: probation_batch_022_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "procedure"

---


### PM 판정
- issue_type_primary: "dismissal_validity"
- reason: 서면통지 하자가 있어도 사건의 중심은 시용근로자 본채용 거부의 정당성 판단이므로 dismissal_validity 채택

## 3. id_37033

소스 A: incompetence_batch_006_reviewed.jsonl
소스 B: probation_batch_028_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["probation_termination"]

---


### PM 판정
- disposition_type: ["dismissal"]
- reason: 시용 후 정식채용된 뒤 업무능력 부족을 이유로 해고한 구조가 더 분명하여 dismissal 채택

## 4. id_37423

소스 A: incompetence_batch_006_reviewed.jsonl
소스 B: probation_batch_028_reviewed.jsonl

충돌 필드: disposition_type
  A: ["rejection_of_regular_employment"]
  B: ["probation_termination"]

---


### PM 판정
- disposition_type: ["probation_termination"]
- reason: 수습기간 중 적격성 부족으로 근로관계를 종료한 사건이라 rejection_of_regular_employment보다 probation_termination이 더 적절

## 5. id_37669

소스 A: incompetence_batch_006_reviewed.jsonl
소스 B: probation_batch_028_reviewed.jsonl

충돌 필드: disposition_type
  A: ["transfer"]
  B: ["transfer", "suspension"]

---


### PM 판정
- disposition_type: ["transfer", "suspension"]
- reason: 전보와 대기발령이 함께 문제된 사건이므로 suspension을 포함한 복합 처분으로 확정

## 6. id_38957

소스 A: incompetence_batch_006_reviewed.jsonl
소스 B: probation_batch_029_reviewed.jsonl

충돌 필드: industry_context
  A: "construction"
  B: "unknown"

---


### PM 판정
- industry_context: "construction"
- reason: 업무능력 평가 후 사직 권고가 이뤄진 건설현장 맥락이 확인되어 construction 채택

## 7. id_38983

소스 A: incompetence_batch_006_reviewed.jsonl
소스 B: probation_batch_029_reviewed.jsonl

충돌 필드: industry_context
  A: "education"
  B: "unknown"

---


### PM 판정
- industry_context: "education"
- reason: 부원장·원장 평가 구조가 드러나는 교육기관 수습평가 사건이라 education 채택

## 8. id_39693

소스 A: incompetence_batch_006_reviewed.jsonl
소스 B: probation_batch_030_reviewed.jsonl

충돌 필드: industry_context
  A: "service"
  B: "unknown"

---


### PM 판정
- industry_context: "service"
- reason: 민원 응대·상담 오류가 핵심인 서비스 현장 수습평가 사건이라 service 채택

## 9. id_401885

소스 A: incompetence_batch_006_reviewed.jsonl
소스 B: probation_batch_032_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---


### PM 판정
- industry_context: "service"
- reason: 수습평가 기준과 본채용 거부 맥락상 service가 더 구체적이므로 채택

## 10. id_34903

소스 A: probation_batch_023_reviewed.jsonl
소스 B: violence_batch_031_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "dismissal_validity"

---


### PM 판정
- issue_type_primary: "dismissal_validity"
- reason: 감봉이 함께 있었지만 최종 쟁점은 수습기간 본채용 거부의 정당성 판단이라 dismissal_validity 채택

## 11. id_350303

소스 A: probation_batch_024_reviewed.jsonl
소스 B: violence_batch_031_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "misconduct"
  B: "dismissal_validity"

충돌 필드: industry_context
  A: "service"
  B: "public"

---


### PM 판정
- issue_type_primary: "dismissal_validity"
- industry_context: "public"
- reason: 비위가 사유로 제시되더라도 본안은 시용근로자 본채용 거부 정당성이고 사건 배경은 공공 쉼터여서 public 채택

## 12. id_350887

소스 A: probation_batch_025_reviewed.jsonl
소스 B: violence_batch_032_reviewed.jsonl

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["probation_termination"]

---


### PM 판정
- disposition_type: ["probation_termination"]
- reason: 시용근로계약에서 유보된 해약권 행사에 대한 절차 하자 사건이므로 probation_termination 채택

## 13. id_351757

소스 A: probation_batch_026_reviewed.jsonl
소스 B: violence_batch_033_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "misconduct"

---


### PM 판정
- issue_type_primary: "disciplinary_severity"
- reason: 폭언·폭행 등 비위는 인정되며 판정의 초점은 해고 양정 및 절차 적정성이라 disciplinary_severity 채택

## 14. id_351861

소스 A: probation_batch_026_reviewed.jsonl
소스 B: violence_batch_033_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "misconduct"

---


### PM 판정
- issue_type_primary: "disciplinary_severity"
- reason: 욕설·몸싸움 자체보다 정직 3개월의 양정 적정성이 중심이어서 disciplinary_severity 채택

## 15. id_346845

소스 A: absence_batch_031_reviewed.jsonl
소스 B: workplace_bullying_batch_008_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "misconduct"
  B: "disciplinary_severity"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---


### PM 판정
- issue_type_primary: "disciplinary_severity"
- disposition_type: ["disciplinary_dismissal"]
- reason: 직무태만·명령불복종·무단결근이 인정된 뒤 양정과 절차를 심사한 징계해고 사건이라 disciplinary_severity/disciplinary_dismissal 채택

## 16. id_347

소스 A: absence_batch_031_reviewed.jsonl
소스 B: workplace_bullying_batch_008_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "absence_without_leave"
  B: "disciplinary_severity"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

---


### PM 판정
- issue_type_primary: "disciplinary_severity"
- disposition_type: ["disciplinary_dismissal"]
- reason: 28일 무단결근이 중대하지만 판정 구조는 징계사유 인정 후 해고 양정·절차 심사에 가까워 disciplinary_severity/disciplinary_dismissal 채택

## 17. id_347625

소스 A: probation_batch_022_reviewed.jsonl
소스 B: workplace_bullying_batch_009_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

---


### PM 판정
- issue_type_primary: "work_ability"
- reason: 1차 평가 점수와 수습평가표의 합리성이 직접 쟁점이므로 본채용 거부 일반론보다 work_ability가 더 정확

## 18. id_347649

소스 A: absence_batch_032_reviewed.jsonl
소스 B: workplace_bullying_batch_009_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "absence_without_leave"
  B: "disciplinary_severity"

---


### PM 판정
- issue_type_primary: "absence_without_leave"
- reason: 3개월 장기 무단결근이 주된 징계사유이므로 disciplinary_severity보다 absence_without_leave가 검색 진입점으로 적절

## 19. id_34905

소스 A: violence_batch_031_reviewed.jsonl
소스 B: workplace_bullying_batch_010_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "finance"

---


### PM 판정
- industry_context: "finance"
- reason: 법인카드 부정사용 등 금융기관 맥락이 드러나 finance 채택

## 20. id_349227

소스 A: violence_batch_031_reviewed.jsonl
소스 B: workplace_bullying_batch_010_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "dismissal_validity"
  B: "workplace_harassment"

---


### PM 판정
- issue_type_primary: "workplace_harassment"
- reason: 직장 내 괴롭힘 성립요건 중 지위 우위 불인정이 핵심 판단이므로 workplace_harassment 채택

## 21. id_349273

소스 A: violence_batch_031_reviewed.jsonl
소스 B: workplace_bullying_batch_010_reviewed.jsonl

충돌 필드: employment_stage
  A: "unknown"
  B: "fixed_term"

---


### PM 판정
- employment_stage: "unknown"
- reason: 근로자성 자체가 부정된 위촉계약 사건이라 fixed_term보다 unknown 유지가 보수적

## 22. id_349459

소스 A: violence_batch_031_reviewed.jsonl
소스 B: workplace_bullying_batch_010_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "workplace_harassment"

충돌 필드: industry_context
  A: "public"
  B: "service"

---


### PM 판정
- issue_type_primary: "workplace_harassment"
- industry_context: "public"
- reason: 괴롭힘 일부 성립 여부와 그 징계양정이 핵심이고 센터 운영 맥락상 public이 더 타당

## 23. id_350349

소스 A: violence_batch_032_reviewed.jsonl
소스 B: workplace_bullying_batch_011_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "workplace_harassment"

충돌 필드: disposition_type
  A: ["dismissal"]
  B: ["disciplinary_dismissal"]

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---


### PM 판정
- issue_type_primary: "workplace_harassment"
- disposition_type: ["disciplinary_dismissal"]
- industry_context: "service"
- reason: 사적 업무지시·욕설·업무전가·병가 회유 등 구체적 괴롭힘 성립이 핵심이어서 workplace_harassment와 disciplinary_dismissal, service를 채택

## 24. id_350497

소스 A: violence_batch_032_reviewed.jsonl
소스 B: workplace_bullying_batch_011_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "workplace_harassment"

---


### PM 판정
- issue_type_primary: "workplace_harassment"
- reason: 폭행·욕설의 직장내 괴롭힘 성립과 동종 전력에 따른 가중징계가 핵심이므로 workplace_harassment 채택

## 25. id_350539

소스 A: probation_batch_025_reviewed.jsonl
소스 B: workplace_bullying_batch_011_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "unfair_treatment"
  B: "dismissal_validity"

---


### PM 판정
- issue_type_primary: "unfair_treatment"
- reason: 괴롭힘 신고 당일 앞당겨진 평가와 본채용 거부의 보복성 불이익 여부가 핵심이어서 unfair_treatment 채택

## 26. id_350625

소스 A: violence_batch_032_reviewed.jsonl
소스 B: workplace_bullying_batch_011_reviewed.jsonl

충돌 필드: industry_context
  A: "public"
  B: "healthcare"

---


### PM 판정
- industry_context: "healthcare"
- reason: 장애인복지기관·위탁복지서비스 맥락이 확인되어 public보다 healthcare가 더 구체적

## 27. id_350969

소스 A: probation_batch_025_reviewed.jsonl
소스 B: workplace_bullying_batch_012_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

충돌 필드: disposition_type
  A: ["rejection_of_regular_employment"]
  B: ["probation_termination"]

---


### PM 판정
- issue_type_primary: "dismissal_validity"
- disposition_type: ["rejection_of_regular_employment"]
- reason: 수습평가 미달이 근거이지만 최종 판단 프레임은 본채용 거부의 정당성 심사이므로 dismissal_validity와 rejection_of_regular_employment 채택

## 28. id_350985

소스 A: violence_batch_032_reviewed.jsonl
소스 B: workplace_bullying_batch_012_reviewed.jsonl

충돌 필드: industry_context
  A: "public"
  B: "unknown"

---


### PM 판정
- industry_context: "public"
- reason: 센터장과 다수 직원 사이의 조직 내 괴롭힘 사건으로 공공센터 맥락이 더 적절하여 public 채택

## 29. id_351039

소스 A: probation_batch_025_reviewed.jsonl
소스 B: workplace_bullying_batch_012_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "procedure"
  B: "dismissal_validity"

충돌 필드: disposition_type
  A: ["rejection_of_regular_employment"]
  B: ["probation_termination"]

---


### PM 판정
- issue_type_primary: "procedure"
- disposition_type: ["rejection_of_regular_employment"]
- reason: 시용기간 연장 권한·절차 하자가 결론을 좌우하므로 procedure와 rejection_of_regular_employment 채택

## 30. id_351527

소스 A: violence_batch_033_reviewed.jsonl
소스 B: workplace_bullying_batch_012_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "misconduct"
  B: "workplace_harassment"

---


### PM 판정
- issue_type_primary: "workplace_harassment"
- reason: 조사결과 통지서 기재가 괴롭힘에 해당하는지 여부 자체가 핵심 판단이라 workplace_harassment 채택

## 31. id_351757

소스 A: probation_batch_026_reviewed.jsonl
소스 B: workplace_bullying_batch_012_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "disciplinary_severity"
  B: "misconduct"

---


### PM 판정
- issue_type_primary: "disciplinary_severity"
- reason: 폭언·폭행 등 비위는 인정되며 판정의 초점은 해고 양정 및 절차 적정성이라 disciplinary_severity 채택

## 32. id_38763

소스 A: probation_batch_029_reviewed.jsonl
소스 B: workplace_bullying_batch_013_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "performance"

---


### PM 판정
- issue_type_primary: "work_ability"
- reason: 수습기간 근무성적평가의 객관성·공정성이 직접 쟁점이므로 performance보다 work_ability 채택

## 33. id_45849

소스 A: incompetence_batch_009_reviewed.jsonl
소스 B: workplace_bullying_batch_033_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "work_ability"
  B: "dismissal_validity"

---


### PM 판정
- issue_type_primary: "dismissal_validity"
- reason: 업무부적격·명령거부·괴롭힘 관련 사정이 모두 본채용 거부 정당성 판단으로 수렴하므로 dismissal_validity 채택

## 34. id_30811

소스 A: probation_batch_015_reviewed.jsonl
소스 B: workplace_bullying_batch_007_reviewed.jsonl

충돌 필드: issue_type_primary
  A: "procedure"
  B: "dismissal_validity"

---


### PM 판정
- issue_type_primary: "dismissal_validity"
- reason: 평가 객관성 부족과 서면통지 위반이 있어도 사건의 법적 중심은 본채용 거부 정당성 판단이므로 dismissal_validity 채택

## 35. id_30879

소스 A: probation_batch_015_reviewed.jsonl
소스 B: workplace_bullying_batch_007_reviewed.jsonl

충돌 필드: industry_context
  A: "unknown"
  B: "service"

---


### PM 판정
- industry_context: "service"
- reason: 업무상 사고 대응 미흡과 보고의무 위반, 다면평가 저조가 결합된 수습 적격성 판단 사건이며 업종은 service가 더 구체적

## 36. id_32113

소스 A: probation_batch_016_reviewed.jsonl
소스 B: workplace_bullying_batch_008_reviewed.jsonl

충돌 필드: disposition_type
  A: ["probation_termination"]
  B: ["rejection_of_regular_employment"]

---


### PM 판정
- disposition_type: ["probation_termination"]
- reason: 업무지시 불이행과 업무태만을 이유로 한 시용기간 중 계약 해지 구조로, 수습 만료 거부보다 probation_termination이 적절

