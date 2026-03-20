# probation_batch_010 self-review

## 배치 통계
- 총 건수: 30
- probation_termination: 8 (id_23717, id_23727, id_23835, id_23915, id_2423, id_24899, id_25023, id_24453[징계해고 재분류])
- rejection_of_regular_employment: 11 (id_23781, id_23933, id_23949, id_23963, id_23995, id_24007, id_24147, id_24207, id_24261, id_24391, id_24563, id_24585, id_2495)
- unrelated_to_probation: 7 (id_23923, id_23989, id_2407, id_24129, id_24417, id_24667, id_24769, id_24903)
- 기타 disposition: 4 (contract_termination, no_formal_disposition, disciplinary_dismissal, other)

## employment_stage 분포
- probation: 21
- fixed_term: 4 (id_23923, id_24417, id_24769, id_24903)
- regular: 3 (id_23989, id_24129, id_24667)
- unknown: 1 (id_2407)

## issue_type_primary 분포
- performance: 9
- procedure: 6
- dismissal_validity: 6
- misconduct: 2
- disciplinary_severity: 2
- worker_status: 1
- absence_without_leave: 1
- discrimination: 1

## disposition_type 핵심 분류 기준 (probation_termination vs rejection_of_regular_employment)

| 구분 | 기준 | 해당 사례 |
|------|------|-----------|
| probation_termination | 수습기간 중(만료 전) 해고 | id_23717, id_23727, id_23835, id_23915, id_2423, id_24899, id_25023 |
| rejection_of_regular_employment | 수습기간 만료 후 본채용 거부 | id_23781, id_23933, id_23949, id_23963, id_23995, id_24007, id_24147, id_24207, id_24261, id_24391, id_24563, id_24585, id_2495 |
| disciplinary_dismissal | 시용기간이나 실질 징계해고 | id_24453, id_23989, id_24667 |
| contract_termination | 기간제 계약만료 | id_23923, id_24769, id_24903 |
| no_formal_disposition | 해고 부존재 | id_2407, id_24379 |

## unrelated_to_probation 판단 근거

### id_23923 — 복직자 수습 적용 불가
- 복직 후 새 근로계약 체결한 자는 신규채용이 아니므로 수습근로자 아님
- 기간제 계약만료로 근로관계 종료

### id_23989 — 20여년 재직자 징계양정 과다
- legacy에 probation 태그 있으나 수습과 전혀 무관
- 교육기관 강사의 부적절 발언에 대한 징계해고 양정 과다

### id_2407 — 사직서 유효성 다툼
- 본문에 수습 관련 쟁점 전무. 사직서 비진의 의사표시 + 철회 가부만 다툼

### id_24129 — 수습근로자 해당 여부 부정
- 근로계약서 미명시, 인사규정상 선택사항, 입증자료 미제시 → 수습 아님
- 직권면직 자체의 부당성이 핵심

### id_24417 — 차별시정 사건
- 촉탁기사 기간을 수습성으로 인정하나, 해고 쟁점이 아닌 임금 차별 사건

### id_24667 — 복수 근로자 징계해고
- 근로자2만 시용기간이나 전체 사건의 핵심은 징계양정

### id_24769 — 기간제 계약만료
- 취업규칙에 수습 규정 있으나 계약기간 3개월과 별도 수습 해석 불가

### id_24903 — 고용승계 촉탁직 기간만료
- 고용승계된 자를 수습근로자로 볼 수 없음, 촉탁직 계약만료

## 핵심 판단 기록

### id_23717
- employment_stage: probation
- primary: procedure
- disposition: ['probation_termination']
- confidence: high
- 판단 근거: 수습기간을 기간제 계약으로 위장한 사례. 실질적으로 수습 해고이므로 probation_termination.

### id_23727
- employment_stage: probation
- primary: performance
- disposition: ['probation_termination']
- confidence: high
- 판단 근거: 경력직 과장 수습 중 납품수량 오류 등 구체적 손해 발생. 서면통지도 이행.

### id_23781
- employment_stage: probation
- primary: procedure
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 주유소. 계약기간 3개월이나 실질 수습계약으로 인정. 수습기간 만료 후 본채용 거부이므로 rejection_of_regular_employment.

### id_23835
- employment_stage: probation
- primary: misconduct
- disposition: ['probation_termination']
- confidence: high
- 판단 근거: 단체협약상 인사위원회 미개최 주장도 있으나, 시용기간 해고는 징계해고와 성질 상이하여 불문.

### id_23915
- employment_stage: probation
- primary: performance
- disposition: ['probation_termination']
- confidence: high
- 판단 근거: 골프의류 백화점 입점 업무. 평가 객관성 부족, 일관된 기준 부재 지적.

### id_23923
- employment_stage: fixed_term
- primary: worker_status
- disposition: ['contract_termination']
- exclusion_flags: ['unrelated_to_probation']
- confidence: high
- 판단 근거: 수습 태그가 붙어있으나 실질적으로 수습근로자가 아닌 것으로 판정. unrelated_to_probation.

### id_23933
- employment_stage: probation
- primary: procedure
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 해고통보서 자체는 존재하나 '부적합'이라고만 기재, 구체적 사유 미기재가 핵심.

### id_23949
- employment_stage: probation
- primary: dismissal_validity
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 의료기관. 개원 준비기간도 수습기간에 포함된다고 판단. 재심에서 초심 취소.

### id_23963
- employment_stage: probation
- primary: procedure
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 상가 관리 소장이 통지 후 철회, 이후 구두로 재통지. 권고사직 시도도 있었음.

