# AI 징계양정 추천 시스템 — Plan Document

> Plan Plus | 2026-03-18 | labor-decisions-search 확장

---

## Executive Summary

| 관점 | 내용 |
|------|------|
| **Problem** | 노무사/HR 담당자가 징계 사안 발생 시 유사 판정례를 일일이 검색해야 하며, 적정 징계수위·절차를 판단하기 어려움 |
| **Solution** | 42k 노동위 판정례 태그 기반 검색 + AI 채팅으로 유사 사례 매칭 및 징계양정 추천 |
| **Function UX Effect** | 상황 입력 → 태그 칩 시각화 → 유사 판정례 카드 → 징계수위/절차 체크리스트 자동 생성 |
| **Core Value** | 설명 가능한 AI (태그 기반 근거 제시) + 실무 도구 (인터랙티브 체크리스트) |

| 항목 | 값 |
|------|-----|
| Feature | AI 징계양정 추천 시스템 |
| 시작일 | 2026-03-18 |
| 예상 범위 | DB 스키마 확장 + 데이터 업로드 + 검색 UI + Edge Function + 채팅 UI |
| 기반 프로젝트 | `C:\dev\labor-decisions-search` (Next.js 16 + Supabase) |

---

## 1. User Intent Discovery

### 핵심 문제
- 42k 노동위 판정례에 태그 분류 완료 → 이를 활용한 검색 + AI 징계양정 추천 서비스 구축

### 대상 사용자
- 노무사, HR 담당자, 사업주 (징계 절차 수행 시)

### 성공 기준
- 상황 입력 시 관련 판정례 5~10건 정확 매칭
- 징계수위 추천 + 필수 절차 체크리스트 제공
- 응답 시간 5초 이내

---

## 2. Alternatives Explored

| 접근법 | 선택 | 이유 |
|--------|------|------|
| **A: 태그 기반 매칭** | ✅ 선택 | 42k 태그 즉시 활용, 설명 가능한 근거 제시, MVP 최적 |
| B: 임베딩 시맨틱 검색 | ❌ | pgvector + 42k 임베딩 비용, 오버엔지니어링 |
| C: 하이브리드 | ❌ 향후 | MVP 이후 확장 옵션 |

---

## 3. YAGNI Review

### MVP 포함
- [x] 42k 판정례 Supabase 업로드 (tags[] 컬럼 포함)
- [x] 태그 기반 필터 검색 UI (사건유형/쟁점/결과/산업)
- [x] AI 채팅 — 징계양정 추천 (Supabase Edge Function + GLM-4.7-Flash)
- [x] Quick Reply 예시 버튼
- [x] 추출 태그 칩 시각화
- [x] 유사 판정례 카드 UI (사건번호-판정결과-핵심요지)

### MVP 제외 (Out of Scope)
- [ ] 통계 대시보드 (인용/기각 비율, 연도별 추이)
- [ ] 피드백 루프 (도움됨/안됨 버튼)
- [ ] 인터랙티브 절차 체크리스트 (체크박스 UI)
- [ ] 사용자 인증/저장 기능
- [ ] 임베딩 시맨틱 검색

---

## 4. Architecture

### 4.1 시스템 구조

```
┌──────────────────────────────────────────────────┐
│  Next.js 16 App Router                           │
├──────────┬──────────────┬────────────────────────┤
│ /search  │ /decisions/  │ /chat (NEW)            │
│ 태그필터 │ [id] 상세    │ AI 징계양정 채팅       │
│ +텍스트  │  (기존)      │                        │
├──────────┴──────────────┴────────────────────────┤
│  /api/chat → Supabase Edge Function 호출         │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────┴───────────────────────────┐
│  Supabase                                         │
│  ┌───────────────────┐  ┌──────────────────────┐ │
│  │ nlrc_decisions     │  │ Edge Function        │ │
│  │ + tags TEXT[]      │  │ ai-sanction-advisor  │ │
│  │ + 42,105 rows      │  │                      │ │
│  │ + GIN index(tags)  │  │ Step 1: GLM 키워드   │ │
│  │ + tsvector search  │  │ Step 2: DB 태그매칭  │ │
│  └───────────────────┘  │ Step 3: GLM 종합분석  │ │
│                          └──────────────────────┘ │
│                                    ↓              │
│                          GLM-4.7-Flash            │
│                          (api.z.ai)               │
└───────────────────────────────────────────────────┘
```

### 4.2 DB 스키마 변경

기존 `nlrc_decisions` 테이블에 `tags` 컬럼 추가:

