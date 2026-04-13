# BigCase(bc_) 데이터 품질 전면 검토 체크리스트 + 수정 계획

> 조사일: 2026-04-04 | 대상: nlrc_decisions 테이블 bc_ 계열 15,742건

---

## A. DB 데이터 품질

### 🔴 치명 — holding_summary 원문 미정제 (80.6%)
- [ ] **1개 이상 원문 패턴 포함**: 12,685건 (80.6%)
- [ ] **"원고는/피고는" 패턴**: 11,881건 (75.5%)
- [ ] **"이 사건" 패턴**: 10,411건 (66.1%)
- [ ] **"을 제" 증거번호**: 4,924건 (31.3%)
- [ ] **"원고와 피고" 패턴**: 1,263건 (8.0%)
- [ ] **2,000자 truncation**: 96%가 1,001~2,000자 구간, max 정확히 2,000자 → 잘림 확실
- **영향**: 사용자에게 판결문 원문이 그대로 노출, 가독성 심각 저하

### 🔴 치명 — holding_points = holding_summary 복사본 (92.1% 오염)
- [ ] **"원고/피고" 포함**: 14,497건 (92.1%)
- [ ] **"이 사건" 포함**: 11,005건 (69.9%)
- [ ] **"갑 제/을 제" 포함**: 7,019건 (44.6%)
- [ ] **NULL**: 1,057건 (6.7%)
- **문제**: holding_summary와 거의 동일한 내용, "핵심 판시사항" 역할 못함
- **수정방향**: 3~5개 bullet point 핵심 판시사항으로 재생성 또는 폐기

### 🔴 심각 — sanction_type 단일값 오류
- [ ] **15,742건 전부 `dismissal`** — 분류 무의미
- **문제**: 수집 시 기본값으로 세팅된 것으로 추정. 실제로는 해고/정직/감봉/견책 등 다양
- **수정방향**: 원문에서 실제 징계유형 재추출

### 🔴 심각 — decision_result 비정규화
- [ ] **42종 난립**: 영어(dismissed/granted/partial)와 한국어(원고패/원고승/파기환송) 혼재
- [ ] 형사판결(벌금/징역) 혼입
- [ ] 빈값 1건, "-" 1건
- **수정방향**: 6~8개 표준값으로 통합 (granted/dismissed/partial/upheld/overturned/criminal/other)

### 🟡 중간 — 분류/메타데이터 결손
- [ ] **reason_category 빈 배열 `{}`**: 1,753건 (11.1%) — is_non_labor=true와 정확히 일치
- [ ] **key_issue NULL**: 372건 (2.4%)
- [ ] **key_issue 200자 초과(비정상)**: 685건 (4.4%)
- [ ] **key_issue "원고/피고" 오염**: 918건 (5.8%)
- [ ] **holding_summary NULL**: 685건 (4.4%) — summary_short도 동시 NULL
- [ ] **title 중복**: 551개 title이 2건 이상 중복 (총 1,102건)
- [ ] **embedding NULL**: 2건

### 🟢 양호
- [x] **summary_short**: 대부분 깨끗 ("이 사건" 5건, "원고/피고" 278건 = 1.8%)
- [x] **title**: 실명/개인정보 노출 0건 (법원명+사건번호 형식)
- [x] **decision_date**: NULL 0건, 범위 1956~2026
- [x] **URL**: 전부 `https://bigcase.ai/cases/...` 형식, NULL 0건
- [x] **reason_category 분포** (빈 배열 제외 13개):
  - absence 2,534 | workplace_bullying 1,852 | incompetence 1,800
  - probation 1,555 | misconduct 1,448 | no_dismissal 856
  - embezzlement 807 | contract_expiry 713 | violence 667
  - transfer 637 | sexual_harassment 630 | redundancy 474 | worker_status 16

### 개인정보 관련
- [x] title: 실명 0건
- [ ] holding_summary 내 익명화 기호(OOO/○○○): 64건 — 양호
- [ ] holding_summary 내 "주민등록번호" 언급: 37건 (실제 번호 아닌 언급)
- [ ] holding_summary 내 "생년월일" 언급: 10건

---

## B. 프론트엔드 렌더링 (10건)

### 🔴 심각
- [ ] **B1. NewsClient XSS 위험**: `dangerouslySetInnerHTML` 사용 → ReactMarkdown으로 교체
  - 파일: `src/app/news/NewsClient.tsx`
- [ ] **B2. CasesClient 마크다운 미적용**: 판례 상세에서 plain text 렌더링
  - 파일: `src/app/cases/CasesClient.tsx`
