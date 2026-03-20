# 고도화 AI 엔진 — Design Document

> **Summary**: BM25+BGE-M3 하이브리드 검색 + ML 앙상블 승률 예측 + SHAP 설명 + 환각 차단
>
> **Project**: labor-decisions-search
> **Version**: 0.1.0
> **Date**: 2026-03-20
> **Status**: Draft
> **Planning Doc**: [advanced-ai-engine.plan.md](../01-plan/features/advanced-ai-engine.plan.md)

---

## 1. Overview

### 1.1 Design Goals

1. 태그 매칭을 넘어 **의미적 유사도**를 포착하는 하이브리드 검색
2. **정량적 승률 예측**으로 실무자에게 데이터 기반 의사결정 근거 제공
3. **SHAP 기반 설명**으로 "왜 이 확률인가"를 투명하게 제시
4. **외부 지식 유입 원천 차단**으로 법률 도구 신뢰성 확보

### 1.2 Design Principles

- **Knowledge Boundary First**: 모든 응답은 42k 판정례 풀 내에서만
- **Hybrid over Single**: 단일 검색 방식 대신 BM25+벡터 상호 보완
- **Explainability by Default**: 예측 결과에는 반드시 SHAP 설명 동반
- **Incremental Enhancement**: 기존 MVP 코드 위에 점진적 확장 (파괴적 변경 최소화)

---

## 2. Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Next.js 16 Frontend                        │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ /search  │  │ /sanction    │  │ /predict (NEW)           │ │
│  │ Hybrid   │  │ AI Chat      │  │ Win Rate Dashboard       │ │
│  │ Search   │  │ + KB Guard   │  │ + SHAP Chart             │ │
│  └────┬─────┘  └──────┬───────┘  └────────────┬─────────────┘ │
│       │               │                        │               │
│  ┌────┴───────────────┴────────────────────────┴─────────────┐ │
│  │                  /api/ Route Handlers                      │ │
│  │  /api/search (hybrid)  /api/chat  /api/predict (NEW)      │ │
│  └────┬───────────────────┬──────────────────┬───────────────┘ │
├───────┼───────────────────┼──────────────────┼─────────────────┤
│       │                   │                  │                 │
│  ┌────▼─────────────┐ ┌───▼──────────┐  ┌───▼──────────────┐ │
│  │  Supabase        │ │ Edge Function│  │ FastAPI          │ │
│  │  ┌────────────┐  │ │ ai-sanction  │  │ (Python ML)      │ │
│  │  │nlrc_decisions│ │ │ -advisor     │  │ ┌──────────────┐ │ │
│  │  │42,105 rows │  │ │ + KB Guard   │  │ │ RF+XGB+Cat   │ │ │
│  │  │+ tags[]    │  │ └──────────────┘  │ │ Ensemble     │ │ │
│  │  │+ tsvector  │  │                   │ │ + SHAP       │ │ │
│  │  └────────────┘  │                   │ └──────────────┘ │ │
│  │  ┌────────────┐  │                   │ ┌──────────────┐ │ │
│  │  │embeddings  │  │                   │ │ BGE-M3       │ │ │
│  │  │(pgvector)  │  │                   │ │ Embedding    │ │ │
│  │  │42,105 vecs │  │                   │ │ Service      │ │ │
│  │  └────────────┘  │                   │ └──────────────┘ │ │
│  └──────────────────┘                   └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

#### 하이브리드 검색 플로우

```
사용자 쿼리 "회사 물품 횡령 3년차"
    │
    ├─→ [BM25] tsvector 검색 → 정확한 용어 매칭 (score_bm25)
    │
    ├─→ [BGE-M3] 쿼리 임베딩 → pgvector cosine similarity (score_vec)
    │
    └─→ [Hybrid Merge]
         score = α * score_bm25 + (1-α) * score_vec  (α=0.4 초기값)
         │
         └─→ [Rerank] 메타데이터 부스트
              - decision_result 매칭 시 +0.1
              - 동일 산업분류 시 +0.05
              │
              └─→ Top-K 결과 반환
```

