# Bulk Retagging 진행 현황

최종 갱신: 2026-03-20 22:00

## 전체 요약

| 항목 | 값 |
|------|-----|
| reviewed 파일 | 96개 |
| reviewed 건수 | 2,788건 |
| **merged 고유 case_id** | **2,561건** |
| 자동 union merge | 73건 |
| **핵심 충돌** | **0건** |
| override 누적 | 130건 |
| review_status final | 129건 |
| 에러 | 0 |

## 주제군별 진행

| 주제군 | input 배치(총) | 완료 배치 | reviewed 건수 | 잔여 |
|--------|:---:|:---:|:---:|:---:|
| probation | 33 | sample+001~014+015~030+032 (31) | ~940 | 031,033 |
| incompetence | 11 | sample+001~011 (12) | ~322 | **완료** |
| absence | 33 | sample+001~014+031~033 (18) | ~510 | 015~030 |
| violence | 33 | sample+001~014+031~033 (18) | ~510 | 015~030 |
| workplace_bullying | 33 | sample+001~014+031~033 (18) | ~510 | 015~030 |
| **합계** | **143** | **97** | **2,788** | **46** |

## 진행률

- 배치 기준: 97/143 = **68%**
- 건수 기준: 2,561/4,232 = **61%** (고유 case_id)
- incompetence: 100% 완료
- probation: 94% (031,033 미완)
- absence/violence/bullying: 각 55% (015~030 미완)

## 잔여 작업

### 즉시 가능
- absence/violence/bullying batch_015~030 (48배치, ~1,440건)
- probation batch_031, 033 (2배치, ~60건)

### 잔여 배치 배정 제안
- Claude: absence 015~023 (9배치)
- Codex: violence 015~023 + bullying 015~023 (18배치)
- 또는 둘 다 주제 섞어서 3배치씩 병렬

## confidence 분포 (2,561건)

| 수준 | 건수 | 비율 |
|------|------|------|
| high | 2,357 | 92% |
| medium | 202 | 8% |
| low | 2 | 0.1% |

## issue_type_primary 분포 (2,561건)

| primary | 건수 | 비율 |
|---------|------|------|
| disciplinary_severity | 602 | 24% |
| dismissal_validity | 597 | 23% |
| misconduct | 320 | 12% |
| work_ability | 287 | 11% |
| procedure | 161 | 6% |
| renewal_expectation | 137 | 5% |
| workplace_harassment | 127 | 5% |
| absence_without_leave | 86 | 3% |
| unfair_treatment | 83 | 3% |
| transfer_validity | 69 | 3% |
| worker_status | 48 | 2% |
| 기타 | 44 | 2% |
