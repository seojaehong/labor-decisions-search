# Tag Search Integration Plan

## 목표

`retagging/output/merged/merged_final_v1.jsonl`를 신규 8축 태그의 유일한 운영 기준본으로 삼고, 기존 `reason_category` 검색과 병행 비교 가능한 연결 경로를 만든다.

지금 단계의 우선순위는 덮어쓰기가 아니라 병행 운영이다.

## 기준 데이터 구분

### 운영 기준본

- 기준본: `retagging/output/merged/merged_final_v1.jsonl`
- 의미:
  - 충돌 adjudication 완료
  - override 반영 완료
  - case_id 기준 단일 확정본

### 비운영 중간본

- `retagging/output/reviewed/*.jsonl`
- 용도:
  - 배치 검토 결과 보존
  - 재검토/역추적/감사 로그
- 금지:
  - 서비스 검색 기준본으로 직접 사용하지 않음

정리:

- 서비스/DB 적재 기준은 항상 `merged_final_v1.jsonl`
- reviewed 전체는 생산/감사 산출물이지 검색 기준본이 아니다

## 현재 코드 기준 연결 포인트

### baseline 검색

- UI 검색:
  - `src/app/search/page.tsx`
  - 현재 `reason_category` + `search_vector` 기준
- AI retrieval:
  - `src/lib/ai/retrieval.ts`
  - 현재 후보 검색 흐름:
    1. `issue_type_primary` 기반 신규 태그 검색
    2. 부족하면 `reason_category` fallback
    3. 부족하면 `tags` fallback

### 현재 상태의 장단점

- 장점:
  - candidate 후보 검색 실험이 이미 일부 들어가 있음
  - baseline과 candidate를 같은 테이블에서 병행 가능
- 문제:
  - DB 컬럼 설계가 merged schema와 완전히 일치하지 않음
  - `include_for_queries`, `exclude_for_queries`, `notes` 저장 컬럼이 없음
  - 현재 `src/app/search/page.tsx`는 candidate 검색 경로를 전혀 노출하지 않음
  - baseline/candidate 비교 결과를 같은 쿼리에서 동시에 보기 어려움

## DB 반영 권장안

### 비교안

#### 1. 단일 JSON 컬럼

- 방식:
  - `retag_payload JSONB` 하나에 merged record 전체 저장
- 장점:
  - 적재가 단순
  - 스키마 변경이 적음
  - 원본 보존에 유리
- 단점:
  - 필터링/정렬/index 설계가 불편
  - 디버깅 시 쿼리가 장황
  - 앱 코드에서 조건 분기 비용이 큼

#### 2. 축별 개별 컬럼

- 방식:
  - `employment_stage`, `issue_type_primary`, `disposition_type` 등 각 축을 분리 저장
- 장점:
  - 검색/필터/index에 강함
  - Supabase query builder에서 사용이 쉬움
  - 디버깅이 직관적
- 단점:
  - schema drift 관리가 필요
  - merged schema 변경 시 DB migration 부담이 있음

#### 3. 혼합안

- 방식:
  - 검색 핵심 축은 개별 컬럼
  - 원본 전체는 `retag_payload JSONB`로 함께 저장
- 장점:
  - 검색 성능, 디버깅, 감사 추적을 같이 잡을 수 있음
  - 실서비스와 실험을 병행하기 좋음
  - 스키마 변경에도 payload가 안전망 역할
- 단점:
  - 저장 중복이 생김
  - 적재 매핑 규칙을 분명히 문서화해야 함

### 권장 결론

혼합안을 권장한다.

이유:

- 검색 시스템에서는 `issue_type_primary`, `employment_stage`, `disposition_type`, `fact_markers`, `legal_focus`, `industry_context`, `exclusion_flags`를 바로 조건에 써야 한다
- 반면 merged 원문을 그대로 보존하는 `retag_payload`도 필요하다
- 평가/디버깅 시 "DB 컬럼 값"과 "원본 merged record"를 나란히 볼 수 있어야 한다

## 운영용 컬럼 세트

현재 `supabase_retag_schema.sql` 초안은 방향은 맞지만 merged schema와 완전히 맞지 않는다.

추가/정리 권장 컬럼:

