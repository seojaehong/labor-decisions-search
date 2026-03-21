# v2 Supabase 업로드 리포트

- 실행일: 2026-03-21
- 기준본: `retagging/output/merged/merged_final_v2.jsonl`

## Pre-Apply 상태

| 항목 | 건수 |
|------|------|
| DB 전체 nlrc_decisions | 42,105건 |
| v1 기준 태깅 반영 | 3,849건 |
| v2 적용 예정 | 3,923건 |
| 신규 추가 (v1 → v2) | +84건 |
| 기존 업데이트 (필드 갱신) | 3,839건 |
| missing/skip 예상 | 0건 (전체 case_id DB 존재 확인) |

## 스키마 마이그레이션

추가한 컬럼 7개 (`add_retag_v2_columns`):
- `include_for_queries TEXT[]`
- `exclude_for_queries TEXT[]`
- `tag_search_enabled BOOLEAN`
- `retag_snapshot_version TEXT`
- `retag_notes TEXT`
- `retag_source_basis TEXT`
- `retag_loaded_at TIMESTAMPTZ`

인덱스 4개 추가 (GIN x2, BTREE x2)

## Apply 결과

| 항목 | 결과 |
|------|------|
| 방식 | httpx asyncio 동시 20개 PATCH |
| 처리 건수 | 3,923건 |
| 성공 | 3,923건 (100%) |
| 실패 | 0건 |
| 소요 시간 | 24.1초 (~163건/s) |

## Post-Apply 검증

### DB 카운트
```
total_tagged=3923, v2_count=3923, v1_count=0
search_enabled=3923, primary_types=21
```

### issue_type_primary 분포 (JSONL ↔ DB 일치 확인)
| 태그 | JSONL | DB |
|------|-------|----|
| disciplinary_severity | 1,174 | 1,174 ✅ |
| dismissal_validity | 763 | 763 ✅ |
| misconduct | 432 | 432 ✅ |
| work_ability | 313 | 313 ✅ |
| workplace_harassment | 235 | 235 ✅ |

### Spot Check (8건 랜덤)
- issue_type_primary, tag_confidence, review_status, retag_snapshot_version 모두 정상
- include_for_queries, exclude_for_queries 배열 정상 반영
- fact_markers, legal_focus 배열 정상

### Candidate 경로 Smoke Test
- `tag_search_enabled = TRUE` 필터: 3,923건 ✅
- `include_for_queries && ARRAY[...]` 배열 겹침 검색: 정확 반환 ✅
- `exclude_for_queries` 보복성 사건 노조 혼입 방지: retaliation + exclude 정상 ✅
- retrieval.ts가 SELECT하는 모든 컬럼 존재 확인 ✅

## 잔여 작업

- notes 경고 61건 (confidence=medium 공란, exclusion_flags 2개+ 공란) — backlog
- merged_final_v2.jsonl → 기준본 확정, v1 archive 처리
