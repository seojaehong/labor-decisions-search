# AI 징계양정 추천 시스템 — Design Document

> Plan: `docs/01-plan/features/ai-sanction-advisor.plan.md`
> 2026-03-18 | labor-decisions-search 확장

---

## 1. DB 스키마 변경

### 1.1 tags 컬럼 추가

```sql
-- 기존 nlrc_decisions 테이블에 tags 배열 컬럼 추가
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}';
CREATE INDEX IF NOT EXISTS idx_nlrc_tags ON nlrc_decisions USING gin(tags);
```

### 1.2 NlrcDecision 타입 확장

```typescript
// src/lib/types.ts — 기존 인터페이스에 추가
export interface NlrcDecision {
  // ... 기존 필드 유지
  tags: string[];  // NEW
}
```

### 1.3 태그 카테고리 상수

```typescript
// src/lib/tags.ts (NEW)
export const TAG_CATEGORIES = {
  사건유형: ['부당해고', '부당노동행위', '부당징계', '차별시정', '조정', '손해배상', '긴급조정', '휴업', '재해'],
  쟁점: ['해고사유', '절차위반', '징계양정', '통상임금', '퇴직금', '근로시간', '직장내괴롭힘', '비정규직', '사직', '갱신기대권', '당사자적격', '근로자성', '구제이익'],
  판정결과: ['인용', '기각', '각하', '초심유지', '초심취소', '조정성립'],
  당사자: ['근로자', '사용자', '노동조합', '공무원', '교원'],
  산업: ['제조업', '건설업', '운수업', '의료', '교육', '공공기관', '금융', 'IT', '서비스업'],
} as const;
```

---

## 2. 데이터 업로드 스크립트

### 2.1 upload_to_supabase.py

```
위치: scripts/upload_to_supabase.py
입력: 노동위판정례/*.md (42,105건)
출력: Supabase nlrc_decisions 테이블 upsert

로직:
1. md 파일 읽기 → frontmatter 파싱 (tags, caseType, decisionResult, date, department)
2. 본문 추출 (판정사항, 판정요지)
3. 기존 reason_category/sanction_type/decision_result 매핑
4. Supabase upsert (id = caseNo 또는 파일명)
5. 배치 1000건 단위, 진행률 출력
```

### 2.2 필드 매핑

| md frontmatter | DB 컬럼 | 변환 |
|----------------|---------|------|
| `tags` | `tags` | 그대로 TEXT[] |
| `caseType` | `case_type` | 그대로 |
| `decisionResult` | `decision_result` | granted/dismissed/rejected 매핑 |
| `date` | `decision_date` | DATE 변환 |
| `department` | `department` | 그대로 |
| `# 제목` | `title` | 첫 번째 # 헤딩 |
| `## 판정사항` | `holding_points` | 섹션 본문 |
| `## 판정요지` | `holding_summary` | 섹션 본문 |
| 원문 링크 | `url` | 파싱 |

---

## 3. 검색 UI 확장

### 3.1 /search 페이지 — 태그 필터 추가

기존 검색 UI에 태그 필터 칩 섹션 추가:

```
┌─────────────────────────────────────────────────┐
│ [검색어 입력]                        [검색]      │
├─────────────────────────────────────────────────┤
│ 사건유형: [부당해고] [부당징계] [차별시정] ...   │
│ 쟁  점: [징계양정] [절차위반] [해고사유] ...    │
│ 결  과: [인용] [기각] [초심유지] ...            │
│ 산  업: [제조업] [의료] [금융] ...              │
├─────────────────────────────────────────────────┤
│ 검색결과 42,105건 (선택: #부당해고 #징계양정)   │
│                                                  │
│ ┌─────────────────────────────────────────────┐ │
│ │ 2025부노OOO | 초심유지 | 2025-08-11        │ │
│ │ 통상임금 재산정 관련 차별 지급...            │ │
│ │ #부당노동행위 #불이익취급 #통상임금          │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### 3.2 Supabase 쿼리

```typescript
// 태그 필터: tags 배열에 선택된 태그가 모두 포함된 행
supabase
  .from('nlrc_decisions')
  .select('*')
  .contains('tags', selectedTags)  // @> operator
  .textSearch('search_vector', query)
  .order('decision_date', { ascending: false })
  .range(offset, offset + PAGE_SIZE - 1)
```

---

## 4. Supabase Edge Function

### 4.1 함수 구조

```
위치: supabase/functions/ai-sanction-advisor/index.ts
트리거: POST /functions/v1/ai-sanction-advisor
입력: { messages: [{role, content}] }
출력: { content, tags, cases }
```

### 4.2 2-Step 흐름

```typescript
// Step 1: 사용자 메시지에서 키워드 추출
const extractPrompt = `사용자의 상황에서 노동법 키워드를 추출하세요.
가능한 키워드: ${ALL_TAGS.join(', ')}
JSON 배열로만 응답.`;

const tags = await callGLM(extractPrompt, userMessage);
// → ["징계해고", "해고사유", "횡령"]

// Step 2: 태그로 유사 판정례 검색
const { data: cases } = await supabase
  .from('nlrc_decisions')
  .select('id, title, decision_result, holding_points, tags, url')
  .contains('tags', tags.slice(0, 3))  // 상위 3개 태그로 매칭
  .limit(10);

// Fallback: 결과 0건이면 태그 1개씩 줄여서 재검색
if (!cases?.length && tags.length > 1) {
  // overlaps 연산자로 OR 매칭
  const { data } = await supabase
    .from('nlrc_decisions')
    .select(...)
    .overlaps('tags', tags)
    .limit(10);
}

