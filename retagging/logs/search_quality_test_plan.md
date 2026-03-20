# 검색 품질 테스트 계획

merged 727건 기준. 태그 체계가 실제 retrieval에서 작동하는지 점검.

## 대표 검색 질의셋 (15개)

### A. 수습해고 (probation)

| # | 질의 | 기대 회수 | 기대 제외 |
|---|------|----------|----------|
| A1 | "수습 6개월 판매실적 미달 본채용거부" | employment_stage=probation + disposition=rejection + fact=sales_target_not_met | renewal_stage 사건, 정규직 해고 |
| A2 | "수습기간 중 업무능력 부족으로 해고" | employment_stage=probation + disposition=probation_termination | rejection_of_regular_employment (만료 시 거부 아님) |
| A3 | "시용근로자 본채용 거부 절차 위반" | primary=procedure + employment_stage=probation | 정규직 절차위반 사건 |

점검 포인트:
- rejection(110건) vs termination(21건) 구분이 질의 의도에 맞게 분리되는지
- "수습해고" 질의에 renewal_stage 사건이 섞이지 않는지

### B. 저성과/업무능력부족 (incompetence)

| # | 질의 | 기대 회수 | 기대 제외 |
|---|------|----------|----------|
| B1 | "정규직 저성과 해고 개선기회" | primary=work_ability + employment_stage=regular + fact=improvement_opportunity_given | 수습 사건, 갱신기대권 |
| B2 | "인사평가 기반 해고 정당성" | primary=work_ability or dismissal_validity + fact=quantitative_evaluation | 절차 위반 중심 사건 |
| B3 | "업무능력 부족 경고 후 해고" | fact=warning_given + work_ability secondary 이상 | 무단결근 사건 |

점검 포인트:
- work_ability(80건) vs dismissal_validity(121건): "업무능력"을 묻는 질의에 dismissal_validity가 과잉 회수되지 않는지
- not_really_performance_case exclusion이 작동하는지

### C. 무단결근 (absence)

| # | 질의 | 기대 회수 | 기대 제외 |
|---|------|----------|----------|
| C1 | "반복 무단결근 해고" | primary=absence_without_leave 또는 fact=repeated_absence + unauthorized_absence | 결근이 배경사실일 뿐인 사건 |
| C2 | "무단결근인데 실제 핵심이 절차위반" | primary=procedure + fact=unauthorized_absence + exclusion=not_really_absence_case | 진짜 결근 사건 |

점검 포인트:
- absence primary가 극소수(merged에서 거의 없음) → secondary로 잡힌 결근 사건 139건 중 실제 결근 핵심은 소수
- not_really_absence_case(98건) exclusion이 노이즈 제거에 효과적인지

### D. 징계양정 (violence → disciplinary_severity)

| # | 질의 | 기대 회수 | 기대 제외 |
|---|------|----------|----------|
| D1 | "폭행 해고 양정 과다" | primary=disciplinary_severity + fact=evidence_sufficient + legal=proportionality | misconduct(비위 존부만 다툰 사건) |
| D2 | "징계사유 인정되지만 해고가 과한 경우" | primary=disciplinary_severity + legal=social_norm_reasonableness | dismissal_validity(해고 존재 자체 다툼) |
| D3 | "정직 처분 양정 적정성" | primary=disciplinary_severity + disposition=suspension | 해고 사건 |

점검 포인트:
- disciplinary_severity(234건)가 가장 큰 카테고리 — 과잉 회수 위험
- misconduct(127건)와의 경계: "비위 사실이 있는가" vs "양정이 적정한가"

### E. 직장내 괴롭힘 (workplace_bullying)

| # | 질의 | 기대 회수 | 기대 제외 |
|---|------|----------|----------|
| E1 | "직장내 괴롭힘 성립 여부" | primary=workplace_harassment | not_really_harassment_case 제외 |
| E2 | "괴롭힘 신고 후 불이익조치" | primary=retaliation 또는 secondary=retaliation | 괴롭힘 자체 성립 사건 |
| E3 | "괴롭힘 관련 징계인데 양정 과다" | primary=disciplinary_severity + secondary=workplace_harassment | 괴롭힘 성립 자체가 핵심인 사건 |

점검 포인트:
- not_really_harassment_case(184건)가 가장 많은 exclusion — 이게 실제로 노이즈를 잘 걸러내는지
- workplace_harassment(26건)가 적은 건 정상 — 괴롭힘 "성립 여부"만 핵심인 사건이 실제로 적기 때문

## 점검 방법

### 1단계: JSONL 기반 시뮬레이션

merged_sample_v1.jsonl에서 각 질의 조건으로 필터링:
```python
# 예: 질의 A1
results = [r for r in merged
    if r['employment_stage'] == 'probation'
    and 'rejection_of_regular_employment' in r['disposition_type']
    and 'sales_target_not_met' in r.get('fact_markers', [])]
```

### 2단계: 정밀도 점검

각 질의별로:
- top 10 회수 사건의 summary_short 확인
- 관련 없는 사건이 섞여있는지 (노이즈율)
- 있어야 할 사건이 빠졌는지 (누락율)

### 3단계: exclusion_flags 효과 측정

동일 질의를 exclusion 적용/미적용으로 비교:
- exclusion 없이 회수 건수
- exclusion 적용 후 회수 건수
- 제거된 건 중 실제 노이즈 비율

## 과잉회수 위험 패턴

| 패턴 | 위험 | 대응 |
|------|------|------|
| disciplinary_severity 234건 | "징계" 질의에 너무 많이 잡힘 | disposition_type + fact_markers로 세분화 필요 |
| dismissal_validity 121건 | 해고 관련 모든 질의에 과잉 | employment_stage + disposition 조합으로 좁히기 |
| not_really_harassment_case 184건 | 괴롭힘 검색 시 대량 제외 | 정상 — 실제 괴롭힘 핵심 사건이 26건뿐 |
| misconduct 127건 | 비위 유형별 구분 안 됨 | secondary로 세분화 (폭행/횡령/기밀유출 등) |

## 누락 위험 패턴

| 패턴 | 위험 | 대응 |
|------|------|------|
| absence primary 극소수 | "무단결근 해고" 질의에 primary 매칭 거의 없음 | fact_markers (repeated_absence, unauthorized_absence) 기반 검색 병행 |
| worker_status 1건 | 근로자성 검색 거의 불가 | 현재 배치에 worker_status 사건이 적었음, 추가 배치 필요 |
| retaliation 0건(merged) | 보복 불이익 검색 불가 | secondary에 있을 수 있음, 확인 필요 |

## 권장 점검 우선순위

1. **A1 + A2**: rejection vs termination 구분 — 실무에서 가장 자주 혼동
2. **C1**: 무단결근 진짜 사건 회수율 — 레거시 대비 개선 확인
3. **E1 + E3**: 괴롭힘 성립 vs 양정 분리 — exclusion 효과 핵심
4. **D1 + D2**: disciplinary_severity 과잉회수 여부
5. **B1**: 정규직 저성과 사건이 수습 사건과 분리되는지