- [ ] **B3. FeaturedDecisions summarize() 마크다운 파괴**: `**`, `##` 등을 strip
  - 파일: `src/components/FeaturedDecisions.tsx`

### 🟡 중간
- [ ] **B4. summary_short 미활용**: DB에 깨끗한 요약 있는데 holding_summary만 사용
- [ ] **B5. normalizeSnippetMarkdown 불완전**: 일부 패턴만 처리
  - 파일: `src/lib/utils/markdown.ts`
- [ ] **B6. 스키마 불일치**: 프론트 타입과 DB 컬럼명 매핑 확인 필요
- [ ] **B7. 검색결과 snippet에 원문 패턴 노출**: holding_summary 기반 snippet 생성

### 🟠 경미
- [ ] **B8. /cases 페이지 CSS 누락**: 마크다운 스타일링 미적용
- [ ] **B9. 판례 카드 텍스트 overflow**: 긴 holding_summary 처리 부재
- [ ] **B10. 접근성(a11y)**: 마크다운 렌더링 시 heading 계층 문제

---

## C. 수정 계획 (Phase별)

### Phase 1: 긴급 렌더링 수정 (1-2일)
> 데이터는 그대로, 보여주는 방식만 개선

1. **summary_short 우선 표시** — 카드/목록에서 holding_summary 대신 summary_short 사용
2. **CasesClient ReactMarkdown 적용** — remark-gfm + rehype-sanitize
3. **FeaturedDecisions summarize() 수정** — 마크다운 보존하면서 truncate
4. **NewsClient XSS 제거** — dangerouslySetInnerHTML → ReactMarkdown
5. **normalizeSnippetMarkdown 강화** — 원문 패턴("원고는", "이 사건") 치환 규칙 추가

### Phase 2: 데이터 재정제 — 핵심 (3-5일)
> AI로 holding_summary + holding_points 전면 재작성

1. **holding_summary AI 재정제**
   - 대상: 15,057건 (NULL 제외)
   - 방법: Haiku/GPT-4o-mini 배치 처리
   - 규칙: "원고/피고"→"근로자/회사", 증거번호 제거, 법률용어 순화
   - 길이: 2000자 truncation 해제, 200-800자 요약 재생성
   - 예상 비용: ~$15-25

2. **holding_points 재생성**
   - 현재 holding_summary 복사본 → 3~5개 핵심 판시사항 bullet points로 재구조화
   - 또는 폐기하고 holding_summary에 통합

3. **decision_result 정규화**
   - 42종 → 6~8개 표준값 매핑 테이블 작성
   - SQL UPDATE로 일괄 변환

4. **sanction_type 재추출**
   - 원문/title에서 실제 징계유형 추출
   - 해고/정직/감봉/견책/경고/기타

5. **reason_category 빈 배열 1,753건 처리**
   - is_non_labor=true → 검색 제외 확인
   - 필요시 AI로 재분류

6. **key_issue 보정**
   - NULL 372건: 원문에서 재추출
   - 200자 초과 685건: 50자 이내로 재생성
   - "원고/피고" 오염 918건: 치환

7. **NULL 685건 배치 재처리**
   - incompetence(385)/workplace_bullying(300)에 집중

8. **중복 551쌍(1,102건) dedup**

### Phase 3: 품질 보증 (1-2일)
> 재정제 결과 검증

1. **샘플 검증** — 카테고리별 50건씩 수동 확인
2. **원문 패턴 잔존 체크** — "원고/피고" 0건 목표
3. **검색 품질 재측정** — evaluate_search_24q.py 재실행 (239/240 유지 확인)
4. **프론트 E2E 확인** — 각 페이지에서 렌더링 정상 확인
5. **embedding 재생성** — holding_summary 변경분 embedding 업데이트

---

## 우선순위 요약

| 순위 | 항목 | 심각도 | 영향도 | 작업량 |
|------|------|--------|--------|--------|
| 1 | Phase 1: summary_short 우선 + XSS 제거 | 치명 | 즉시 개선 | 2시간 |
| 2 | Phase 2-1: holding_summary AI 재정제 | 치명 | 근본 해결 | 3일 |
| 3 | Phase 2-2: holding_points 재생성/폐기 | 치명 | 데이터 정합성 | 2일 |
| 4 | Phase 2-3: decision_result 정규화 | 심각 | 검색/필터 | 0.5일 |
| 5 | Phase 2-4: sanction_type 재추출 | 심각 | 분류 정확성 | 1일 |
| 6 | Phase 2-5~8: 보정/dedup | 중간 | 데이터 완결성 | 1일 |
| 7 | Phase 3: 검증 | - | 안정성 | 1-2일 |
