# probation_batch_011_reviewed.jsonl 1차 self-review 메모

## 배치 통계
- 총 30건
- **수습 관련(probation)**: 21건
  - rejection_of_regular_employment (본채용 거부): 15건
  - probation_termination (수습기간 중 해고): 3건
  - no_formal_disposition (해고 부존재/합의해지): 3건
- **비수습(unrelated_to_probation)**: 7건
- **채용전형 단계(pre_hire)**: 2건

## 핵심 분류 판단

### rejection_of_regular_employment vs probation_termination 구분
- **rejection_of_regular_employment**: 수습기간 만료 시점 또는 평가 후 본채용 거부 (id_25071, id_25201, id_2523, id_25383, id_25395, id_25469, id_25481, id_25631, id_25699, id_25883, id_26055, id_26077, id_26189, id_26219, id_26363→징계해고로 처리)
- **probation_termination**: 수습기간 도중 해고 (id_25277, id_25423, id_26331)
- 구분 기준: 수습기간 만료 시점의 본채용 거부인지, 수습기간 중간에 해고된 것인지

### unrelated_to_probation 판정 (7건)
| case_id | 사유 |
|---------|------|
| id_25225 | 수습기간 이미 종료, 관리소장 임명 후 징계해고 — 실질은 절차위반 |
| id_25529 | 과거 2차례 8개월 경력으로 시용근로자 부정 — 서면통지 미비 |
| id_25889 | 20년 재직 정규직 성희롱 징계양정 — 수습과 완전 무관 |
| id_26073 | 근로계약서에 수습 미명시, 직권면직 — 수습 지위 부정 |
| id_26187 | 수습 후 정규직 임용 완료, 계약직 전환 강요 후 면직 — 수습 무관 |
| id_25765 | 노조 규약 시정명령 — 해고 사건 아님(unrelated_to_dismissal도 부착) |
| id_26171 | 채용전형 역량평가 단계 — 근로관계 불성립(pre_hire) |

### 해고 부존재 판정 (3건)
| case_id | 사유 |
|---------|------|
| id_25421 | 해고예고통보서 서명 + 자택근무 = 합의해지 |
| id_25427 | 시용계약, 합의해지 인정 |
| id_26035 | 수습 3일차, 임금 협의 결렬로 근로자 자발적 출근 중단 |

## 개별 사건 메모

## id_25071
- primary/disposition: work_ability / ['rejection_of_regular_employment']
- secondary: ['performance', 'procedure']
- exclusion_flags: []
- 판단: 전형적 수습 본채용 거부. 조리원+노인돌봄 복합업무 부적격.

## id_25201
- primary/disposition: dismissal_validity / ['rejection_of_regular_employment']
- secondary: ['evaluation', 'procedure']
- exclusion_flags: []
- 판단: 본채용 거부의 실체+절차 모두 부당. 금전보상명령 포함.

## id_25225
- primary/disposition: procedure / ['disciplinary_dismissal']
- secondary: ['dismissal_validity']
- exclusion_flags: ['unrelated_to_probation']
- 변경 이유: 수습기간 3.31 종료 후 관리소장 임명. 실질은 정규직 징계해고 절차위반.

## id_2523
- primary/disposition: work_ability / ['rejection_of_regular_employment']
- secondary: ['evaluation', 'procedure']
- exclusion_flags: []
- 판단: OJT 평가 C등급. 전자시스템 해고통지 적법성도 인정. 재심 초심유지.

## id_25277
- primary/disposition: misconduct / ['probation_termination']
- secondary: ['procedure']
- exclusion_flags: []
- 판단: 수습기간 중 해고(만료 전). 출입방해·컴퓨터 무단반출 등 비위행위.

## id_25299
- primary/disposition: dismissal_validity / ['dismissal']
- secondary: ['worker_status', 'evaluation']
- exclusion_flags: ['unrelated_to_probation']
- 변경 이유: 수습 합의 자체가 없어 일반직원. 수습기간 종료 명목 해임은 부당.

## id_25355
- primary/disposition: worker_status / ['no_formal_disposition']
- secondary: ['dismissal_validity']
- exclusion_flags: ['unrelated_to_probation', 'unrelated_to_dismissal']
- 변경 이유: 채용전형 단계, 근로관계 불성립. pre_hire.

## id_25383
- primary/disposition: misconduct / ['rejection_of_regular_employment']
- secondary: ['procedure']
- exclusion_flags: []
- 판단: 시용기간 중 자의적 업무처리로 신뢰 상실. 인사위원회·문서통지 절차 충족.

## id_25395
- primary/disposition: work_ability / ['rejection_of_regular_employment']
- secondary: ['evaluation', 'procedure']
- exclusion_flags: []
- 판단: 10개 항목 5등급 평가, 60점 미만 2회. 인사위원회 보완절차 구비.

## id_25421
- primary/disposition: dismissal_validity / ['no_formal_disposition']
- secondary: []
- exclusion_flags: ['settlement_or_mutual_termination']
- 판단: 해고예고통보서 서명 + 자택근무 = 합의해지. 해고 부존재.

## id_25423
- primary/disposition: dismissal_validity / ['probation_termination']
- secondary: ['work_ability', 'procedure']
- exclusion_flags: []
- 판단: 시용기간 중 해고이나 사회통념상 상당성 결여. 병원 개원 초기 혼선.

## id_25427
- primary/disposition: dismissal_validity / ['no_formal_disposition']
- secondary: []
- exclusion_flags: ['settlement_or_mutual_termination']
- 판단: 시용계약 성격 인정, 합의해지. 해고 부존재.

