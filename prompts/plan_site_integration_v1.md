# 대작업 계획: 판정례검색 → 노란봉투법.com 통합

## 현황 분석

### 두 레포 비교
| 항목 | labor-law-guide (노란봉투법.com) | labor-decisions-search |
|------|----------------------------------|----------------------|
| Next.js | 16.1.6 | 16.1.6 |
| React | 19.2.3 | 19.2.3 |
| 라우트 수 | 17개 | 8개 |
| 디자인 시스템 | Toss 스타일 (Pretendard) | OKLch + Geist |
| SEO | 완비 (sitemap, robots, JSON-LD, OG) | 최소 |
| AI | GLM-4.7-Flash (채팅) | Anthropic Claude (비교분석) |
| Supabase | 공유 DB (yellow-envelope-law) | 동일 DB |
| 배포 | Vercel (노란봉투법.com) | Vercel (staging) |

### 현재 연결 상태
- GlassNav에서 labor-decisions-search.vercel.app로 **외부 링크**
- DB는 이미 공유 (nlrc_decisions, cases, molab_interpretations 등)
- 코드 import는 없음 (완전 분리)

---

## 통합 전략: "안착" 방식 결정

### Option A: 모노레포 병합 (코드 하나로)
- labor-law-guide에 labor-decisions-search 코드를 직접 이식
- 장점: 단일 배포, SEO 최적화, 코드 공유
- 단점: 대규모 작업, 충돌 위험, 디자인 시스템 통합 필요

### Option B: API 프록시 (프론트만 통합) ⭐ 권장
- labor-law-guide에 /search, /sanction 라우트 추가
- UI는 노란봉투법 디자인으로 새로 작성
- API는 labor-decisions-search의 로직을 lib으로 복사 또는 내부 API 호출
- 장점: 점진적 이식, 디자인 통일, SEO 유지
- 단점: 일시적 코드 중복 (나중에 정리)

### Option C: Next.js Rewrites (도메인만 통합)
- 노란봉투법.com/search → labor-decisions-search.vercel.app/search
- 장점: 가장 빠름
- 단점: 디자인 불일치, 사용자 경험 분절

### 권장: Option B (API 프록시 + UI 재작성)
이유: 사용자 경험 통일이 핵심. 검색 로직은 Supabase 직접 쿼리로 충분하고, AI 분석만 별도 API 필요.

---

## 5단계 실행 계획

### Phase 1: 기반 정비 (1일)
1. **디자인 토큰 통합**: labor-law-guide의 Toss 디자인 시스템에 검색 전용 컬러 추가
2. **공유 타입 이식**: `ReasonCategory`, `DecisionResult`, `SearchCard` 등을 labor-law-guide/src/lib/types/에 복사
3. **Supabase 쿼리 모듈 이식**: search-modes.ts 핵심 로직을 labor-law-guide에 이식
   - `runBaselineSearch`, `runMolabSearch`, `runBigcaseSearch`, `runLawgoSearch`
   - 이미 같은 Supabase 프로젝트이므로 환경변수 추가 불필요

### Phase 2: 검색 페이지 통합 (2일)
4. **`/search` 라우트 생성** (labor-law-guide)
   - 노란봉투법 디자인으로 검색 UI 재작성
   - GlassNav 수정: 외부 링크 → 내부 `/search` 링크
   - 기존 `/database` 페이지와 역할 정리 (database → 간단 탐색, search → 전문 검색)
5. **검색 결과 카드 컴포넌트**
   - 판정례(nlrc) / 법원판례(bigcase+lawgo) / 행정해석(molab) 3종 카드
   - source_provider 배지 디자인 통일
6. **검색 API 라우트** (`/api/search`)
   - search-modes.ts 로직 기반
   - baseline/candidate/compare 3모드 유지

### Phase 3: AI 비교분석기 통합 (2일)
7. **`/analyze` 라우트 생성** (구 `/sanction`)
   - "AI 징계양정" → "AI 비교분석기"로 리브랜딩
   - 채팅 인터페이스 + 유사사례 비교 + 체크리스트 생성
