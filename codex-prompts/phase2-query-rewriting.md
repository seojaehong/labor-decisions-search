# Phase 2: AI Query Rewriting 파이프라인

## 목표
사용자 자연어 쿼리를 법률 검색에 최적화된 쿼리로 변환하는 AI 기반 파이프라인 구축.

## 배경
- 현재 `src/lib/search/normalize-query.ts`와 `query-parser.ts`에 rule-based 버전이 존재
- 이를 AI 기반으로 업그레이드하여 검색 정확도를 65% → 73%로 향상
- Supabase에 `search_similar_cases_hybrid` RPC가 이미 배포되어 있음

## 작업 내용

### 1. AI Query Rewriter 함수 생성
**파일:** `src/lib/search/ai-query-rewriter.ts` (신규)

```typescript
interface RewrittenQuery {
  searchQuery: string;      // 검색용 최적화 쿼리 (한국어 법률 키워드 중심)
  category: string;         // 자동 감지된 카테고리
  intent: string;           // 쿼리 의도 (severity_check, validity_check 등)
  keywords: string[];       // 핵심 법률 키워드
}

export async function rewriteQuery(userQuery: string): Promise<RewrittenQuery>
```

**구현 방법:**
- OpenAI `gpt-4o-mini` 또는 Claude `claude-haiku-4-5-20251001` 사용
- 프롬프트에 아래 변환 규칙 포함:

**변환 예시:**
| 사용자 입력 | 변환 결과 |
|---|---|
| "사장이 욕설하는데 참다가 때렸어요" | query: "폭행 비위 징계해고 양정 과다 우발적", category: "violence" |
| "3년 계약직인데 다음달 안 쓴다고 해요" | query: "기간제 갱신기대권 계약만료 부당해고", category: "contract_expiry" |
| "무단결근 3일 했다고 짤렸어요" | query: "무단결근 징계해고 양정 과다 절차", category: "absence" |
| "수습기간인데 갑자기 해고 통보" | query: "수습기간 본채용 거부 서면통지 절차 하자", category: "probation" |

**카테고리 목록** (reason_category 값):
- absence, workplace_bullying, probation, incompetence, contract_expiry
- transfer, violence, worker_status, sexual_harassment, embezzlement
- misconduct, economic_dismissal, no_dismissal, union_activity, other

**프롬프트 핵심 지침:**
1. 법률 용어로 변환 (일상어 → 법률 키워드)
2. 검색 관련 핵심 키워드 3-7개 추출
3. 카테고리 자동 감지
4. 불필요한 조사/어미 제거
5. 양정(징계 수위), 절차(서면통지 등), 사유(비위 내용) 구분

### 2. 기존 코드 통합
**파일:** `src/lib/search/search-modes.ts`

현재 `runCandidateSearch()` 함수에서:
1. `rewriteQuery(userQuery)` 호출 추가
2. 변환된 쿼리로 `searchCasesViaRpc()` 호출
3. fallback: AI 실패 시 기존 rule-based 사용

### 3. 환경변수
- `OPENAI_API_KEY`: 이미 `.env`에 존재 (embedding용)
- 추가 비용: 쿼리당 ~$0.001 (gpt-4o-mini)

## 참고 파일
- `src/lib/search/normalize-query.ts` — 기존 rule-based 정규화 (참고용)
- `src/lib/search/query-parser.ts` — 기존 시나리오 감지 (참고용)
- `src/lib/ai/retrieval.ts` — OpenAI API 호출 패턴 (embedding 생성 코드 참고)
- `src/app/api/search/route.ts` — 검색 API 엔트리포인트

## 테스트
아래 24개 평가 쿼리로 변환 결과 확인:
1. "반복 무단결근으로 해고된 사건"
2. "무단결근이 언급되지만 실제 핵심은 절차 위반인 사건"
3. "택시나 버스 기사 무단결근 징계해고"
4. "직장내괴롭힘이 실제로 성립하는지 다툼이 핵심인 사건"
5. "직장내괴롭힘 신고 후 불이익이나 보복이 문제 된 사건"
6. "괴롭힘은 인정되는데 징계 수위가 과한지 보는 사건"
7. "수습기간 중 본채용 거부가 정당한지"
8. "수습기간 중 업무능력 부족으로 해고하거나 본채용 거부한 사건"
9. "수습인데 서면통지나 절차 문제가 있는 사건"
10. "정규직 저성과나 업무능력 부족으로 해고된 사건"
11. "개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건"
12. "징계사유는 인정되지만 해고가 너무 과하다고 본 사건"
13. "정직 처분 양정이 적정한지 본 사건"
14. "감봉 처분이 과한지 본 사건"
15. "기간제 근로자의 갱신기대권이 인정되는지"
16. "계약기간 만료인데 사실상 해고처럼 다퉈진 사건"
17. "전보나 인사발령이 정당한지 다툰 사건"
18. "대기발령이나 배치전환이 징계인지 인사권 행사인지 다툼"
19. "폭행이나 욕설 같은 비위 사실 자체가 인정되는지가 핵심인 사건"
20. "폭행은 있었지만 해고까지는 과하다고 본 사건"
21. "욕설이나 직장질서 문란이 반복되어 징계해고된 사건"
22. "근로자성이 실제 핵심 쟁점인 사건"
23. "괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건"
24. "여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건"

## 완료 기준
- [ ] `ai-query-rewriter.ts` 구현
- [ ] search-modes.ts에 통합
- [ ] 24개 테스트 쿼리 변환 결과 출력 확인
- [ ] fallback 로직 (AI 실패 시 rule-based) 동작 확인
- [ ] 타입 안전성 확보
