# 판정례 데이터 파이프라인 스크립트

## 데이터 업로드/분류

### upload_to_supabase.py
원본 마크다운 판정례를 Supabase에 업로드.
```bash
python3 scripts/upload_to_supabase.py              # 전체
python3 scripts/upload_to_supabase.py --dry-run    # 미리보기
```

### classify-reasons.js
키워드 패턴 기반 reason_category + sanction_type 일괄 분류.
```bash
node scripts/classify-reasons.js              # 전체
node scripts/classify-reasons.js --dry-run    # 통계만
node scripts/classify-reasons.js --limit 100  # 100건
```

### generate-embeddings.js
text-embedding-3-small 기반 document-level 임베딩 생성.
```bash
node scripts/generate-embeddings.js --dry-run    # 비용 추정
node scripts/generate-embeddings.js --limit 100  # 100건
node scripts/generate-embeddings.js              # 전체
```

## 재태깅 파이프라인

### retag-decisions.js
Haiku API 기반 다축 재태깅 배치 스크립트.
현재는 서브에이전트 방식을 권장하지만, API 배치 대안으로 사용 가능.
```bash
node scripts/retag-decisions.js --dry-run --limit 3   # 테스트
node scripts/retag-decisions.js --limit 100            # 100건
node scripts/retag-decisions.js --category absence     # 특정 카테고리
```

### validate_tagging_jsonl.py
재태깅 JSONL 결과 검증. 필수 필드, 타입, enum 허용값, 중복 case_id 검사.
```bash
python3 scripts/validate_tagging_jsonl.py retagging/output/draft/*.jsonl
python3 scripts/validate_tagging_jsonl.py retagging/output/draft/*.jsonl --report
```
검증 항목:
- JSON 파싱, 필수 필드 19개, 배열 타입 7개
- enum 허용값 (태그 사전 v1 기준)
- issue_type_primary 단일 문자열 여부
- case_id 중복 (파일 내 + 전체)
- notes 권장 경고 (confidence != high, exclusion_flags 2개+)

### merge_tagging_outputs.py
여러 JSONL 파일을 case_id 기준으로 스마트 병합.
```bash
python3 scripts/merge_tagging_outputs.py retagging/output/draft/*.jsonl --report
python3 scripts/merge_tagging_outputs.py retagging/output/draft/*.jsonl retagging/output/reviewed/*.jsonl -o retagging/output/merged/merged_v1.jsonl --report
```
병합 규칙:
- 배열 필드 (secondary, fact_markers 등): union merge
- 핵심 필드 (primary, employment_stage, disposition_type): 충돌 시 자동 병합 금지
- 핵심 충돌: logs/merge_collisions_report.md로 분리
- reviewed > draft 우선 (review_status 기반)
- confidence: 높은 쪽 유지
- 텍스트 필드: 더 긴 쪽 유지

## 디렉토리 구조

```
retagging/
  input/batches/       입력 JSONL (주제군별)
  output/draft/        서브에이전트 초안
  output/reviewed/     검수 완료본
  output/merged/       병합 결과
  logs/                진행 로그, 검증/병합 리포트
  prompts/             마스터 프롬프트, 태그 사전

docs/
  tagging-schema-v1.json   태그 사전 (enum 허용값)
```

## 작업 흐름

1. 입력 배치 생성 (DB에서 주제군별 JSONL 추출)
2. 서브에이전트로 태깅 (또는 retag-decisions.js API 배치)
3. validate로 검증
4. 필요시 검수 (reviewed 폴더)
5. merge로 병합 (충돌은 collision report로 분리)
6. **충돌 수동 판정 → override 적용**
7. 검색 품질 테스트
8. 확인 후 DB 반영

## 수동 충돌 처리 흐름

merge 실행 시 핵심 필드 충돌(issue_type_primary, employment_stage, disposition_type, industry_context)이 발견되면:

1. `logs/merge_collisions_report.md`에 충돌 상세가 기록됨
2. 사람이 검토 후 확정값을 결정
3. `output/reviewed/manual_merge_overrides_v1.json`에 확정값 기록
4. merge 재실행 시 `--overrides` 옵션으로 적용

```bash
# 충돌 확인
python3 scripts/merge_tagging_outputs.py retagging/output/reviewed/*.jsonl --report
# → logs/merge_collisions_report.md 확인

# 수동 판정 후 override 적용
python3 scripts/merge_tagging_outputs.py retagging/output/reviewed/*.jsonl \
  --overrides retagging/output/reviewed/manual_merge_overrides_v1.json \
  -o retagging/output/merged/merged_sample_v1.jsonl --report
```

override JSON 형식:
```json
{
  "overrides": [
    {
      "case_id": "id_XXXXX",
      "fields": { "issue_type_primary": "확정값" },
      "reason": "판정 근거"
    }
  ]
}
```

override 적용된 건은 `review_status: "final"`로 표시됨.