#### 승률 예측 플로우

```
사용자 입력 (상황 설명)
    │
    ├─→ [Feature Extraction]
    │    ├─ 텍스트 → BGE-M3 임베딩 (1024d)
    │    ├─ NER/정규식 → 정량 피처 추출
    │    │   - 근속연수, 기업규모, 징계종류, 비위횟수
    │    └─ 메타데이터 → 원핫 인코딩
    │
    ├─→ [ML Ensemble] (FastAPI)
    │    ├─ RandomForest.predict_proba(X)
    │    ├─ XGBClassifier.predict_proba(X)
    │    └─ CatBoostClassifier.predict_proba(X)
    │         │
    │         └─→ Soft Voting: mean(probabilities)
    │              → "사측 패소 확률: 82%"
    │
    └─→ [SHAP Explanation]
         ├─ TreeExplainer(ensemble)
         ├─ shap_values = explainer(X)
         └─→ Top-5 요인 + 기여도
              "소명기회 미부여: -15%"
              "3회 이상 비위: +20%"
```

### 2.3 Dependencies

| 컴포넌트 | 의존 대상 | 목적 |
|----------|----------|------|
| Hybrid Search Service | Supabase (nlrc_decisions + embeddings) | BM25 + 벡터 검색 |
| FastAPI Prediction | ML 모델 파일 (pkl), BGE-M3 모델 | 승률 예측 + 임베딩 |
| /predict UI | FastAPI, Recharts | 대시보드 시각화 |
| KB Guard | 42k 판정례 풀 | 지식 경계 검증 |

---

## 3. Data Model

### 3.1 embeddings 테이블 (NEW)

