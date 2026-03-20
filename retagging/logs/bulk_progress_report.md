# Bulk Retagging 진행 현황

최종 갱신: 2026-03-20

## 전체 요약

| 항목 | 값 |
|------|-----|
| reviewed 파일 | 28개 |
| reviewed 건수 | 790건 |
| **merged 고유 case_id** | **727건** |
| 자동 union merge | 19건 |
| **핵심 충돌** | **0건** (44건 override 해소) |
| override 누적 | 44건 |
| review_status final | 44건 |
| 에러 | 0 |

## 주제군별 진행

| 주제군 | input 배치 | reviewed 배치 | reviewed 건수 | 진행률 |
|--------|-----------|--------------|-------------|--------|
| probation | 33 | 5 + sample | 151건 | 15% |
| incompetence | 11 | 3 + sample | 90건 | 28% |
| absence | 33 | 5 + sample | 150건 | 15% |
| violence | 33 | 5 + sample | 170건 | 17% |
| workplace_bullying | 33 | 5 + sample | 170건 | 17% |
| **합계** | **143** | **28파일** | **790건** | |

## confidence 분포 (727건)

| 수준 | 건수 |
|------|------|
| high | ~620 (85%) |
| medium | ~105 (14%) |
| low | ~2 (0.3%) |

## issue_type_primary 분포 (727건)

| primary | 건수 |
|---------|------|
| disciplinary_severity | ~240 |
| dismissal_validity | ~130 |
| misconduct | ~130 |
| work_ability | ~80 |
| unfair_treatment | ~55 |
| renewal_expectation | ~40 |
| procedure | ~35 |
| workplace_harassment | ~25 |
| worker_status | ~2 |

## 다음 액션

1. 검색 품질 테스트 — 727건 merged 기반 대표 질의 5~10개
2. 효과 확인 후 DB 반영 여부 결정
3. 나머지 배치 (각 주제군 batch_006+) 진행