// Step 3: 종합 분석
const analysisPrompt = `당신은 노동법 전문 AI입니다.
사용자 상황과 유사 판정례를 바탕으로:
1. 예상 징계수위 (근거 판정례 인용)
2. 필수 절차 체크리스트
3. 주의사항
을 안내하세요.

유사 판정례:
${cases.map(c => `- ${c.title} [${c.decision_result}]: ${c.holding_points?.slice(0, 200)}`).join('\n')}
`;

const analysis = await callGLM(analysisPrompt, userMessage);
```

### 4.3 GLM 호출 헬퍼

```typescript
async function callGLM(systemPrompt: string, userMessage: string) {
  const resp = await fetch('https://api.z.ai/api/paas/v4/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Deno.env.get('GLM_API_KEY')}`,
    },
    body: JSON.stringify({
      model: 'GLM-4.7-Flash',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userMessage },
      ],
      max_tokens: 2048,
      temperature: 0.3,
    }),
  });
  return (await resp.json()).choices[0].message.content;
}
```

### 4.4 환경변수

```
# Supabase Edge Function secrets
GLM_API_KEY=65f63a36a7034f1f9b7ef3939acdbc49.ELytUo99zdM5o9IU
```

---

## 5. 채팅 UI

### 5.1 /chat 페이지 구조

```
src/app/chat/page.tsx (NEW)
src/components/chat/ChatMessage.tsx (NEW)
src/components/chat/TagChips.tsx (NEW)
src/components/chat/CaseCard.tsx (NEW)
src/components/chat/QuickReplies.tsx (NEW)
```

### 5.2 화면 구성

```
┌─────────────────────────────────────────────────┐
│  ⚖️ AI 징계양정 상담                            │
├─────────────────────────────────────────────────┤
│                                                  │
│  🤖 안녕하세요! 징계 관련 상황을 말씀해주시면   │
│     유사 판정례를 분석해 드립니다.               │
│                                                  │
│  [직원 지각/결근] [횡령/배임] [폭언/폭행]       │  ← Quick Replies
│  [업무태만] [사내 성희롱]                       │
│                                                  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│                                                  │
│  👤 직원이 회사 물품을 횡령했습니다.             │
│     3년차 정규직이고 금액은 500만원입니다.       │
│                                                  │
│  🤖 분석 키워드:                                │
│     [#징계해고] [#해고사유] [#횡령]              │  ← TagChips
│                                                  │
│     📋 예상 징계수위: 해고                      │
│     유사 판정례 10건 중 8건이 해고 판정          │
│                                                  │
│     ┌─ 유사 판정례 ─────────────────────┐       │
│     │ id_25001 | 기각 | 2021-09-14     │       │  ← CaseCard
│     │ 허위계정 생성 지시 → 징계해고...  │       │
│     │ #징계해고 #해고사유               │       │
│     └──────────────────────────────────┘       │
│                                                  │
│     ✅ 필수 절차:                               │
│     1. 인사위원회 개최                          │
│     2. 해당 직원 소명기회 부여                  │
│     3. 서면으로 해고 통지 (30일 전)             │
│                                                  │
├─────────────────────────────────────────────────┤
│ [상황을 설명해주세요...]              [전송 ➤]  │
└─────────────────────────────────────────────────┘
```

### 5.3 상태 관리

```typescript
// src/app/chat/page.tsx
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  tags?: string[];           // 추출된 태그 (assistant만)
  cases?: CaseCardData[];    // 유사 판정례 (assistant만)
}

interface CaseCardData {
  id: string;
  title: string;
  decision_result: string;
  holding_points: string;
  tags: string[];
  url: string;
}
```

### 5.4 API 호출 (Next.js Route → Edge Function)

```typescript
// src/app/api/chat/route.ts (NEW — 기존과 별도)
// 또는 클라이언트에서 직접 Edge Function 호출
const response = await fetch(
  `${process.env.NEXT_PUBLIC_SUPABASE_URL}/functions/v1/ai-sanction-advisor`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages }),
  }
);
```

---

## 6. 네비게이션

기존 레이아웃에 `/chat` 링크 추가:

```
[🏠 홈] [🔍 검색] [📊 통계] [💬 AI 상담]  ← NEW
```

---

## 7. Implementation Order

| 순서 | 작업 | 파일 | 의존성 |
|------|------|------|--------|
| 1 | DB 스키마 변경 (tags 컬럼) | Supabase SQL Editor | 없음 |
| 2 | 타입 확장 + 태그 상수 | `types.ts`, `tags.ts` | 없음 |
| 3 | 데이터 업로드 스크립트 | `scripts/upload_to_supabase.py` | Step 1 |
| 4 | 검색 UI 태그 필터 | `search/page.tsx` | Step 1,2 |
| 5 | Edge Function 생성 | `supabase/functions/` | Step 1,3 |
| 6 | 채팅 컴포넌트 | `components/chat/*` | Step 2 |
| 7 | 채팅 페이지 | `app/chat/page.tsx` | Step 5,6 |
| 8 | 네비게이션 업데이트 | `layout.tsx` | Step 7 |
| 9 | Vercel + Supabase 배포 | 환경변수 설정 | 전체 |

---

## 8. 환경변수 정리

| 변수 | 위치 | 값 |
|------|------|-----|
| `NEXT_PUBLIC_SUPABASE_URL` | Vercel | 기존 유지 |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Vercel | 기존 유지 |
| `GLM_API_KEY` | Supabase Edge Function secrets | `65f63a...o9IU` |

---

> Next step: `/pdca do ai-sanction-advisor`
