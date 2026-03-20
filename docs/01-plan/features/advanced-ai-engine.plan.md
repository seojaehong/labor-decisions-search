# 고도화 AI 엔진 — Plan Document

> **Summary**: 4만 건 노동 판정례 기반 하이브리드 검색 + ML 승률 예측 + 설명 가능한 AI 시스템
>
> **Project**: labor-decisions-search
> **Version**: 0.1.0
> **Date**: 2026-03-20
> **Status**: Draft
> **기반**: 기존 MVP (태그 기반 검색 + GLM 채팅) 위에 고도화

---

## Executive Summary

| 관점 | 내용 |
|------|------|
| **Problem** | 태그 기반 매칭만으로는 의미적 유사도를 포착하지 못하고, 징계 결과 예측의 정량적 근거가 없으며, GLM 모델이 외부 지식을 혼입하여 환각 위험 존재 |
| **Solution** | BM25+BGE-M3 하이브리드 검색 + RF/XGBoost/CatBoost 앙상블 승률 예측 + 명시적 지식 경계 모델링으로 환각 차단 |
| **Function UX Effect** | 상황 입력 → 하이브리드 검색으로 정밀 유사 판정례 매칭 → "사측 패소 확률 82%" 수치 + SHAP 요인별 기여도 시각화 |
| **Core Value** | 정량적 승률 예측(데이터 기반) + 설명 가능성(SHAP) + 환각 제로(지식 경계) = 실무자가 신뢰할 수 있는 AI 법률 도구 |

| 항목 | 값 |
|------|-----|
| Feature | advanced-ai-engine |
| 시작일 | 2026-03-20 |
| 예상 범위 | 3개 서브시스템 (하이브리드 검색 / ML 예측 / 환각 방지) |
| 기반 프로젝트 | `C:\dev\labor-decisions-search` (Next.js 16 + Supabase) |
| 선행 조건 | MVP 완료 (ai-sanction-advisor + search-logic-upgrade) |

---

## 1. Overview

### 1.1 Purpose

현재 MVP의 태그 기반 검색을 **하이브리드 검색(BM25+벡터)**으로 업그레이드하고, **ML 앙상블 모델로 승률 예측** 기능을 추가하며, **명시적 지식 경계 모델링으로 환각을 원천 차단**하는 고도화 AI 엔진 구축.

### 1.2 Background

- 42,105건의 노동위 판정례가 태그 분류 완료 → 텍스트 + 메타데이터 풍부
- 현재 태그 매칭(@> 연산)은 정확한 키워드 일치만 가능, 의미적 유사도 불가
- 실무자는 "이 상황에서 이길 확률"이라는 정량적 답변을 원함
- GLM-4.7-Flash는 외부 지식 혼입 가능성 존재 → 법률 도구에서 치명적

### 1.3 Related Documents

- Plan: `docs/01-plan/features/ai-sanction-advisor.plan.md` (MVP)
- Design: `docs/02-design/features/ai-sanction-advisor.design.md` (MVP)
- Plan: `docs/01-plan/features/search-logic-upgrade.plan.md` (검색 정밀화)

---

## 2. Scope

### 2.1 In Scope

- [x] BM25 + BGE-M3 하이브리드 검색 체계 구축
- [x] 42k 판정례 벡터 임베딩 생성 및 저장
- [x] RF + XGBoost + CatBoost 소프트 보팅 앙상블 승률 예측
- [x] 피처 엔지니어링 (텍스트 임베딩 + 정량적 메타데이터)
- [x] SHAP 기반 설명 가능성 (요인별 기여도)
- [x] 명시적 지식 경계 모델링 (외부 지식 유입 차단)
- [x] 의미 단위 청킹 (Semantic Chunking)
- [x] 프롬프트 수준 지식 증류 (SLM 추론 강화)
- [x] 승률 예측 대시보드 UI

### 2.2 Out of Scope