```sql
ALTER TABLE nlrc_decisions ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}';
CREATE INDEX IF NOT EXISTS idx_nlrc_tags ON nlrc_decisions USING gin(tags);
```

### 4.3 데이터 파이프라인

```
42k md files (태그 분류 완료)
    ↓ Python upload script
Supabase nlrc_decisions
    - id: "id_1" ~ "id_414099"
    - tags: ["부당해고", "징계양정", "절차위반", ...]
    - title, holding_points, holding_summary, url, ...
```

### 4.4 AI 채팅 흐름 (2-step GLM)

```
사용자: "직원이 회사 물품을 횡령했습니다. 3년차 정규직입니다."
    ↓
[Step 1] GLM → 키워드 추출: ["징계해고", "해고사유", "횡령", "비위행위"]
    ↓
[Step 2] Supabase → tags @> ARRAY['징계해고','해고사유'] → 유사 판정례 10건
    ↓
[Step 3] GLM → 유사 판정례 + 사용자 상황 종합 분석
    ↓
응답:
  - 추출 태그 칩: #징계해고 #해고사유 #횡령
  - 예상 징계수위: 해고 (유사 사례 8/10건 해고, 2건 정직)
  - 필수 절차: ① 인사위원회 개최 ② 소명기회 부여 ③ 서면통지
  - 근거 판정례 카드 3건
```

---

## 5. Implementation Steps

### Step 1: DB 스키마 확장 + 데이터 업로드
- `nlrc_decisions` 테이블에 `tags[]` 컬럼 추가
- 42k md 파일 → Supabase 업로드 Python 스크립트
- 기존 데이터와 병합 (이미 일부 올라가 있을 수 있음)

### Step 2: 태그 기반 검색 UI 개선
- `/search` 페이지에 태그 필터 UI 추가
- 사건유형/쟁점/판정결과/산업 카테고리별 필터 칩
- 기존 텍스트 검색과 태그 필터 결합

### Step 3: Supabase Edge Function 생성
- `ai-sanction-advisor` Edge Function
- GLM-4.7-Flash API 호출 (api.z.ai)
- 2-step 흐름: 키워드 추출 → DB 매칭 → 종합 분석
- Fallback: 매칭 0건 시 일반 노동법 원칙 답변

### Step 4: 채팅 UI 구현
- `/chat` 페이지 (Next.js App Router)
- Quick Reply 예시 버튼 (직원 지각, 횡령, 폭언 등)
- 추출 태그 칩 시각화
- 유사 판정례 카드형 UI (인라인)
- 절차 체크리스트 텍스트 출력

### Step 5: 통합 테스트 + 배포
- E2E 시나리오 테스트 (횡령, 폭언, 무단결근 등 5개 시나리오)
- Vercel 배포 + Supabase 환경변수 설정

---

## 6. Brainstorming Log

| 결정 | 선택 | 이유 |
|------|------|------|
| 프로젝트 | 기존 labor-decisions-search 확장 | Supabase 인스턴스 재활용, 기존 검색/상세 페이지 연계 |
| AI 입력 | 채팅 형식 | 법률 상담의 심리적 접근성, 노란봉투법 사이트와 UX 일관성 |
| AI 백엔드 | Supabase Edge Function + GLM | API 키 서버사이드 보호, Supabase 생태계 통합 |
| 매칭 방식 | 태그 기반 | 42k 태그 즉시 활용, 설명 가능한 근거 |
| MVP 범위 | 업로드 + 검색 + AI 채팅 | 통계 대시보드/피드백 루프는 후속 |

### PM/UX 전문가 피드백 반영
- 태그 칩 시각화 → Step 4에 반영
- 판정례 카드 UI → Step 4에 반영
- Quick Reply 버튼 → Step 4에 반영
- Fallback 전략 → Step 3에 반영
- 피드백 루프/인터랙티브 체크리스트 → Out of Scope (향후)

---

## 7. Risk & Mitigation

| 리스크 | 대응 |
|--------|------|
| GLM-4.7-Flash 잔액 부족 | api.z.ai 기준 현재 사용 가능 확인. 충전 필요 시 대체 모델 목록 확보 |
| 태그 매칭 0건 | Fallback: 태그 수를 줄여 재검색 → 그래도 0건이면 일반 원칙 답변 |
| Supabase Edge Function 콜드 스타트 | 첫 호출 느림 가능 → UI에 로딩 애니메이션 |
| 태그 품질 | 검증 에이전트로 샘플 확인 완료. 오태깅률 ~20% (의료, 근로시간) → 규칙 보강 완료 |

---

> Next step: `/pdca design ai-sanction-advisor`