- `employment_stage TEXT`
- `issue_type_primary TEXT`
- `issue_type_secondary TEXT[]`
- `disposition_type TEXT[]`
- `fact_markers TEXT[]`
- `legal_focus TEXT[]`
- `industry_context TEXT`
- `exclusion_flags TEXT[]`
- `include_for_queries TEXT[]`
- `exclude_for_queries TEXT[]`
- `summary_short TEXT`
- `retrieval_note TEXT`
- `tag_confidence TEXT`
- `retag_notes TEXT`
- `retag_version TEXT`
- `review_status TEXT`
- `retag_source_basis TEXT`
- `retag_snapshot_version TEXT`
- `retag_loaded_at TIMESTAMPTZ`
- `retag_payload JSONB`

주의:

- DB에는 `tag_confidence`를 유지하되 merged의 `confidence`를 매핑한다
- DB에는 `retag_notes`를 유지하되 merged의 `notes`를 매핑한다

## 적재 기준

### 원칙

- source of truth:
  - `retagging/output/merged/merged_final_v1.jsonl`
- target table:
  - `nlrc_decisions`
- match key:
  - `merged.case_id == nlrc_decisions.id`

### 적재 방식

- 1차 권장:
  - `nlrc_decision_tag_candidates` staging table에 먼저 적재
- 2차 권장:
  - 검증 후 `nlrc_decisions` candidate 컬럼으로 승격
- baseline 필드(`reason_category`, `sanction_type`, `decision_result`, `search_vector`)는 유지
- candidate 필드만 병행 적재

### 적재 모드

1. `dry-run`
- 읽기 + 매핑 + 샘플 출력 + 누락 case_id 리포트

2. `apply`
- staging table이면 `case_id` 기준 upsert
- live table이면 case_id 기준 update
- 적재 결과 리포트 저장

## target table 최종 선택

### 권장 선택

구현 직전 기준으로는 `staging table -> live promotion` 경로를 권장한다.

이유:

- 첫 적재에서 `case_id` 누락 여부를 안전하게 검증 가능
- baseline 검색 경로를 건드리지 않고 candidate payload만 먼저 쌓을 수 있음
- compare 모드 구현 전에도 데이터 정합성 검사가 쉬움

### same-table이 더 나은 경우

아래 조건이 이미 만족되면 `nlrc_decisions` 직접 update도 가능하다.

- `id == case_id` 정합성이 안정적으로 검증됨
- 운영 테이블에 candidate 컬럼이 이미 적용됨
- rollback보다 compare 편의가 더 중요함

현재 권장 순서:

1. `supabase_retag_candidate_stage.sql`
2. `load_merged_tags_to_supabase.py --target-table nlrc_decision_tag_candidates --dry-run`
3. staging 검증
4. 필요시 live table 반영

## 검색 연결 전략

### 1. baseline 경로 유지

- 기존 `reason_category` 검색은 그대로 유지
- 의미:
  - 회귀 기준선
  - 비교 실험의 control group

### 2. candidate 경로 추가

- candidate 검색은 신규 8축 태그 기반
- 최소 검색축:
  - `issue_type_primary`
  - `employment_stage`
  - `disposition_type`
  - `fact_markers`
  - `legal_focus`
  - `industry_context`
  - `exclusion_flags`

### 3. compare 모드 추가

- 같은 query에 대해 baseline과 candidate 결과를 동시에 반환
- 추천 형태:
  - `search_mode=baseline`
  - `search_mode=candidate`
  - `search_mode=compare`

## 구현 순서 권장

1. DB migration 적용
2. `merged_final_v1.jsonl` dry-run 적재
3. 누락 case_id 및 컬럼 매핑 확인
4. apply 적재
5. `src/lib/ai/retrieval.ts`에서 baseline/candidate 분리 함수화
6. `src/app/search/page.tsx`에 compare mode 추가
7. before/after 실험 경로 연결

## 성공 조건

- DB 기준본이 `merged_final_v1.jsonl`로 통일됨
- baseline/candidate를 같은 쿼리에서 병행 비교 가능
- 서비스 검색에서 candidate 경로를 안전하게 켜고 끌 수 있음
- 디버깅 시 case_id 하나로 baseline reason과 candidate 8축을 함께 추적할 수 있음