- Fine-tuning / LoRA (모델 학습 비용 과대)
- 실시간 판정례 자동 수집 (웹 크롤링)
- 사용자 인증 및 이력 저장
- 모바일 앱
- 다국어 지원

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-01 | BM25 키워드 검색 + BGE-M3 벡터 검색 하이브리드 결합 | High | Pending |
| FR-02 | 42k 판정례 BGE-M3 임베딩 생성 및 pgvector 저장 | High | Pending |
| FR-03 | ML 앙상블 모델 학습 (RF/XGBoost/CatBoost) | High | Pending |
| FR-04 | 피처 추출: 텍스트 임베딩 + 정량 변수 (근속연수, 기업규모, 징계종류, 비위횟수) | High | Pending |
| FR-05 | SHAP Value 기반 요인별 영향도 계산 및 시각화 | Medium | Pending |
| FR-06 | 명시적 지식 경계: 4만 건 판정례 풀 내에서만 근거 제시 | High | Pending |
| FR-07 | 의미 단위 청킹으로 판정례 분할 | Medium | Pending |
| FR-08 | 프롬프트 지식 증류 (대형 모델 CoT → SLM 프롬프트 주입) | Medium | Pending |
| FR-09 | 승률 예측 결과 대시보드 (확률 + SHAP 차트) | Medium | Pending |

### 3.2 Non-Functional Requirements

| 카테고리 | 기준 | 측정 방법 |
|----------|------|----------|
| 성능 | 검색 응답 1초 이내, 승률 예측 3초 이내 | Latency 측정 |
| 정확도 | 승률 예측 85%+ (교차검증) | k-fold Cross-validation |
| 환각률 | 외부 지식 인용 0% | 외부 지식 유입 테스트 |
| 확장성 | 10만 건까지 스케일 | 부하 테스트 |

---

## 4. Success Criteria

### 4.1 Definition of Done

- [ ] 하이브리드 검색이 기존 태그 매칭 대비 Recall@10 20%+ 향상
- [ ] 승률 예측 정확도 85%+ (교차검증)
- [ ] SHAP 설명이 상위 5개 요인 제시
- [ ] 외부 지식 유입 테스트 통과 (0% 환각률)
- [ ] 5개 시나리오 E2E 테스트 통과

### 4.2 Quality Criteria

- [ ] 검색 응답 p95 < 1초
- [ ] 모델 학습 재현 가능 (시드 고정, 파이프라인 스크립트화)
- [ ] 빌드 성공 + 린트 에러 0

---

## 5. Risks and Mitigation

| 리스크 | 영향 | 가능성 | 대응 |
|--------|------|--------|------|
| BGE-M3 임베딩 비용 (42k건) | Medium | Low | 배치 처리, 로컬 GPU 또는 API 비용 $50 이내 |
| pgvector Supabase 성능 | High | Medium | 인덱스 튜닝 (IVFFlat/HNSW), 필요시 Qdrant 대안 |
| ML 모델 학습 데이터 편향 | High | Medium | 인용/기각 비율 확인, 층화 샘플링, 교차검증 |
| 정량 피처 부족 (근속연수 등 텍스트에서 추출 필요) | Medium | High | NER/정규식 기반 추출 스크립트, 미추출 건은 결측치 처리 |
| SLM 프롬프트 증류 효과 불확실 | Medium | Medium | A/B 테스트, 증류 전/후 응답 품질 비교 |

---

## 6. Architecture Considerations

### 6.1 Project Level

| Level | 선택 |
|-------|:----:|
| **Starter** | |
| **Dynamic** | ✅ |
| **Enterprise** | |

### 6.2 Key Architectural Decisions

| 결정 | 옵션 | 선택 | 근거 |
|------|------|------|------|
| 검색 엔진 | 태그매칭 / BM25+벡터 / Elasticsearch | BM25+BGE-M3 | 한국어 다국어 지원, 8192 토큰 장문 처리, 법률 용어 매칭 |
| 벡터 DB | pgvector / Qdrant / Pinecone | pgvector | Supabase 생태계 통합, 추가 인프라 불필요 |
| ML 프레임워크 | scikit-learn+XGBoost / PyTorch | scikit-learn+XGBoost+CatBoost | 표형식 데이터에 최적, 학습 빠름 |
| 임베딩 모델 | BGE-M3 / multilingual-e5 / KoSimCSE | BGE-M3 | 다중 세분성, 한국어 성능, 8192 토큰 |
| 설명가능성 | SHAP / LIME / 자체 구현 | SHAP | 글로벌+로컬 설명, 앙상블 호환, 업계 표준 |
| 승률 예측 서빙 | Python API / Edge Function / Supabase RPC | Python API (FastAPI) | ML 모델 서빙에 Python 필수, scikit-learn/XGBoost 런타임 |