## id_25469
- primary/disposition: work_ability / ['rejection_of_regular_employment']
- secondary: ['performance', 'misconduct']
- exclusion_flags: []
- 판단: 2개월간 4건 민원, 청소업무 부적절, 상급자 무례.

## id_25481
- primary/disposition: dismissal_validity / ['rejection_of_regular_employment']
- secondary: ['worker_status', 'procedure']
- exclusion_flags: []
- 판단: 6개월 수습 만료 후 임의 연장 무효. 실질 정규직이나 disposition은 형식상 본채용 거부.

## id_25529
- primary/disposition: procedure / ['dismissal']
- secondary: ['worker_status', 'dismissal_validity']
- exclusion_flags: ['unrelated_to_probation']
- 변경 이유: 과거 경력 감안 시용근로자 부정. 서면통지 미비가 주된 위반.

## id_25631
- primary/disposition: dismissal_validity / ['rejection_of_regular_employment']
- secondary: ['evaluation', 'worker_status']
- exclusion_flags: []
- 판단: 수습기간 연장은 유효하나 연장 기간 평가 미실시. 본채용 거부 사유 부족.

## id_25699
- primary/disposition: dismissal_validity / ['rejection_of_regular_employment']
- secondary: ['misconduct']
- exclusion_flags: []
- 판단: 운수업 기사 수습. 해고사유 각각 합리성 부족.

## id_25765
- primary/disposition: discrimination / ['other']
- secondary: ['unfair_treatment']
- exclusion_flags: ['unrelated_to_dismissal']
- 변경 이유: 노조 규약 시정명령. 해고 사건 아님. 시용기간 조합원 차별.

## id_25883
- primary/disposition: dismissal_validity / ['rejection_of_regular_employment']
- secondary: ['attendance', 'procedure']
- exclusion_flags: []
- 판단: 고용승계 근로자 수습. 무단결근 5일이 취업규칙상 해고사유 미해당. 초심취소.

## id_25889
- primary/disposition: disciplinary_severity / ['disciplinary_dismissal']
- secondary: ['misconduct']
- exclusion_flags: ['unrelated_to_probation']
- 변경 이유: 20년 재직 정규직. 성희롱·장애인 비하 발언 징계양정 과다. 수습과 무관.

## id_26035
- primary/disposition: dismissal_validity / ['no_formal_disposition']
- secondary: []
- exclusion_flags: ['settlement_or_mutual_termination', 'resignation_dispute']
- 판단: 수습 3일차 콜센터. 임금 조건 합의 실패, 근로자 자발적 출근 중단.

## id_26055
- primary/disposition: work_ability / ['rejection_of_regular_employment']
- secondary: ['evaluation', 'discrimination']
- exclusion_flags: []
- 판단: 보훈특별고용이나 차별 아님. 평가 50.5/70점 미달.

## id_26073
- primary/disposition: dismissal_validity / ['dismissal']
- secondary: ['worker_status', 'procedure']
- exclusion_flags: ['unrelated_to_probation']
- 변경 이유: 수습기간 미명시, 수습근로자 부정. 직권면직 해고 해당, 사유·절차 부당.

## id_26077
- primary/disposition: work_ability / ['rejection_of_regular_employment']
- secondary: ['performance']
- exclusion_flags: []
- 판단: 동료 일관 진술로 업무태도·능력 문제 확인. 해고일 11.7 확정.

## id_26171
- primary/disposition: worker_status / ['no_formal_disposition']
- secondary: []
- exclusion_flags: ['unrelated_to_probation', 'unrelated_to_dismissal']
- 변경 이유: 채용전형 역량평가 단계. 근로관계 불성립. 각하.

## id_26187
- primary/disposition: dismissal_validity / ['contract_termination']
- secondary: ['worker_status']
- exclusion_flags: ['unrelated_to_probation']
- 변경 이유: 수습 후 정규직 임용 완료. 계약직 전환 강요 후 계약만료 면직.

## id_26189
- primary/disposition: misconduct / ['rejection_of_regular_employment']
- secondary: ['attendance', 'work_ability']
- exclusion_flags: []
- 판단: 복합 비위(지각, 교통사고, 명예훼손, 지시거부, 안전위반, 음주출근).

## id_26219
- primary/disposition: work_ability / ['rejection_of_regular_employment']
- secondary: ['evaluation']
- exclusion_flags: []
- 판단: 연수종합평가+영업점 역량평가 모두 최하위. 근로자도 평가기준 이례성 부인.

## id_26331
- primary/disposition: work_ability / ['probation_termination']
- secondary: ['misconduct', 'worker_status']
- exclusion_flags: []
- 판단: 학원 강사 수습기간 중 해고. 수업준비 소홀·강의매뉴얼 미준수.

## id_26363
- primary/disposition: procedure / ['disciplinary_dismissal']
- secondary: ['misconduct', 'attendance']
- exclusion_flags: []
- 판단: 수습근로자 징계해고. 사유 인정되나 징계위 구성이 단협 위반(2인만).

## 특이사항 / 주의점
1. **id_25481**: 수습기간 임의 연장이 무효인 경우, employment_stage를 regular로 설정. 그러나 disposition_type은 형식상 본채용 거부였으므로 rejection_of_regular_employment 유지.
2. **id_25299**: 수습 합의 자체가 없는 경우도 unrelated_to_probation으로 처리. 사용자가 수습이라고 주장했을 뿐.
3. **id_26363**: 수습근로자이나 징계위원회를 통한 징계해고 처리. disposition_type은 disciplinary_dismissal. 절차 위반이 핵심.
4. **legacy 태그 오류**: id_26055의 union_activity는 보훈특별고용과 혼동된 것으로 보임. id_25889의 probation도 실질과 불일치.
