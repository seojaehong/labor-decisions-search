# Plan Plus: 검색 로직 업그레이드

## Executive Summary

| 관점 | 내용 |
|------|------|
| **Problem** | 사유별 카드 클릭 시 0건 반환, reason_category 42,105건 전부 빈 배열, REASON_TO_TAGS 매핑 부정확 |
| **Solution** | REASON_TO_TAGS 정밀 매핑 + 0건 버그 수정 + AI 일괄 분류로 reason_category 데이터 보강 |
| **Function UX Effect** | 성희롱 카드 클릭 → 1,387건 즉시 표시, 전체 사유 분류 완료 후 정밀 검색 가능 |
| **Core Value** | 노무사/HR 실무자와 일반 근로자가 사유별로 유사 판정례를 즉시 찾을 수 있는 실용적 검색 시스템 |

| 항목 | 값 |
|------|-----|
| Feature | search-logic-upgrade |
| Created | 2026-03-19 |
| Level | Dynamic |
| Status | Plan |

---

## 1. User Intent Discovery

### 핵심 문제
홈페이지의 사유별 카드(성희롱, 횡령 등) 클릭 시 **0건 반환**. 원인은:
1. `reason_category` 컬럼이 42,105건 전부 빈 배열
2. `REASON_TO_TAGS` 우회 매핑이 너무 넓거나 부정확
3. 별도의 0건 버그 존재 (Supabase에서는 1,387건 반환 확인)

### 대상 사용자
- **1차**: 노무사/HR 실무자 — 징계 사례 검토, 양정 기준 확인, 노동위 대응 준비
- **2차**: 일반 근로자 — 부당해고 시 유사 사례 검색

### 성공 기준
1. 사유별 카드 클릭 시 관련 결과 10건 이상 표시
2. 42,000건 전체 reason_category 분류 완료 (빈 배열 비율 100% → 10% 이하)
3. 검색 응답속도 1초 이내
4. (후순위) 복합 필터로 정밀 검색 가능

---

## 2. Alternatives Explored

| 접근법 | 설명 | 선택 |
|--------|------|------|
| **A: 태그 우선 + AI 분류 후행** | 태그 매핑 정밀화로 즉시 효과 + AI 분류는 백그라운드 | - |
| B: AI 분류 우선 + UI 후행 | 근본 해결이지만 당장 개선 없음 | - |
| C: 하이브리드 (tags+전문검색 병행) | 즉시 효과이나 쿼리 복잡도 증가 | - |
| **선택: 병행 진행** | A 기반이되, 매핑 정밀화와 AI 분류를 동시 진행 | **O** |

---

## 3. YAGNI Review

### 포함 (v1)
- [x] REASON_TO_TAGS 매핑 정밀화 (10개 사유 전체)
- [x] 0건 버그 디버깅 및 수정
- [x] AI reason_category 일괄 분류 스크립트
- [x] 분류 완료 후 검색 로직 전환 (reason_category 우선 + tags fallback)

### 후순위 (v2)
- [ ] TAG_CATEGORIES 다중 필터 UI (사건유형/쟁점/산업/당사자)
- [ ] 전문검색 개선 (형태소 분석, 동의어 처리)
- [ ] 검색 결과 정렬 옵션 (관련도순, 최신순)

---

## 4. Architecture

### 수정 파일

| 파일 | 변경 내용 |
|------|---------|
| `src/lib/types.ts` | REASON_TO_TAGS 10개 사유 정밀 재매핑 |
| `src/app/search/page.tsx` | 0건 버그 수정 + 검색 로직 개선 (reason_category 우선 → tags fallback) |

### 신규 파일

| 파일 | 목적 |
|------|------|
| `scripts/classify-reasons.ts` | AI 일괄 분류 배치 스크립트 (Haiku API) |

### 데이터 플로우

```
[즉시 수정] — 매핑 정밀화 + 버그 수정
홈 카드 클릭 → /search?reason=sexual_harassment
  → REASON_TO_TAGS["sexual_harassment"] = ["성희롱"]
  → overlaps("tags", ["성희롱"]) → 1,387건 표시

[AI 분류 완료 후] — reason_category 직접 검색
홈 카드 클릭 → /search?reason=sexual_harassment
  → contains("reason_category", ["sexual_harassment"]) → 정밀 결과
  → 미분류 건은 REASON_TO_TAGS fallback
```

### REASON_TO_TAGS 재매핑 (안)

| 사유 | 현재 매핑 | 개선 매핑 |
|------|----------|----------|
| sexual_harassment | ["성희롱"] | ["성희롱"] (유지) |
| workplace_bullying | ["직장내괴롭힘"] | ["직장내괴롭힘"] (유지) |
| violence | ["징계양정","해고사유"] | ["폭언","폭행","가혹행위"] |
| absence | ["해고사유"] | ["무단결근","태만","결근"] |
| embezzlement | ["횡령","배임","착복"] | (DB 태그 확인 후 확정) |
| incompetence | ["해고사유"] | ["업무능력부족","근무성적"] |
| misconduct | ["해고사유","징계해고"] | ["비위행위","징계해고"] |
| redundancy | ["부당해고"] | ["경영상해고","정리해고","구조조정"] |
| probation | ["수습"] | ["수습"] (유지) |
| other | [] | [] (유지, AI 분류로 해결) |

> 실제 매핑은 DB 태그 분포 확인 후 확정

### AI 분류 스크립트 설계

```
입력: title + key_issue + holding_summary + tags
모델: Claude Haiku (빠르고 저렴)
출력: ReasonCategory[] (복수 분류 허용)
배치: 100건씩 조회 → 분류 → UPDATE
재시작: reason_category != '{}' 건 스킵
예상: 42,105건 × ~$0.001/건 ≈ $42 (Haiku 기준)
```

---

## 5. Brainstorming Log

| 단계 | 결정 | 근거 |
|------|------|------|
| 핵심 목표 | 4가지 전부 단계적 진행 | 사용자 요청 |
| 접근법 | A(태그 우선) 기반 병행 | 즉시 효과 + 근본 해결 동시 |
| 1차 스코프 | 매핑 정밀화 + AI 분류 | TAG_CATEGORIES UI, 전문검색은 후순위 |
| 분류 스크립트 | Node.js (TypeScript) | 프로젝트 기술스택 일관성 |
| 분류 완료 후 | reason_category 우선 + tags fallback | 정밀도 향상 |

---

## 6. Implementation Steps

### Step 1: 버그 수정 + 매핑 정밀화 (즉시)
1. 0건 버그 원인 파악 및 수정 (search/page.tsx)
2. DB 태그 분포 조회하여 REASON_TO_TAGS 정밀 재매핑
3. 카드별 검색 결과 확인 (10개 사유 전부)

### Step 2: AI 분류 스크립트 (병행)
1. scripts/classify-reasons.ts 작성
2. Haiku API 연동 + 프롬프트 설계
3. 소규모 테스트 (100건) → 분류 품질 확인
4. 전체 실행 (42,105건)

### Step 3: 검색 로직 전환
1. search/page.tsx에서 reason_category 우선 검색으로 전환
2. 미분류 건 대비 REASON_TO_TAGS fallback 유지
3. 통계 페이지 reason_stats VIEW 정상 동작 확인
