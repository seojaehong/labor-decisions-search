# BigCase autoresearch

BigCase 판례 데이터(nlrc_decisions, 57,574건)의 품질을 자율적으로 측정→개선→검증하는 자동 연구 루프.
Karpathy의 autoresearch 패턴을 데이터 품질 개선에 적용.

## 환경

- DB: Supabase (mewqgevgdgghhatqtuos)
- 테��블: nlrc_decisions (bc_* 15,742건 + id_* 41,729건 + 기타)
- Supabase 키: /home/ubuntu/work-orchestrator/repos/labor-law-guide/supabase/.env
- 레포: /home/ubuntu/work-orchestrator/repos/labor-decisions-search/
- 기존 스크립트: scripts/ 디렉토리 (bigcase_*.py, upload_to_supabase.py 등)

## 평가 함수 (고정, 수정 금지)

```bash
python3 autoresearch/benchmark.py
```

핵심 지표: `quality_score` (0~100, lower is better)
구성:
- confidence_level NULL 비율 × 30
- tier NULL 비율 × 20
- holding_summary NULL 비율 × 25
- key_issue NULL 비�� × 15
- reason_category NULL 비율 × 10

## 수정 가능 범위

**CAN do:**
- Supabase에 SQL 실행 (UPDATE, INSERT, ALTER)
- scripts/ 디렉토리의 기존 Python 스크립트 활용 및 수정
- autoresearch/experiments/ 에 새 스크립트 작성
- 프론트엔드 코드(src/) 수정 (스키마 정합성)

**CANNOT do:**
- autoresearch/benchmark.py 수정 (평가 함수 고정)
- 데이터 삭제 (DELETE 금지 — UPDATE/INSERT만)
- 외부 패키지 추가 설치

## 알려진 문제들

1. **search_tsv 컬럼**: 수동으로 만든 빈 컬럼. 실제 검색은 search_vector(GENERATED ALWAYS) 사용 중. search_tsv는 정리 대상.
2. **bc_ confidence_level 전부 NULL**: 15,742건. id_는 대부분 0.9로 세팅됨.
3. **tier NULL 20,912건**: 분류 기준 부재.
4. **holding_summary/key_issue NULL**: bc_ 레코드 중 일부 텍스트 필드 비어있음.
5. **reason_category NULL**: 태깅 미완료 레코드.

## 데이터 스키마 참조

supabase_schema.sql:
- search_vector: tsvector GENERATED ALWAYS AS (to_tsvector('simple', coalesce(title,'') || ' ' || coalesce(holding_points,'') || ' ' || coalesce(holding_summary,'') || ' ' || coalesce(reason_detail,'') || ' ' || coalesce(key_issue,''))) STORED

supabase_retag_schema.sql:
- reason_category, legal_focus, disposition_type, fact_markers, tag_confidence 등

## confidence_level 기준

bc_ 레코드 confidence_level 세팅 기준:
- 0.9: title + holding_summary + key_issue + reason_category 모두 있음
- 0.7: title + holding_summary 있음, 나머지 일부 NULL
- 0.5: title만 있고 나머지 대부분 NULL
- 0.3: title도 부실하거나 텍스트 극히 짧음

## tier 기준

- high_priority: 실무 빈출 카테고리 (직장내괴롭힘, 부당해고, 임금체불, 산업재해)
- standard: 일반 카테고리
- low_priority: 특수/희귀 사례

reason_category 기준:
- high_priority 매핑: workplace_bullying, unfair_dismissal, wage_theft, industrial_accident, sexual_harassment, probation_dismissal
- standard: 나머지 모든 유효 카테고리
- low_priority: reason_category IS NULL 이고 텍스트 정보 부족

## 로깅

results.tsv (탭 구분):
```
timestamp	quality_score	conf_null_pct	tier_null_pct	holding_null_pct	status	description
```

status: keep | discard | crash

## 실험 루프

LOOP:
1. benchmark.py 실행 → 현재 quality_score 기록
2. 문제 하나 선택 (가장 큰 NULL 비율부터)
3. 수정 SQL/스크립트 작성 및 실행
4. benchmark.py 재실행 → 새 quality_score
5. 개선됐으면 keep → results.tsv 기록 → 다음 실험
6. 악화됐으면 discard → 롤백 SQL 실행 → results.tsv 기록 → 다른 접근
7. GOTO 1

## 우선순위 (추천 실험 순서)

1. bc_ confidence_level 일괄 세팅 (15,742건, 가장 큰 영향)
2. tier 일괄 세팅 (20,912건)
3. holding_summary NULL인 bc_ 레코드 보강 (원문에서 추출 가능한지)
4. reason_category NULL 레코드 재태깅
5. key_issue NULL 레코드 보��
6. search_tsv 컬럼 정리 (DROP 또는 search_vector와 동기화)

## 절대 멈추지 마라

실험 루프가 시작되면, 사람에게 "계속할까요?" 묻지 않는다.
아이디어가 떨어지면 더 생각한다:
- scripts/ 디렉토리의 기존 스크립트를 읽고 활용법을 찾는다
- supabase_schema.sql, supabase_retag_schema.sql을 다시 읽는다
- 프론트엔드 코드(src/lib/search/)를 읽고 실제 사용되는 필드를 파악한다
- 이전 실험에서 discard된 접근의 변형을 시도한다
사람이 수동으로 멈출 때까지 무한 반���한다.
