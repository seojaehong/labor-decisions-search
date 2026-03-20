# Bulk Retagging 진행 현황

최종 갱신: 2026-03-20

## 1차 bulk 완료 요약

| 주제군 | input 배치 | reviewed 배치 | reviewed 건수 | 진행률 |
|--------|-----------|--------------|-------------|--------|
| probation | 33 | 5 + sample | 151건 | 15% |
| incompetence | 11 | 3 + sample | 90건 | 28% |
| absence | 33 | 5 + sample | 150건 | 15% |
| violence | 33 | sample만 | 20건 | 2% |
| workplace_bullying | 33 | sample만 | 20건 | 2% |
| **합계** | **143** | **18파일** | **490건** | |

## 병합 결과

| 항목 | 값 |
|------|-----|
| 입력 파일 | 18개 (490건) |
| **merged 고유 case_id** | **464건** |
| 자동 union merge | 14건 |
| **핵심 충돌 (수동 검토 필요)** | **7건** |
| override 적용 (기존) | 5건 |
| 에러 | 0 |
| notes 권장 경고 | 16건 |

## 핵심 충돌 7건 (수동 판정 대기)

| case_id | 충돌 필드 | 소스 |
|---------|----------|------|
| id_14663 | industry_context, disposition_type | absence_005 vs incompetence_001 |
| id_11473 | issue_type_primary, industry_context | absence_001 vs probation_001 |
| id_13323 | issue_type_primary | incompetence_001 vs probation_003 |
| id_13583 | issue_type_primary | absence_004 vs probation_003 |
| id_14469 | primary, industry, disposition | absence_005 vs probation_004 |
| id_14493 | primary, industry, disposition | absence_005 vs probation_004 |
| id_16547 | primary, disposition | incompetence_001 vs probation_005 |

상세: logs/merge_collisions_report.md

## confidence 분포

| 수준 | 건수 |
|------|------|
| high | 396 (85%) |
| medium | 67 (14%) |
| low | 1 (0.2%) |

## issue_type_primary 분포 (464건)

| primary | 건수 | 비율 |
|---------|------|------|
| dismissal_validity | 107 | 23% |
| disciplinary_severity | 100 | 22% |
| misconduct | 82 | 18% |
| work_ability | 80 | 17% |
| renewal_expectation | 38 | 8% |
| procedure | 35 | 8% |
| workplace_harassment | 11 | 2% |
| unfair_treatment | 10 | 2% |
| worker_status | 1 | 0.2% |

## 다음 액션

1. **수동 판정**: 충돌 7건 검토 → manual_merge_overrides_v1.json 추가
2. **2차 bulk**: violence_batch_001+, workplace_bullying_batch_001+ 진행
3. **검색 품질 테스트**: 464건 기반 대표 질의 테스트 가능
