# Bulk Retagging 진행 현황

최종 갱신: 2026-03-20

## 배치 현황

| 주제군 | 전체 | input 배치 | reviewed | 진행률 |
|--------|------|-----------|----------|--------|
| probation | 974 | 33 | **1** (batch_001, 30건) | 3% |
| incompetence | 322 | 11 | 0 | 0% |
| absence | 980 | 33 | 0 | 0% |
| violence | 977 | 33 | 0 | 0% |
| workplace_bullying | 979 | 33 | 0 | 0% |
| **합계** | **4,232** | **143** | **1** | **0.7%** |

## 누적 통계 (샘플 + bulk)

| 항목 | 값 |
|------|-----|
| 총 reviewed 건수 | 130건 (샘플 100 + bulk 30) |
| merged 고유 case_id | 114건 |
| 에러 | 0 |
| 경고 | 3건 (notes 권장) |
| 핵심 충돌 | 0건 |
| override 적용 | 5건 (샘플 단계 확정) |
| 수동 판정 대기 | 0건 |

## 배치별 상세

| 배치 | 건수 | 에러 | 경고 | 충돌 | confidence |
|------|------|------|------|------|-----------|
| 샘플 5종 (100건) | 84 고유 | 0 | 3 | 5→0 (override) | high 81, med 3 |
| probation_batch_001 | 30 | 0 | 0 | 0 | high 28, med 2 |

## issue_type_primary 분포 (전체 114건)

| primary | 건수 |
|---------|------|
| dismissal_validity | 25 |
| misconduct | 19 |
| work_ability | 19 |
| disciplinary_severity | 15 |
| procedure | 13 |
| renewal_expectation | 10 |
| workplace_harassment | 9 |
| unfair_treatment | 3 |
| worker_status | 1 |

## 다음 대기 배치

probation_batch_002, 003 → incompetence_batch_001~003 → absence_batch_001~003
