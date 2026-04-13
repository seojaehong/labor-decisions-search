# Phase 4: AI Re-ranking (최종 품질 부스트)

## 목표
Hybrid RPC 결과 top 20개를 AI가 쿼리 의도에 맞게 재평가하여 최종 top 5를 선별.
목표: 79% → 90-95% 정확도.

## 의존성
- Phase 3 (Hybrid RPC 통합) 완료 필요
- 독립 실행도 가능 (search_similar_cases 결과에도 적용 가능)

## 작업 내용

### 1. AI Re-ranker 함수 생성
**파일:** `src/lib/ai/reranker.ts` (신규, labor-decisions-search 레포)

```typescript
interface RankedResult {
  id: string;
  title: string;
  relevanceScore: number;    // AI가 부여한 0-10 점수
  reasoning: string;         // 왜 이 점수인지 한줄 설명
}

export async function rerankResults(
  userQuery: string,
  results: SearchResult[],   // hybrid RPC 결과 (top 20)
  topK: number = 5
): Promise<RankedResult[]>
```

### 2. Re-ranking 프롬프트

```
당신은 노동법 판례 검색 결과를 평가하는 전문가입니다.

사용자 검색 쿼리: "{userQuery}"

아래 검색 결과들을 쿼리와의 관련성 기준으로 0-10점으로 평가해주세요.

평가 기준:
- 10점: 쿼리가 정확히 묻는 법적 쟁점을 다루는 사건
- 8-9점: 동일 쟁점이나 세부 맥락이 약간 다른 사건
- 5-7점: 관련 주제이나 핵심 쟁점이 다른 사건
- 3-4점: 일부 키워드만 겹치는 사건
- 0-2점: 쿼리와 무관한 사건

특히 중요한 구분:
- "양정 과다" 쿼리: 징계사유는 인정되지만 징계 수위가 과한지를 다루는 사건이 높은 점수
- "절차 하자" 쿼리: 서면통지, 소명기회 등 절차적 문제를 다루는 사건이 높은 점수
- "성립 여부" 쿼리: 비위 사실 자체의 존부가 핵심인 사건이 높은 점수
- 형사사건, 군사법 사건, 종중/교회 내부 분쟁은 0점

검색 결과:
{results를 번호+title+key_issue 형태로 나열}

JSON 배열로 응답해주세요:
[{"id": "...", "score": 10, "reason": "..."}]
```

### 3. 모델 선택
- **추천:** `claude-haiku-4-5-20251001` (빠르고 저렴)
- **대안:** `gpt-4o-mini` (이미 API키 있음)
- 비용: 쿼리당 ~$0.005-0.02
- 지연시간: ~1-2초 추가

### 4. 통합 위치

**labor-decisions-search:** `src/lib/ai/retrieval.ts`의 `searchCasesViaRpc()` 함수 뒤에 추가

```typescript
// 기존 코드
const results = await searchCasesViaRpc(query, category, 20); // limit을 20으로 증가

// 새로 추가
const reranked = await rerankResults(originalQuery, results, 5);

// reranked 결과를 점수순 정렬 후 반환
return reranked
  .sort((a, b) => b.relevanceScore - a.relevanceScore)
  .slice(0, 5);
```

**labor-law-guide:** `/api/analyze` 경로에도 동일 패턴 적용

### 5. 캐싱 전략
- 동일 쿼리+결과 조합에 대해 re-ranking 결과를 메모리 캐시 (5분)
- 캐시 키: `hash(query + resultIds.join(','))`
- API 비용 절감 효과

### 6. 에러 처리
- AI re-ranking 실패 시 → 원본 hybrid 결과 그대로 반환 (graceful degradation)
- 타임아웃: 5초 (초과 시 원본 반환)
- API 키 없음: re-ranking 스킵

## 참고: 현재 스코어링 함수들 (Supabase에 배포됨)

```sql
-- 1. compute_search_trigram_score(query, title, holding_summary, key_issue, summary_short)
-- title similarity * 0.5 + holding * 0.2 + key_issue * 0.2 + summary * 0.1

-- 2. compute_search_metadata_boost(query, sanction_type, reason_category, holding_summary, title)
-- 18개 패턴 (A-R): sanction 정합, 양정, 절차, 보복, 복합비위, 운수업, 갱신기대권, 근로자성 등

-- 3. is_non_labor_case(title, holding_summary)
-- 형사/군사법/종중/교회/재판권면제 사건 필터
```

## 평가 방법
아래 24개 쿼리로 re-ranking 전/후 비교:
(Phase 2 프롬프트의 동일 24개 쿼리 사용)

각 쿼리에 대해:
1. Hybrid RPC 결과 top 20 가져오기
2. AI re-ranking 적용
3. 최종 top 5의 관련성 점수 채점 (0/1/2 기준)
4. 가중 합산 (1위×3 + 2위×2.5 + 3위×2 + 4위×1.5 + 5위×1)

## 완료 기준
- [ ] `reranker.ts` 구현 (프롬프트 + API 호출 + JSON 파싱)
- [ ] retrieval.ts에 통합 (searchCasesViaRpc 뒤)
- [ ] 캐싱 로직 구현
- [ ] fallback 동작 확인 (AI 실패 시 원본 반환)
- [ ] 3개 이상 테스트 쿼리로 re-ranking 효과 확인
- [ ] 타입 안전성 확보