```sql
-- pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- 임베딩 테이블
CREATE TABLE nlrc_embeddings (
  id TEXT PRIMARY KEY REFERENCES nlrc_decisions(id),
  embedding vector(1024),         -- BGE-M3 output dimension
  chunk_index INTEGER DEFAULT 0,  -- 청크 인덱스 (의미 단위)
  chunk_text TEXT,                 -- 원본 청크 텍스트
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW 인덱스 (cosine 유사도)
CREATE INDEX idx_nlrc_embeddings_hnsw
  ON nlrc_embeddings
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

### 3.2 prediction_features 테이블 (NEW)

```sql
CREATE TABLE prediction_features (
  id TEXT PRIMARY KEY REFERENCES nlrc_decisions(id),
  -- 정량 피처
  tenure_years FLOAT,           -- 근속연수
  company_size TEXT,             -- 기업규모 (small/medium/large)
  sanction_type TEXT,            -- 징계종류 (해고/정직/감봉/견책/강등)
  prior_violations INTEGER,     -- 과거 비위 횟수
  due_process_given BOOLEAN,    -- 소명기회 부여 여부
  -- 라벨
  outcome TEXT,                  -- granted(인용)/dismissed(기각)
  -- 메타
  feature_vector JSONB,          -- 전체 피처 벡터 (JSON)
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.3 NlrcDecision 타입 확장

```typescript
// src/lib/types.ts — 추가
export interface NlrcEmbedding {
  id: string;
  embedding: number[];
  chunk_index: number;
  chunk_text: string;
}

export interface PredictionResult {
  win_probability: number;       // 0.0 ~ 1.0
  model_scores: {
    random_forest: number;
    xgboost: number;
    catboost: number;
  };
  shap_factors: ShapFactor[];
  similar_cases: string[];       // 참조된 판정례 ID 목록
}

export interface ShapFactor {
  feature_name: string;          // e.g. "소명기회 미부여"
  display_name: string;          // e.g. "소명기회 미부여"
  impact: number;                // e.g. -0.15 (15% 감소)
  direction: 'positive' | 'negative';
}
```

---

## 4. API Specification

### 4.1 Endpoint List

| Method | Path | 설명 | 서버 |
|--------|------|------|------|
| GET | /api/search | 하이브리드 검색 (기존 확장) | Next.js |
| POST | /api/predict | 승률 예측 요청 | Next.js → FastAPI |
| POST | /ml/predict | ML 예측 실행 | FastAPI |
| POST | /ml/embed | 텍스트 임베딩 생성 | FastAPI |
| GET | /ml/health | ML 서버 상태 | FastAPI |

### 4.2 하이브리드 검색 API

#### `GET /api/search` (확장)

기존 태그 검색에 하이브리드 모드 추가.

**Query Parameters:**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `q` | string | 검색어 |
| `tags` | string[] | 태그 필터 (기존 유지) |
| `mode` | `tag` \| `hybrid` | 검색 모드 (기본: `tag`, 하이브리드 사용 시 `hybrid`) |
| `alpha` | number | BM25 가중치 (0.0~1.0, 기본: 0.4) |
| `page` | number | 페이지 |

**Response (hybrid mode):**
```json
{
  "results": [
    {
      "id": "id_25001",
      "title": "...",
      "score": 0.87,
      "score_bm25": 0.92,
      "score_vector": 0.83,
      "tags": ["징계해고", "횡령"],
      "decision_result": "기각",
      "holding_summary": "..."
    }
  ],
  "total": 1387,
  "mode": "hybrid"
}
```

### 4.3 승률 예측 API

#### `POST /api/predict`

**Request:**
```json
{
  "situation": "직원이 회사 물품을 횡령했습니다. 3년차 정규직이고 금액은 500만원입니다.",
  "metadata": {
    "tenure_years": 3,
    "company_size": "medium",
    "sanction_type": "해고",
    "prior_violations": 0
  }
}
```

**Response:**
```json
{
  "win_probability": 0.82,
  "label": "사측 패소 확률 82%",
  "model_scores": {
    "random_forest": 0.79,
    "xgboost": 0.84,
    "catboost": 0.83
  },
  "shap_factors": [
    { "feature_name": "prior_violations", "display_name": "과거 비위 이력 없음", "impact": -0.12, "direction": "negative" },
    { "feature_name": "due_process", "display_name": "소명기회 부여 여부 불명", "impact": -0.15, "direction": "negative" },
    { "feature_name": "sanction_severity", "display_name": "해고 (최중징계)", "impact": 0.08, "direction": "positive" },
    { "feature_name": "tenure", "display_name": "근속 3년", "impact": -0.05, "direction": "negative" },
    { "feature_name": "amount", "display_name": "횡령 금액 500만원", "impact": 0.04, "direction": "positive" }
  ],
  "similar_cases": ["id_25001", "id_31042", "id_8823"],
  "confidence": "high"
}
```

### 4.4 FastAPI ML 서버

#### `POST /ml/predict`

```python
# ml-server/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import shap

app = FastAPI()

# 모델 로드 (서버 시작 시 1회)
rf_model = joblib.load("models/rf_model.pkl")
xgb_model = joblib.load("models/xgb_model.pkl")
cat_model = joblib.load("models/cat_model.pkl")
explainer = shap.TreeExplainer(rf_model)  # 대표 모델

class PredictRequest(BaseModel):
    features: list[float]        # 피처 벡터
    feature_names: list[str]     # 피처명 목록

@app.post("/ml/predict")
def predict(req: PredictRequest):
    X = np.array([req.features])

    # Soft Voting
    probs = np.mean([
        rf_model.predict_proba(X),
        xgb_model.predict_proba(X),
        cat_model.predict_proba(X),
    ], axis=0)

    # SHAP
    shap_values = explainer.shap_values(X)

    # Top-5 요인
    top_indices = np.argsort(np.abs(shap_values[0]))[-5:][::-1]
    factors = [
        {
            "feature_name": req.feature_names[i],
            "impact": float(shap_values[0][i]),
            "direction": "positive" if shap_values[0][i] > 0 else "negative"
        }
        for i in top_indices
    ]

    return {
        "win_probability": float(probs[0][1]),  # 인용(근로자 승) 확률
        "model_scores": {
            "random_forest": float(rf_model.predict_proba(X)[0][1]),
            "xgboost": float(xgb_model.predict_proba(X)[0][1]),
            "catboost": float(cat_model.predict_proba(X)[0][1]),
        },
        "shap_factors": factors,
    }
```

---

## 5. UI/UX Design

### 5.1 /predict 페이지 — 승률 예측 대시보드

```
┌─────────────────────────────────────────────────────────────┐
│  ⚖️ AI 승률 예측                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📝 상황 입력                                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 직원이 회사 물품을 횡령했습니다.                       │  │
│  │ 3년차 정규직이고 금액은 500만원입니다.                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  📊 추가 정보 (정확도 향상)                                  │
│  근속연수: [3  ]  기업규모: [중소기업 ▼]                     │
│  징계종류: [해고 ▼]  과거비위: [0  ]                         │
│                                           [예측 실행 ▶]     │
│                                                              │
│  ═══════════════════════════════════════════════════════════ │
│                                                              │
│  🎯 예측 결과                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         사측 패소 확률                               │    │
│  │                                                      │    │
│  │              ██████████████████░░░░  82%             │    │
│  │                                                      │    │
│  │  모델별:  RF 79%  |  XGBoost 84%  |  CatBoost 83%  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  📈 주요 영향 요인 (SHAP)                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  소명기회 부여 불명    ◀████████████████  -15%       │    │
│  │  과거 비위 이력 없음   ◀██████████████    -12%       │    │
│  │  해고 (최중징계)              ██████████▶  +8%       │    │
│  │  근속 3년              ◀██████            -5%       │    │
│  │  횡령 금액 500만원            ████████▶    +4%       │    │
│  └─────────────────────────────────────────────────────┘    │
│  ⚠️ "소명기회 미부여가 사측 승률을 15% 하락시킵니다"         │
│                                                              │
│  📋 유사 판정례                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ id_25001 | 기각 | 횡령 500만원 사안, 해고 적정       │    │
│  │ id_31042 | 인용 | 소명기회 미부여로 절차 위반        │    │
│  │ id_8823  | 기각 | 횡령 1000만원, 해고 적정           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 /search 페이지 — 하이브리드 검색 토글

기존 검색 UI에 모드 전환 추가:

```
┌─────────────────────────────────────────────────┐
│ [검색어 입력]                        [검색]      │
│ 검색 모드: (●) 태그 매칭  ( ) 하이브리드 검색   │
│ ── 하이브리드 옵션 (접힘) ──────────────────── │
│   BM25 가중치: ════●════  0.4                   │
├─────────────────────────────────────────────────┤
│ 태그 필터: [부당해고] [징계양정] [횡령] ...      │
├─────────────────────────────────────────────────┤
│ 검색결과 1,387건  유사도순 ▼                     │
│ ┌─────────────────────────────────────────────┐ │
│ │ id_25001 | 기각 | score: 0.87              │ │
│ │ BM25: 0.92 | Vector: 0.83                  │ │
│ │ 횡령 관련 징계해고 사안...                   │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### 5.3 Component List

| 컴포넌트 | 위치 | 역할 |
|----------|------|------|
| `PredictPage` | `src/app/predict/page.tsx` | 승률 예측 페이지 |
| `PredictForm` | `src/components/predict/PredictForm.tsx` | 상황 입력 + 메타데이터 폼 |
| `PredictResult` | `src/components/predict/PredictResult.tsx` | 결과 표시 (확률 바 + 모델별) |
| `ShapChart` | `src/components/predict/ShapChart.tsx` | SHAP 요인 기여도 차트 (Recharts) |
| `SearchModeToggle` | `src/components/search/SearchModeToggle.tsx` | 태그/하이브리드 전환 |
| `ScoreBreakdown` | `src/components/search/ScoreBreakdown.tsx` | BM25/Vector 점수 표시 |

---

## 6. Knowledge Boundary Guard

### 6.1 설계

외부 지식 유입을 차단하는 3단계 가드:

```
[Guard Layer 1] 시스템 프롬프트 제약
  "당신은 오직 제공된 42,105건의 노동위 판정례만을 근거로 답변합니다.
   판정례 풀에 없는 사실, 법령 해석, 일반 상식을 인용하지 마세요.
   근거를 찾을 수 없으면 '관련 판정례를 찾지 못했습니다'라고 답하세요."

[Guard Layer 2] 검색 결과 필터
  - 검색 결과 0건 → "관련 판정례 없음" 응답 (환각 생성 차단)
  - Top-K 결과의 유사도 threshold: cosine > 0.6 미만 제외

[Guard Layer 3] 응답 후 검증 (선택적)
  - 응답 내 인용 사건번호가 실제 DB에 존재하는지 확인
  - 미존재 사건번호 → 해당 인용 제거 후 재응답
```

### 6.2 프롬프트 지식 증류

대형 모델의 CoT를 SLM 프롬프트에 주입:

```typescript
const DISTILLED_PROMPT = `
[추론 가이드]
노동법 사안 분석 시 다음 단계를 순서대로 수행하세요:

1. 사실관계 정리: 누가, 무엇을, 언제, 어떤 상황에서
2. 쟁점 분류: 해고사유 존재 여부 / 절차 준수 여부 / 징계양정 적정 여부
3. 각 쟁점별 판단:
   - 해고사유: 사회통념상 근로관계를 계속할 수 없는 정도인가
   - 절차: 취업규칙/단체협약 상 인사위원회, 소명기회, 서면통지 등
   - 양정: 비위의 정도, 고의 여부, 근속연수, 반성 여부 등 종합
4. 유사 판정례 비교: 제공된 판정례와 사실관계 대조
5. 결론: 근거 판정례를 인용하여 예상 결과 제시

[금지사항]
- 판정례 풀에 없는 판례나 법령 인용 금지
- "일반적으로", "통상적으로" 등 막연한 표현 사용 금지
- 확신 없는 추론 시 "관련 판정례가 부족하여 확답하기 어렵습니다" 표현 사용
`;
```

---

## 7. Data Pipeline Design

### 7.1 의미 단위 청킹

```python
# scripts/semantic_chunking.py
def chunk_decision(text: str) -> list[str]:
    """판정례를 의미 단위로 분할"""
    sections = [
        "판정사항",     # 청구 취지
        "인정사실",     # 사실관계
        "당사자 주장",  # 양측 주장
        "판단",         # 위원회 판단
        "결론",         # 판정 결과
    ]
    chunks = []
    for section in sections:
        content = extract_section(text, section)
        if content and len(content) > 50:
            chunks.append(f"[{section}] {content}")

    # 섹션이 없는 경우 sliding window fallback
    if not chunks:
        chunks = sliding_window(text, window=512, overlap=64)

    return chunks
```

### 7.2 BGE-M3 임베딩 생성

```python
# scripts/generate_embeddings.py
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

def embed_batch(texts: list[str]) -> list[list[float]]:
    """배치 임베딩 생성 (dense vectors)"""
    result = model.encode(
        texts,
        batch_size=32,
        max_length=8192,
        return_dense=True,
        return_sparse=False,   # BM25 대체이므로 sparse 불필요
        return_colbert_vecs=False,
    )
    return result['dense_vecs']  # shape: (N, 1024)

# 실행: 42,105건 × 평균 3청크 = ~126,000 임베딩
# 예상 시간: GPU 기준 ~2시간, CPU 기준 ~12시간
```

### 7.3 피처 엔지니어링

```python
# scripts/extract_features.py
import re

def extract_quantitative_features(decision: dict) -> dict:
    """판정례에서 정량 피처 추출"""
    text = decision.get('holding_summary', '') + decision.get('holding_points', '')

    features = {
        'tenure_years': extract_tenure(text),          # 정규식: "N년차", "근속 N년"
        'company_size': extract_company_size(text),     # "종업원 N명" → small/medium/large
        'sanction_type': decision.get('sanction_type', 'unknown'),
        'prior_violations': extract_violations(text),   # "N차 징계", "이전 N회"
        'due_process_given': detect_due_process(text),  # "소명기회", "인사위원회"
        'case_type': decision.get('case_type', ''),
        'industry': extract_industry(decision.get('tags', [])),
    }
    return features

def extract_tenure(text: str) -> float | None:
    patterns = [
        r'(\d+)년\s*(\d+)?개월?\s*(?:근속|근무|재직)',
        r'근속(?:기간|연수)?\s*(?:약\s*)?(\d+)년',
        r'입사\s*(?:후|이래)\s*(\d+)년',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            years = int(m.group(1))
            months = int(m.group(2)) if m.group(2) else 0
            return years + months / 12
    return None
```

---

## 8. ML Model Training Design

### 8.1 학습 데이터셋

```
입력 피처:
  - text_embedding: BGE-M3 임베딩 1024d (판정요지 기준)
  - tenure_years: float (근속연수)
  - company_size: one-hot 3d (small/medium/large)
  - sanction_type: one-hot 5d (해고/정직/감봉/견책/강등)
  - prior_violations: int (비위횟수)
  - due_process_given: binary (소명기회)
  - case_type: one-hot Nd (사건유형)

라벨:
  - outcome: binary (인용=1, 기각=0)
    ※ 각하/조정성립은 학습 데이터에서 제외

데이터 분포 확인 필요:
  - 인용/기각 비율 → 불균형 시 SMOTE 또는 class_weight 적용
```

### 8.2 모델 학습 파이프라인

```python
# ml-server/train.py
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import StratifiedKFold
import joblib

# 공통 하이퍼파라미터
SEED = 42
N_FOLDS = 5

models = {
    'rf': RandomForestClassifier(
        n_estimators=500, max_depth=15,
        class_weight='balanced', random_state=SEED
    ),
    'xgb': XGBClassifier(
        n_estimators=500, max_depth=8, learning_rate=0.05,
        scale_pos_weight=ratio, random_state=SEED
    ),
    'cat': CatBoostClassifier(
        iterations=500, depth=8, learning_rate=0.05,
        auto_class_weights='Balanced', random_seed=SEED, verbose=0
    ),
}

# K-Fold 교차검증
skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy')
    print(f"{name}: {scores.mean():.3f} ± {scores.std():.3f}")

# 전체 데이터로 학습 + 저장
for name, model in models.items():
    model.fit(X, y)
    joblib.dump(model, f"models/{name}_model.pkl")
```

---

## 9. 파일 구조

### 9.1 프론트엔드 (Next.js)

```
src/
├── app/
│   ├── predict/
│   │   └── page.tsx              # NEW: 승률 예측 페이지
│   ├── search/
│   │   └── page.tsx              # MODIFY: 하이브리드 검색 모드 추가
│   └── api/
│       ├── predict/
│       │   └── route.ts          # NEW: FastAPI 프록시
│       └── search/
│           └── route.ts          # MODIFY: 하이브리드 검색 API
├── components/
│   ├── predict/
│   │   ├── PredictForm.tsx       # NEW
│   │   ├── PredictResult.tsx     # NEW
│   │   └── ShapChart.tsx         # NEW (Recharts 기반)
│   └── search/
│       ├── SearchModeToggle.tsx  # NEW
│       └── ScoreBreakdown.tsx    # NEW
└── lib/
    ├── types.ts                  # MODIFY: 예측 관련 타입 추가
    └── ml-client.ts              # NEW: FastAPI 호출 유틸리티
```

### 9.2 ML 서버 (Python)

```
ml-server/
├── main.py                      # FastAPI 엔트리포인트
├── models/
│   ├── rf_model.pkl
│   ├── xgb_model.pkl
│   └── cat_model.pkl
├── requirements.txt             # fastapi, scikit-learn, xgboost, catboost, shap, FlagEmbedding
└── Dockerfile                   # 배포용
```

### 9.3 데이터 파이프라인 (스크립트)

```
scripts/
├── upload_to_supabase.py        # 기존 유지
├── semantic_chunking.py         # NEW: 의미 단위 청킹
├── generate_embeddings.py       # NEW: BGE-M3 임베딩 생성
├── extract_features.py          # NEW: 정량 피처 추출
└── train_models.py              # NEW: ML 모델 학습
```

---

## 10. Implementation Order

| 순서 | Phase | 작업 | 파일 | 의존성 |
|------|-------|------|------|--------|
| 1 | A | 의미 단위 청킹 스크립트 | `scripts/semantic_chunking.py` | 없음 |
| 2 | A | BGE-M3 임베딩 생성 | `scripts/generate_embeddings.py` | Step 1 |
| 3 | A | pgvector 테이블 + 임베딩 저장 | Supabase SQL + Step 2 | Step 2 |
| 4 | A | 피처 엔지니어링 스크립트 | `scripts/extract_features.py` | 없음 |
| 5 | B | BM25 tsvector 강화 | Supabase SQL | 없음 |
| 6 | B | 하이브리드 검색 서비스 | `/api/search` 확장 | Step 3, 5 |
| 7 | B | 검색 UI 하이브리드 모드 | `SearchModeToggle`, `ScoreBreakdown` | Step 6 |
| 8 | C | ML 학습 데이터셋 구성 | `scripts/train_models.py` | Step 2, 4 |
| 9 | C | 모델 학습 + 교차검증 | `ml-server/models/` | Step 8 |
| 10 | C | FastAPI 서빙 + SHAP | `ml-server/main.py` | Step 9 |
| 11 | D | /predict 페이지 + SHAP 차트 | `app/predict/`, `components/predict/` | Step 10 |
| 12 | D | KB Guard 적용 | Edge Function 수정 | Step 3 |
| 13 | D | 프롬프트 지식 증류 | Edge Function 수정 | Step 12 |
| 14 | D | E2E 테스트 + 배포 | 전체 | 전체 |

---

## 11. 환경변수

| 변수 | 위치 | 용도 |
|------|------|------|
| `NEXT_PUBLIC_SUPABASE_URL` | Vercel | 기존 유지 |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Vercel | 기존 유지 |
| `ML_SERVER_URL` | Vercel | FastAPI 서버 URL |
| `GLM_API_KEY` | Supabase Edge Function | 기존 유지 |

---

## 12. Test Plan

| 타입 | 대상 | 기대 결과 |
|------|------|----------|
| 검색 정확도 | Precision@10, Recall@10 | 하이브리드 > 태그 매칭 (20%+ 향상) |
| 승률 예측 | 5-fold CV accuracy | 85%+ |
| 환각 테스트 | 외부 지식 유입 시도 5건 | 전부 차단 |
| SHAP 일관성 | 동일 입력 반복 | 동일 SHAP 값 |
| 응답 시간 | 검색 <1s, 예측 <3s | p95 기준 |
| UI 통합 | 5개 시나리오 (횡령, 폭행, 성희롱, 무단결근, 업무능력부족) | 전체 플로우 정상 |

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-03-20 | Initial draft (PR 기반) | Claude |