### 6.3 시스템 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface Layer                        │
│  Next.js 16 App Router                                         │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ /search  │  │ /sanction    │  │ /predict (NEW)           │ │
│  │ 하이브리드│  │ AI 채팅      │  │ 승률 예측 대시보드       │ │
│  │ 검색     │  │ (기존 강화)  │  │ + SHAP 차트             │ │
│  └──────────┘  └──────────────┘  └──────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                     Application Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │  Hybrid Search  │  │  Knowledge      │  │  Prediction   │  │
│  │  Service        │  │  Boundary       │  │  Service      │  │
│  │  (BM25+BGE-M3) │  │  Guard          │  │  (FastAPI)    │  │
│  └─────────────────┘  └─────────────────┘  └───────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                      Data Layer                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │  Semantic       │  │  Feature        │  │  ML Models    │  │
│  │  Chunking       │  │  Engineering    │  │  (pkl files)  │  │
│  │  Pipeline       │  │  Pipeline       │  │  RF/XGB/Cat   │  │
│  └─────────────────┘  └─────────────────┘  └───────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                    Storage Layer                                │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │  Supabase       │  │  pgvector       │                     │
│  │  nlrc_decisions │  │  embeddings     │                     │
│  │  42,105 rows    │  │  42,105 vectors │                     │
│  └─────────────────┘  └─────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. 해외 사례 참조

| 연구 대상 | 알고리즘 | 정확도 | 출처 |
|----------|---------|--------|------|
| 미국 대법원 판결 예측 | 랜덤 포레스트 | **70.2%** | Katz et al. (2023) |
| 영국 금융 분쟁 예측 | ML 앙상블 | **86.6%** | CaseCrunch Inc. |
| 건설 분쟁 예측 | 랜덤 포레스트 | **95%** | Ashworth et al. |
| 중국 노동 분쟁 (LDMLSV) | RF+ExtraTree+CatBoost Soft Voting | **90%** | Chen et al. |
| 인도 법률 청원 랭킹 | RF+XGBoost+텍스트 임베딩 | **99%+** | Kumar et al. |

---

## 8. Implementation Steps (High-Level)

### Phase A: 데이터 파이프라인 (선행)
1. 의미 단위 청킹 스크립트 (42k 판정례 → 청크)
2. BGE-M3 임베딩 생성 (배치)
3. pgvector 테이블 생성 + 임베딩 저장
4. 피처 엔지니어링 (텍스트+정량 피처 추출)

### Phase B: 검색 엔진 업그레이드
5. BM25 인덱스 구축 (tsvector 강화 또는 별도)
6. 하이브리드 검색 서비스 (BM25 스코어 + 벡터 유사도 결합)
7. Reranking 로직 (메타데이터 기반 재순위화)
8. /search UI 하이브리드 검색 전환

### Phase C: ML 승률 예측
9. 학습 데이터셋 구성 (인용/기각 라벨 + 피처)
10. 모델 학습 (RF + XGBoost + CatBoost)
11. 소프트 보팅 앙상블 + 교차검증
12. SHAP Value 계산 파이프라인
13. FastAPI 서빙 엔드포인트

### Phase D: UI + 통합
14. /predict 페이지 (승률 대시보드 + SHAP 차트)
15. 지식 경계 가드 (프롬프트 + 검증 레이어)
16. 프롬프트 지식 증류 적용
17. E2E 테스트 + 배포

---

## 9. Next Steps

1. [ ] Design 문서 작성 (`advanced-ai-engine.design.md`)
2. [ ] MVP 완료 확인 (search-logic-upgrade Do 완료)
3. [ ] Phase A 데이터 파이프라인부터 시작

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-03-20 | Initial draft (PR 기반) | Claude |