### id_23989
- employment_stage: regular
- primary: disciplinary_severity
- disposition: ['disciplinary_dismissal']
- exclusion_flags: ['unrelated_to_probation']
- confidence: high
- 판단 근거: legacy_reason_category에 probation이 포함되어 있으나, 20여년 재직자로 수습과 전혀 무관. 징계양정 과다가 핵심.

### id_23995
- employment_stage: probation
- primary: procedure
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 입주자대표회의 의사정족수 미달. 첫 번째 해고는 무효이나, 두 번째(수습기간 종료) 계약해지로 근로관계 종료.

### id_24007
- employment_stage: probation
- primary: performance
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 호텔 인스펙터. 시용기간 중 해고는 징계절차 불요.

### id_2407
- employment_stage: unknown
- primary: dismissal_validity
- disposition: ['no_formal_disposition']
- exclusion_flags: ['unrelated_to_probation', 'resignation_dispute']
- confidence: high
- 판단 근거: legacy tags에 probation이 있으나 본문에 수습 관련 쟁점 없음. 사직서 유효성이 유일한 쟁점.

### id_24129
- employment_stage: regular
- primary: dismissal_validity
- disposition: ['dismissal']
- exclusion_flags: ['unrelated_to_probation']
- confidence: high
- 판단 근거: 근로계약서에 수습기간 미명시, 인사규정상 선택사항, 입증자료 미제시 → 수습근로자 아님.

### id_24147
- employment_stage: probation
- primary: performance
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 수습이라는 용어 사용하나 실질 시용. 취업규칙상 인사위원회 불요 규정 있어 절차 위반은 부정.

### id_24207
- employment_stage: probation
- primary: performance
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: TBE 보고서 한국어 작성, 무단 발송, 평가 52점. 수습사원 관리지침서에 별도 절차 규정 없음.

### id_2423
- employment_stage: probation
- primary: performance
- disposition: ['probation_termination']
- confidence: high
- 판단 근거: 식자재 유통기한 관리 미흡 등 사유. 평가 객관성·공정성 부족 판단.

### id_24261
- employment_stage: probation
- primary: performance
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 역량평가(성과급용)와 수습평가(본채용용)의 시기·목적이 상이하여 점수 차이는 불합리하지 않다고 판단.

### id_24379
- employment_stage: probation
- primary: dismissal_validity
- disposition: ['no_formal_disposition']
- confidence: high
- 판단 근거: 콜센터. 수습 5일 후 임금 확정 과정에서 시급 7000원 거절 후 미출근.

### id_24391
- employment_stage: probation
- primary: absence_without_leave
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 고용승계 시에도 수습기간 설정 가능 확인. 무단결근 + 초번근무 거부.

### id_24417
- employment_stage: fixed_term
- primary: discrimination
- disposition: ['other']
- exclusion_flags: ['unrelated_to_probation', 'unrelated_to_dismissal']
- confidence: high
- 판단 근거: 차별시정 사건. 촉탁기사 기간을 수습성 기간으로 인정하나 해고 쟁점 아님.

### id_24453
- employment_stage: probation
- primary: disciplinary_severity
- disposition: ['disciplinary_dismissal']
- confidence: high
- 판단 근거: 시용기간이라도 징계사유에 해당하면 징계절차를 거쳐야 한다는 중요 판단. 미숙련자 실수 + 1일 무단결근.

### id_24563
- employment_stage: probation
- primary: performance
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 수습기간 연장의 유효성 판단(묵시적 동의 인정)도 중요 쟁점.

### id_24585
- employment_stage: probation
- primary: dismissal_validity
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 재심에서 초심 취소. 본채용 거부 사유 + 서면통지 모두 문제.

### id_24667
- employment_stage: regular
- primary: disciplinary_severity
- disposition: ['disciplinary_dismissal']
- exclusion_flags: ['unrelated_to_probation']
- confidence: medium
- 판단 근거: 복수 근로자 중 근로자2만 시용기간이나 전체 사건의 핵심은 징계해고 양정. 운수업.

### id_24769
- employment_stage: fixed_term
- primary: dismissal_validity
- disposition: ['contract_termination']
- exclusion_flags: ['unrelated_to_probation']
- confidence: high
- 판단 근거: 취업규칙에 수습기간 규정이 있으나, 근로계약서상 계약기간이 3개월이므로 별도 수습 해석 불가.

### id_24899
- employment_stage: probation
- primary: misconduct
- disposition: ['probation_termination']
- confidence: high
- 판단 근거: 택시기사. 부제차량 4회 운행 + 졸음운전 사고 + 요금 부당징수 민원. 단체협약에 수습 중 징계사유 시 채용취소 규정.

### id_24903
- employment_stage: fixed_term
- primary: dismissal_validity
- disposition: ['contract_termination']
- exclusion_flags: ['unrelated_to_probation']
- confidence: high
- 판단 근거: 경비지도사. 고용승계 시 수습계약이 아닌 촉탁직 계약으로 판단. 정년 이슈도 관련.

### id_2495
- employment_stage: probation
- primary: procedure
- disposition: ['rejection_of_regular_employment']
- confidence: high
- 판단 근거: 재심에서 초심 취소. 공무직에 정규직 인사규정 준용 자체가 부당.

### id_25023
- employment_stage: probation
- primary: performance
- disposition: ['probation_termination']
- confidence: high
- 판단 근거: 호텔. 예초기·전기카트 습득 거부, 시설반장 퇴사 초래. 채용취소 통지서 + 면담 이행.