8. **AI API 통합**
   - 기존 GLM 채팅 (`/api/chat`) + Anthropic 비교분석 (`/api/analyze`) 공존
   - Phase 3 UX 로드맵의 "AI가 알아서 분기" 기반 마련
9. **판정례 상세 페이지** (`/decisions/[id]`)
   - 검색 결과 클릭 → 상세 보기
   - 유사 사례 사이드바

### Phase 4: 네비게이션 & UX 통합 (1일)
10. **GlassNav 재설계**
    - 메가메뉴: 가이드 | 검색 | AI분석 | 블로그 | 지원금
    - 모바일: 바텀 네비
11. **홈페이지 리디자인**
    - 3개 주요 경로 카드 (가이드 / 검색 / AI분석)
    - 최근 판정례, 인기 행정해석, 최신 블로그 위젯
12. **통합 검색 바 (글로벌)**
    - 헤더에 검색 입력 → 판정례+행정해석+블로그 동시 검색

### Phase 5: SEO & 마무리 (1일)
13. **sitemap.xml 확장**: /search, /analyze, /decisions/[id] 추가
14. **JSON-LD 추가**: 검색 결과 구조화 데이터
15. **리다이렉트 설정**: labor-decisions-search.vercel.app → 노란봉투법.com/search
16. **성능 최적화**: 검색 쿼리 캐싱, ISR 적용
17. **labor-decisions-search 레포 역할 전환**: 수집 스크립트 + 분석 로직 전용 (프론트엔드 제거)

---

## 이식 대상 파일 목록

### labor-decisions-search → labor-law-guide 이식
```
src/lib/types.ts          → src/lib/types/decisions.ts (타입)
src/lib/search/           → src/lib/search/ (검색 로직 전체)
  search-modes.ts
  types.ts
  query-parser.ts
  normalize-query.ts
src/lib/ai/               → src/lib/ai/ (AI 분석)
  prompt.ts
  retrieval.ts
  decision-bucket.ts
  stream.ts
src/lib/tags.ts           → src/lib/tags.ts
src/lib/format-holding.ts → src/lib/format-holding.ts
src/components/ui/        → 기존 컴포넌트에 통합 (badge, table 등)
```

### 새로 만들 파일 (labor-law-guide)
```
src/app/search/page.tsx          — 통합 검색 UI
src/app/search/SearchClient.tsx  — 검색 클라이언트 컴포넌트
src/app/analyze/page.tsx         — AI 비교분석기
src/app/analyze/AnalyzeClient.tsx
src/app/decisions/[id]/page.tsx  — 판정례 상세
src/app/api/search/route.ts     — 검색 API
src/app/api/analyze/route.ts    — AI 분석 API
src/components/SearchCard.tsx    — 검색 결과 카드
src/components/MolabCard.tsx     — 행정해석 카드
src/components/SearchBar.tsx     — 글로벌 검색 바
```

---

## 리스크 & 대응

| 리스크 | 대응 |
|--------|------|
| 디자인 불일치 | Phase 1에서 디자인 토큰 먼저 통합 |
| API 키 충돌 | env 분리 (GLM_API_KEY + ANTHROPIC_API_KEY) |
| 검색 성능 | Supabase 인덱스 확인, ISR 캐싱 |
| SEO 깨짐 | 리다이렉트 301, sitemap 선행 업데이트 |
| 기존 사용자 혼란 | 외부 링크 → 내부 링크 점진적 전환 |

---

## 일정 (예상)

| Phase | 내용 | 소요 |
|-------|------|------|
| 1 | 기반 정비 (타입, 쿼리 모듈) | 1일 |
| 2 | 검색 페이지 통합 | 2일 |
| 3 | AI 비교분석기 통합 | 2일 |
| 4 | 네비게이션 & UX | 1일 |
| 5 | SEO & 마무리 | 1일 |
| **합계** | | **~7일** |

---

## 통합 후 레포 역할

- **labor-law-guide**: 노란봉투법.com 프론트엔드 전체 (가이드 + 검색 + AI분석 + 블로그 + 지원금)
- **labor-decisions-search**: 데이터 수집 전용 (BigCase 크롤러, molab 태거, 분석 스크립트)
- **Supabase**: 공유 DB 유지 (변경 없음)
