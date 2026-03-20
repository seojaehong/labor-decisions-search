# incompetence_batch_009_reviewed.jsonl 1차 self-review 메모

## 배치 요약
- 총 30건 (incompetence 레거시 분류)
- work_ability 정면 쟁점: 12건
- dismissal_validity(해고 정당성 자체가 핵심): 6건
- renewal_expectation 혼입(exclusion 처리): 3건
- procedure dominant: 2건
- misconduct 실질: 1건
- disciplinary_severity(이중징계 등): 2건
- transfer_validity: 1건
- worker_status(채용 미성립): 1건
- 기타(채용내정 취소, 해고 부존재 등): 2건

## work_ability vs dismissal_validity 판별 기준
- **work_ability**: 업무수행능력 부족 자체가 정면으로 다투어지는 사건 (주로 수습/본채용 거부)
- **dismissal_validity**: 업무능력 부족이 주장되었으나, 실질은 입증 부족·절차 하자·이중징계 등 해고 자체의 정당성이 핵심인 사건

## 갱신기대권 혼입 건 (exclusion 처리)

### id_44731
- primary: renewal_expectation / disposition: ['nonrenewal']
- exclusion_flags: ['renewal_expectation_dominant', 'not_really_performance_case']
- 사유: 갱신기대권이 핵심 쟁점. 경비원 평가점수 미달이 갱신 거절 사유이나, 업무능력 검색에 상위 노출되면 혼란.

### id_50313
- primary: renewal_expectation / disposition: ['nonrenewal']
- exclusion_flags: ['renewal_expectation_dominant', 'not_really_performance_case']
- 사유: 갱신기대권 핵심. 미화원 동료 다툼·민원이 갱신 거절 사유.

### id_50425
- primary: renewal_expectation / disposition: ['nonrenewal']
- exclusion_flags: ['renewal_expectation_dominant', 'not_really_performance_case']
- 사유: 갱신기대권 핵심. 재계약 평가점수 70점 미달.

## not_really_performance_case 플래그 부여 건 (13건)

| case_id | 실질 쟁점 | primary 태그 |
|---------|-----------|-------------|
| id_44499 | 징계사유 입증 부족 + 양정 과다 + 절차 하자 | dismissal_validity |
| id_44731 | 갱신기대권 | renewal_expectation |
| id_45099 | 해고사유 입증 전무 + 상시근로자수 | dismissal_validity |
| id_45967 | 해고 부존재 | dismissal_validity |
| id_46335 | 해고사유 미인정 + 절차 하자 | dismissal_validity |
| id_46355 | 이중징계 | disciplinary_severity |
| id_47567 | 징계사유 입증 부족 + 절차 하자 | dismissal_validity |
| id_48183 | 근로계약 미성립 | worker_status |
| id_48589 | 채용내정 취소 부당 | dismissal_validity |
| id_49303 | 욕설 비위행위(misconduct) | misconduct |
| id_49841 | 이중징계(정직) | disciplinary_severity |
| id_50313 | 갱신기대권 | renewal_expectation |
| id_50425 | 갱신기대권 | renewal_expectation |
| id_51061 | 채용내정 취소 | dismissal_validity |
| id_51489 | 해고 존재 + 구제이익 | dismissal_validity |
| id_51567 | 전보·직위해제 정당성 | transfer_validity |

## procedure_dominant 플래그 부여 건

### id_4641
- primary: procedure
- 사유: 서면통지 의무 위반이 핵심. 업무능력 부족은 퇴직 종용 맥락 언급에 불과.

### id_48033
- primary: procedure
- 사유: 해고통지서에 구체적 해고사유 미명시. 업무능력 부족은 계약서 해지조항 나열에 불과.

## 수습/본채용 거부 사건 정리 (work_ability primary, 10건)

| case_id | 결과 | 핵심 판단 |
|---------|------|-----------|
| id_44349 | 기각(정당) | 수습평가표 기반, 서면 통지 적법 |
| id_45849 | 초심유지(정당) | 업무명령 거부 + 괴롭힘 + 평가 미달 |
| id_47055 | 기각(정당) | 기준점수 현저 미달 + 동료 연명서 |
| id_47883 | 초심유지(정당) | 배치전환 지시 불응 |
| id_48681 | 인용(부당) | 평가자 전문성·기준 미제시 |
| id_49415 | 기각(정당) | 다면평가 절차 적법 |
| id_50515 | 인용(부당) | 평가 객관성·공정성 부족 |
| id_50607 | 초심유지(정당) | 평가 미달 + 괴롭힘 신고 보복 아님 |
| id_51313 | 기각(정당) | 168건 오류 + 교육 후 미개선 |
| id_46597 | 인용(부당) | 사실확인서 신빙성 부족(정규직) |
| id_51167 | 인용(부당) | 면직 사유 입증 없음(정규직) |

## 특이 사건

### id_4563 (근무성적 불량자 결정)
- 면직이 아닌 '근무성적 불량자 결정' 자체의 징벌성 여부가 쟁점
- disposition_type: ['other'] — 해고·정직 등이 아닌 불이익 결정
- primary: performance (인사고과 기반 평가 정당성)

### id_48183 (채용 절차 중단)
- 근로관계 자체가 미성립
- employment_stage: pre_hire
- primary: worker_status

### id_48589 / id_51061 (채용내정 취소 — 초심+재심)
- 채용내정(근로계약) 성립 후 취소의 정당성
- employment_stage: pre_hire
- 수습 평가 미실시 상태에서 업무부적격 판단한 것이 핵심 부당 사유
