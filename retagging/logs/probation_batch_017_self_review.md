# probation_batch_017 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_017.jsonl`
- 출력: `retagging/output/reviewed/probation_batch_017_reviewed.jsonl`
- 총 30건
- 작업일: 2026-03-20

## 수습 vs 비수습 분류

### 수습(probation) 관련 사건 (21건)
| case_id | employment_stage | 분류 근거 |
|---------|-----------------|----------|
| id_32957 | probation | 업무지시 거부와 직원 간 갈등을 이유로 본채용 거부 정당 |
| id_33023 | probation | 객관적 자료 부족 + 합리적 평가절차 부재로 본채용 거부 부당 |
| id_33087 | probation | 상급자와의 폭행사건을 이유로 본채용 거부 정당 |
| id_33125 | probation | 평가기준 미달 시용근로자 본채용 거부 정당 |
| id_33355 | probation | 평가점수 미달 및 절차 적정으로 본채용 거부 정당 |
| id_33379 | probation | 정직처분 다툼 중 사직으로 구제이익 소멸 |
| id_33403 | probation | 직무능력평가 저조 + 반복적 불화로 본채용 거부 정당 |
| id_33473 | probation | 채용경위 부적절 + 경력·자격 부족으로 본채용 거부 정당 |
| id_33481 | probation | 명예퇴직금 반납 약정 불이행으로 본채용 거부 정당 |
| id_33485 | probation | 교통사고를 이유로 정직 30일은 양정 과하지 않음 |
| id_33533 | probation | 합리적 사유와 적법 절차가 모두 인정됨 |
| id_33585 | probation | 수습평가의 객관성·공정성 결여로 거부 부당 |
| id_33735 | probation | 80점 기준 미달(60점) 본채용 거부 정당 |
| id_33763 | probation | 평가 객관성 부족 + 귀책 입증 부족으로 거부 부당 |
| id_33819 | probation | 객관적 기준 없는 주관 평가로 거부 부당 |
| id_33859 | probation | 무단결근·지시불응·수습평가 미달이 함께 문제된 복합 사건 |
| id_33901 | probation | 동종업체 근무경력 은폐로 본채용 거부 정당 |
| id_34167 | probation | 일부 징계사유 인정되나 해고 양정 과다 |
| id_34195 | probation | 사용자 적격 + 수습평가 재량 범위 내 본채용 거부 정당 |
| id_34209 | probation | 합리적 이유 부족으로 본채용 거부 부당 |
| id_34259 | probation | 평가점수 미달 및 절차 적법으로 본채용 거부 정당 |

### 비수습 또는 전환 사건 (9건)
| case_id | employment_stage | 분류 근거 |
|---------|-----------------|----------|
| id_33173 | regular | 수습이 아닌 정식근로자 해고의 서면통지 위반 |
| id_33185 | fixed_term | 기간제 갱신기대권 불인정 |
| id_3321 | regular | 시용근로자 아님. 일반 해고 기준으로 부당 판정 |
| id_33341 | regular | 시용성 부인 + 구두 해고 부당 |
| id_33921 | pre_hire | 견습·실습의 근로관계 성립이 먼저 인정된 사례 |
| id_34071 | regular | 수습 종료 후 정식근로자 해고의 서면통지 위반 |
| id_34079 | fixed_term | 기간제 갱신기대권 불인정 |
| id_34143 | regular | 수습 여부보다 일반 해고 사유 입증 실패가 핵심 |
| id_3423 | regular | 수습 규정을 정식근로자에게 적용한 해고 부당 |

## rejection vs termination 구분

### 본채용 거부(rejection_of_regular_employment) — 18건
`id_32957`, `id_33023`, `id_33087`, `id_33125`, `id_33355`, `id_33403`, `id_33473`, `id_33481`, `id_33533`, `id_33585`, `id_33735`, `id_33763`, `id_33819`, `id_33859`, `id_33901`, `id_33921`, `id_34209`, `id_34259`

### 시용기간 중 해고/징계(dismissal/suspension) — 9건
| case_id | disposition_type | 사유 |
|---------|-----------------|------|
| id_33379 | suspension | 정직처분 다툼 중 사직으로 구제이익 소멸 |
| id_33485 | suspension | 시용기간 교통사고에 대한 정직 30일 |
| id_33859 | suspension, rejection_of_regular_employment | 무단결근·지시불응·수습평가 미달이 함께 작동 |
| id_33173 | dismissal | 정식근로자 해고의 서면통지 위반 |
| id_3321 | dismissal | 시용근로자 아님에도 시용 기준으로 종료 |
| id_33341 | dismissal | 구두 해고 및 자진사직·합의해지 불인정 |
| id_34071 | dismissal | 수습 도과 후 정식근로자 해고 |
| id_3423 | dismissal | 수습 규정 오적용 |
| id_34143 | dismissal | 해고 사유 입증 부족 |

### 기간제/갱신기대권
| case_id | disposition_type | 사유 |
|---------|-----------------|------|
| id_33185 | nonrenewal | 갱신기대권 불인정 |
| id_34079 | nonrenewal | 갱신기대권 불인정 |

## 주요 경계 사례

1. `id_33379`
   - 징계 정당성 자체보다 사직으로 인한 구제이익 소멸이 먼저 결정되어 `fact_specific_low_reusability`와 `resignation_dispute`를 함께 두었다.
2. `id_33859`
   - 정직과 본채용 거부가 동시에 정당하다고 본 복합 사건이라 `disciplinary_severity`를 primary로 두고 `absence_without_leave`, `misconduct`, `dismissal_validity`를 보조로 넣었다.
3. `id_33921`
   - 시용보다 견습·실습의 근로자성 판단이 앞서는 사건이라 `pre_hire`로 보정했다.
4. `id_33473`, `id_34195`
   - 채용경위/사용자 적격/수습평가 재량이 겹치는 경계 사례라 `worker_status`와 `dismissal_validity` 사이를 신중하게 조정했다.
5. `id_33185`, `id_34079`
   - 수습 표기가 섞여 있어도 실질은 기간제 갱신기대권 사건이므로 `unrelated_to_probation`을 부여했다.

## 신뢰도 분포
- high: 24건
- medium: 6건

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 `pending`
- tag_version: 전건 `v1`
