# Phase 3: Analyze API를 Hybrid RPC로 전환

## 목표
labor-law-guide 앱의 `/api/analyze` 경로가 현재 `search_similar_cases` (trigram only)를 호출하는데,
이를 `search_similar_cases_hybrid` (trigram + vector)로 교체하여 검색 품질 향상.

## 의존성
- Phase 2 (Query Rewriting)가 먼저 완료되어야 함
- 또는 Phase 2 없이 embedding만 추가해도 독립 실행 가능

## 배경
- Supabase project: `mewqgevgdgghhatqtuos`
- `search_similar_cases_hybrid` RPC는 이미 배포됨
- nlrc_decisions 테이블에 `embedding` 컬럼(vector(1536)) 존재
- ivfflat 인덱스 생성 완료

## 작업 내용

### 1. Embedding 생성 유틸리티 추가
**파일:** `src/lib/embedding.ts` (신규, labor-law-guide 레포)
**위치:** `/home/ubuntu/work-orchestrator/repos/labor-law-guide/src/lib/embedding.ts`

```typescript
const OPENAI_EMBEDDING_MODEL = 'text-embedding-3-small';

export async function createEmbedding(text: string): Promise<number[] | null> {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return null;

  try {
    const response = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: OPENAI_EMBEDDING_MODEL,
        input: text.slice(0, 8000), // 토큰 제한
      }),
    });

    const payload = await response.json();
    return payload.data?.[0]?.embedding ?? null;
  } catch {
    return null;
  }
}

// Supabase vector 형식으로 변환
export function toVectorLiteral(embedding: number[]): string {
  return `[${embedding.join(',')}]`;
}
```

### 2. Analyze API 수정
**파일:** `/home/ubuntu/work-orchestrator/repos/labor-law-guide/src/app/api/analyze/route.ts`

현재 코드 (변경 전):
```typescript
const { data, error } = await supabaseAdmin.rpc('search_similar_cases', {
  query,
  category,
  limit,
});
```

변경 후:
```typescript
import { createEmbedding, toVectorLiteral } from '@/lib/embedding';

// 1. embedding 생성 시도
const embedding = await createEmbedding(query);

let data;
if (embedding) {
  // 2. hybrid search 시도
  const result = await supabaseAdmin.rpc('search_similar_cases_hybrid', {
    query,
    query_embedding: toVectorLiteral(embedding),
    category,
    limit: limit || 15,
    trigram_weight: 0.4,
    semantic_weight: 0.6,
  });

  if (!result.error && result.data?.length > 0) {
    data = result.data;
  }
}

if (!data) {
  // 3. fallback: trigram only
  const result = await supabaseAdmin.rpc('search_similar_cases', {
    query,
    category,
    limit,
  });
  data = result.data;
}
```

### 3. Cases API도 동일 패턴 적용 (선택)
**파일:** `/home/ubuntu/work-orchestrator/repos/labor-law-guide/src/app/api/cases/route.ts`

현재 `search_cases` RPC → `search_similar_cases_hybrid` 전환 가능.
단, cases API는 pagination 있으므로 구조가 다름. 우선순위 낮음.

### 4. 환경변수 설정
**파일:** `/home/ubuntu/work-orchestrator/repos/labor-law-guide/.env.local` (또는 Vercel 환경변수)

필요한 키:
```
OPENAI_API_KEY=sk-...
```

현재 이 키는 labor-decisions-search 레포의 `supabase/.env`에만 있음.
labor-law-guide에도 동일 키 설정 필요.

## 참고 파일
- labor-decisions-search의 `src/lib/ai/retrieval.ts` — embedding 생성 + hybrid RPC 호출 패턴 참고
- labor-law-guide의 `src/app/api/analyze/route.ts` — 현재 analyze 코드
- labor-law-guide의 `src/app/api/cases/route.ts` — 현재 cases 검색 코드

## Supabase RPC 시그니처 (이미 배포됨)
```sql
search_similar_cases_hybrid(
  query text,
  query_embedding vector,
  category text default '',
  "limit" integer default 5,
  trigram_weight real default 0.4,
  semantic_weight real default 0.6
) returns table (
  id text, title text, decision_result text,
  holding_summary text, summary_short text, key_issue text,
  reason_category text[], sanction_type text,
  decision_date date, url text, relevance real
)
```

## 완료 기준
- [ ] `src/lib/embedding.ts` 구현
- [ ] `/api/analyze` 경로에서 hybrid RPC 호출
- [ ] embedding 실패 시 trigram fallback 동작
- [ ] 로컬에서 테스트 쿼리 실행 확인
- [ ] 타입 에러 없음
