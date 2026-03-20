# 세션 요약 — 2026-03-20

1. 5개 주제군 샘플 100건 재태깅 완료 (서브에이전트 5개 병렬, API 비용 $0)
   - high 95건, medium 5건, low 0건
   - 핵심 발견: 기존 단일 태그 정확도 ~40%

2. validate + merge 스크립트 완성, 실행 검증 완료
   - validate: 에러 0, 경고 49 (notes 비어있음 + 중복 case_id)
   - merge v2: 자동 union merge + 핵심 충돌 분리

3. merge collision 9건 존재 — 수동 검토 필요
   - performance vs work_ability (3건)
   - dismissal vs disciplinary_dismissal (3건)
   - misconduct vs workplace_harassment (2건)
   - misconduct vs disciplinary_severity (1건)

4. v1.1 후보 규칙 메모됨
   - performance/work_ability 통합 또는 구분 기준 명확화
   - dismissal/disciplinary_dismissal 구분 기준 태그 사전에 추가
   - notes 권장 조건 (confidence != high, exclusion_flags 2개+)

5. 다음 액션: collision policy 확정 → 5,000건 배치 확장 → 검색 품질 테스트

## 파일 목록

### 신규 생성
- scripts/validate_tagging_jsonl.py
- scripts/merge_tagging_outputs.py
- scripts/retag-decisions.js
- docs/tagging-schema-v1.json
- supabase_retag_schema.sql
- retagging/input/batches/*.jsonl (5파일)
- retagging/output/draft/*.jsonl (5파일)
- retagging/output/merged/merged_v1.jsonl
- retagging/logs/batch_status.md
- retagging/logs/merge_report.md
- retagging/logs/merge_collisions_report.md
- retagging/logs/validation_report.md

### 수정
- src/lib/types.ts (검색 reason_category 전환)
- src/app/search/page.tsx (reason_category 직접 검색)
- src/lib/ai/retrieval.ts (reason_category 매핑 + rerank 비활성)
- src/lib/ai/prompt.ts (마크다운 금지)
- src/app/api/sanction/route.ts (blocking JSON 복원)
- src/app/sanction/page.tsx (스트리밍 제거)
- scripts/upload_to_supabase.py (decision_result 매핑 수정)
- scripts/classify-reasons.js (sanction_months 보강)
- scripts/generate-embeddings.js (임베딩 파이프라인)
