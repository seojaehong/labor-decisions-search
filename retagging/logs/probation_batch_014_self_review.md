# probation_batch_014 Self-Review

## 배치 개요
- **입력**: `retagging/input/batches/probation_batch_014.jsonl` (30건)
- **출력**: `retagging/output/reviewed/probation_batch_014_reviewed.jsonl` (30건)
- **작업일**: 2026-03-20

## 수습 vs 비수습 분류

### 수습(probation) 관련 사건 (26건)
| case_id | employment_stage | 분류 근거 |
|---------|-----------------|----------|
| id_29523 | probation | 수습 3개월 근무평가 하위 → 본채용 거부 정당 |
| id_29567 | probation | 수습 중 산재요양 본채용 거절 → 계약만료로 구제이익 소멸 |
| id_29575 | probation | 업무적격성 평가 52점(기준 80점) → 본채용 거부 정당 |
| id_29589 | probation | 시용기간 중 증빙 없이 해고 + 서면통지 미비 → 부당 |
| id_29597 | probation | 수습 경비원 업무지시 거부 → 본채용 거부 정당 |
| id_29605 | probation | 시용 3개월 업무평가 → 본채용 거부 정당 |
| id_29641 | probation | 수습 3개월 도과(6.26~9.30) → 시용해고 아닌 통상해고, 사유 부족 부당 |
| id_29699 | probation | 운전직 수습 계약외 업무 + 20일 평가 → 본채용 거부 부당 |
| id_2971 | probation | 계약직→정규직 전환 시용기간 + 괴롭힘 신고자 평가 객관성 인정 → 거부 정당 |
| id_29751 | probation | 근태불량 + 인사위원회 심의 → 본채용 거부 정당 |
| id_29757 | probation | 근무성적평가 70점 미달 면직 → 본채용 거부 정당 |
| id_29835 | probation | 간호사 투약오류 → 본채용 거부 정당 |
| id_29941 | probation | 택시 운행실적 40% 저조 → 해고 정당 |
| id_29969 | probation | 임원급 수습 6개월 사유·절차 미비 → 본채용 거부 부당 |
| id_29995 | probation | 요양보호사 수습 근무성적평가 → 본채용 거부 정당 |
| id_30207 | probation | 평가 36점(기준 60점) + 잦은 지각 → 본채용 거부 정당 |
| id_30253 | probation | 수습 2개월 업무지시 거부·민원·갈등 → 거부 정당 |
| id_30349 | probation | 수십 차례 출납 오류 → 본채용 거부 정당 |
| id_30355 | probation | 수습만료 사직권유 → 합의해지 → 구제이익 소멸 |
| id_30401 | probation | 시용 중 귀책사유 입증 부족 + 개선기회 미부여 → 해고 부당 |
| id_30411 | probation | 시용기간 도과 + 평가규칙 소급적용 불가 → 거부 부당 |
| id_30453 | probation | 수습 중 갈등유발 + 장기미근무 → 해고 정당 |
| id_30463 | probation | 시용기간 만료 → 정식근로자. 정직·해고 모두 부당 |
| id_30515 | probation | 업무적격성 70점 미달 + 시말서 이력 → 거부 정당 |
| id_30605 | probation | 의사 수습 49점 + 약품안전 미준수 → 거부 정당 |
| id_30673 | probation | 공공기관 수습 중 채용취소 — 사용자 과실로 부당 |

### 비수습(unrelated_to_probation) 사건 (4건)
| case_id | employment_stage | 분류 근거 |
|---------|-----------------|----------|
| id_29671 | fixed_term | 3개월 기간제 경비원. 시용 주장 불인정, 계약만료 종료 |
| id_29745 | regular | 취업규칙상 채용 확정 근로자 → 시용 불인정. 징계양정 과도 |
| id_29883 | fixed_term | 기간제 심리상담사. 갱신기대권 불인정. 수습 실질 판시 없음 |
| id_30365 | regular | 취업규칙 수습기간 임의규정 + 임금전액 → 시용 불인정. 징계양정 과도 |

## rejection vs termination 구분

### 본채용 거부(rejection_of_regular_employment) — 19건
id_29523, id_29567, id_29575, id_29597, id_29605, id_29699, id_2971, id_29751, id_29757, id_29835, id_29969, id_29995, id_30207, id_30253, id_30349, id_30411, id_30515, id_30605, id_30463(도과→dismissal로 재분류 포함)

### 시용기간 중 해고(probation_termination) — 4건
| case_id | disposition_type | 사유 |
|---------|-----------------|------|
| id_29589 | probation_termination | 시용기간 중 일방적 해고(재심 초심유지) |
| id_29941 | probation_termination | 택시 운행실적 저조 해고 |
| id_30401 | probation_termination | 시용기간 중 해고(사유 부존재) |
| id_30453 | probation_termination | 수습기간 중 해고(갈등+미근무) |

### 통상해고(dismissal) — 4건
| case_id | disposition_type | 사유 |
|---------|-----------------|------|
| id_29641 | dismissal | 수습 도과 후 해고(시용해고 아닌 통상해고) |
| id_30365 | dismissal | 시용 불인정, 통상 징계해고(양정 과도) |
| id_30463 | suspension, dismissal | 시용 도과 → 정식근로자 정직+해고 |
| id_30673 | dismissal | 공공기관 수습 중 채용취소 |

### 기타
| case_id | disposition_type | 사유 |
|---------|-----------------|------|
| id_29671 | contract_termination | 기간제 계약만료 |
| id_29745 | disciplinary_dismissal | 채용확정 근로자 징계해고(시용 아님) |
| id_29883 | nonrenewal | 기간제 갱신기대권 불인정 |
| id_30355 | no_formal_disposition | 합의해지로 구제이익 소멸 |

## 주요 판단 포인트

1. **수습기간 도과 사건 (id_29641, id_30411, id_30463)**: 수습기간 경과 후에는 통상근로자와 동일 해고절차 적용. rejection이 아닌 dismissal로 분류. 평가규칙 소급적용 불가(id_30411).

2. **시용관계 부인 사건 (id_29671, id_29745, id_30365)**: 기간제 계약(id_29671), 취업규칙 채용확정 조항(id_29745), 임의규정+임금전액(id_30365) → 시용근로자 불인정.

3. **갱신기대권 사건 (id_29883)**: 기간제 심리상담사, 1회 갱신만으로 기대권 불인정. 수습 태그 있으나 실질 무관.

4. **소규모 사업장 1인 평가자 (id_29605, id_29995, id_30515)**: 인력규모상 불가피한 경우 1인 평가자도 객관성 훼손 아님으로 일관 판단.

5. **산재요양 중 해고 (id_29567, id_29589)**: id_29567은 계약만료로 실질 판단 없이 각하, id_29589는 산재요양 중 해고를 부당사유의 하나로 적시.

6. **공공기관 채용취소 (id_30673)**: 서류전형 점수 산정 오류는 사용자 중과실이며, 수습기간이라는 점도 채용취소 정당화 근거 불가.

## 신뢰도 분포
- high: 28건
- medium: 2건 (id_29567 계약만료로 실질 판단 없음, id_30355 합의해지로 수습 실질 판시 없음)

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- review_status: 전건 "pending"
- tag_version: 전건 "v1"
