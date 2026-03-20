# DB Reflection Design

## 결론

DB 반영은 `혼합안`으로 간다.

- 검색 핵심 축: 개별 컬럼
- 감사/복구용 원본: `retag_payload JSONB`

## 왜 단일 JSON만으로는 부족한가

실제 검색/필터/디버깅에서는 아래 질의가 자주 필요하다.

- `issue_type_primary = 'disciplinary_severity'`
- `employment_stage = 'probation'`
- `disposition_type`에 `disciplinary_dismissal` 포함
- `exclusion_flags`에 `not_really_absence_case` 포함
- `legal_focus`에 `proportionality` 포함

이 질의들을 JSONB path 기반으로만 처리하면:

- index 설계가 불편하고
- Supabase query builder 코드가 장황해지며
- 디버깅이 어려워진다

## 왜 축별 컬럼만으로도 부족한가

merged schema는 서비스용 요약이면서 동시에 감사 가능한 기준본이다.

실무적으로는 아래가 자주 필요하다.

- 적재 전/후 원문 동일성 확인
- 특정 case_id의 원본 merged 레코드 확인
- 스키마 확장 시 손실 없이 후속 컬럼 재생성

그래서 `retag_payload JSONB`는 계속 유지하는 것이 좋다.

## 권장 컬럼 구조

### 필수 검색 컬럼

- `employment_stage TEXT`
- `issue_type_primary TEXT`
- `issue_type_secondary TEXT[]`
- `disposition_type TEXT[]`
- `fact_markers TEXT[]`
- `legal_focus TEXT[]`
- `industry_context TEXT`
- `exclusion_flags TEXT[]`

### 보조 검색/디버깅 컬럼

- `include_for_queries TEXT[]`
- `exclude_for_queries TEXT[]`
- `summary_short TEXT`
- `retrieval_note TEXT`

### 메타 컬럼

- `tag_confidence TEXT`
- `retag_notes TEXT`
- `retag_version TEXT`
- `review_status TEXT`
- `retag_source_basis TEXT`
- `retag_snapshot_version TEXT`
- `retag_loaded_at TIMESTAMPTZ`

### 원본 보존 컬럼

- `retag_payload JSONB`

## 권장 인덱스

- B-tree
  - `issue_type_primary`
  - `employment_stage`
  - `industry_context`
  - `retag_version`
  - `retag_snapshot_version`
  - `review_status`

- GIN
  - `issue_type_secondary`
  - `disposition_type`
  - `fact_markers`
  - `legal_focus`
  - `exclusion_flags`
  - `include_for_queries`
  - `exclude_for_queries`

## 기존 baseline 컬럼과의 관계

유지:

- `reason_category`
- `reason_detail`
- `sanction_type`
- `decision_result`
- `search_vector`
- 기타 원본 메타

원칙:

- baseline 컬럼은 기존 경로를 유지하는 기준선
- candidate 컬럼은 신규 실험/서비스 경로
- 둘을 서로 덮어쓰지 않는다

## 추천 저장 모델

| 항목 | 저장 위치 | 이유 |
|------|-----------|------|
| 서비스 검색 필터 | 축별 컬럼 | 빠른 필터링 |
| 디버깅/추적 | `retag_payload` | 원본 보존 |
| 오프라인 평가용 설명 | `summary_short`, `retrieval_note`, `retag_notes` | 결과 해석 |
| 실험 스냅샷 관리 | `retag_snapshot_version` | 버전 고정 |

## 서비스 기준본 명시

운영 배포 전까지 `retag_snapshot_version = 'merged_final_v1'`를 기준 스냅샷으로 고정한다.

이 값을 기준으로:

- compare 모드
- 회귀 테스트
- 실험 로그
- 후속 재적재

를 전부 통일한다.

## target table 권장안

최종 서비스 조회는 `nlrc_decisions`를 사용하더라도, 첫 적재는 staging table이 더 안전하다.

권장 단계:

1. `nlrc_decision_tag_candidates`에 적재
2. case_id 정합성 및 누락 검증
3. compare/QA 확인
4. 이후 `nlrc_decisions` candidate 컬럼으로 승격

즉:

- 저장 모델은 same-table compare에 유리하게 설계
- 첫 반영은 staging-first로 운영
