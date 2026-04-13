# v6 Step 2: probation ambiguous 세분화

## 배경

v5 결과:
- probation 전체 3,984건
- review_sub_bucket 분포: lean_keep 2,608 / ambiguous 1,100 / lean_remove 276
- lean_keep 2,608건은 순수 수습/시용 건으로 유지
- lean_remove 276건은 Step 1의 misconduct lean_remove와 유사하게 별도 이관 처리 가능
- **ambiguous 1,100건**이 핵심 — "수습 관련인 것 같지만 실제로는 다른 쟁점이 주인 건"들

## 목표

probation `ambiguous` 1,100건을 하위유형별로 분류하고, 각 유형에 대한 **재분류 규칙**을 생성한다.

---

## Phase 1: ambiguous 하위유형 클러스터링

### 1-1. v5 report.json에서 probation ambiguous 전체 로드

```python
# v5 산출물에서 probation의 review_sub_bucket == "ambiguous"인 건들 추출
# 각 건의 positive_hits, negative_hits, competitor_category, evidence_snippet 수집
```

### 1-2. 세분화 대상 카테고리 분류

ambiguous의 positive_hits/negative_hits/evidence를 기반으로 아래 하위유형으로 분류:

| 세분화 유형 | 식별 기준 | 예상 규모 | 처리 방향 |
|---|---|---|---|
| `probation_pure` | 수습/시용/본채용 거부가 **주 쟁점**, negative가 약함 | 중 | probation 유지 (lean_keep으로 승격) |
| `contract_expiry` | 계약만료, 갱신거절, 갱신기대권, 기간제가 핵심 쟁점 | 대 | contract_expiry로 이관 |
| `no_dismissal` | 사직서, 합의해지, 권고사직, 해고 부존재 | 중 | no_dismissal로 이관 |
| `dismissal_procedure` | 해고절차, 서면통지, 해고예고, 30일 전, 절차적 하자 | 소 | dismissal_procedure로 이관 |
| `misconduct_overlap` | 비위, 징계, 성희롱 등 misconduct 요소가 강함 | 소 | misconduct로 이관 |
| `incompetence` | 근무성적, 업무능력 부족, 저성과 | 소 | incompetence로 이관 |
| `unknown_ambiguous` | 위 어디에도 해당 안 되는 건 | 소 | review로 유지, 수동 확인 |

### 1-3. 분류 로직 구현

`reason_category_refine_payloads.py`에 새 함수 추가:

```python
def classify_probation_ambiguous(
    positive_hits: list[str],
    negative_hits: list[str],
    evidence: str,
    competitor_category: str
) -> str:
    """probation ambiguous 건의 세분화 카테고리를 결정한다."""

    # 1순위: competitor_category가 probation이 아닌 다른 카테고리면 그대로 사용
    VALID_COMPETITORS = {
        "contract_expiry", "no_dismissal", "dismissal_procedure",
        "misconduct", "incompetence", "redundancy"
    }
    if competitor_category in VALID_COMPETITORS:
        return competitor_category

    # 2순위: negative_hits 강도 기반 — negative가 probation보다 강한 신호면 이관
    SEGMENTATION_MAP = {
        "contract_expiry": [
            "계약만료", "갱신거절", "갱신기대권", "기간만료", "기간제",
            "계약기간", "갱신", "기간의 정함"
        ],
        "no_dismissal": [
            "사직서", "합의해지", "권고사직", "해고 부존재", "해고가 존재하지",
            "사직의 의사표시", "자발적 퇴직", "합의퇴직"
        ],
        "dismissal_procedure": [
            "서면통지", "해고예고", "해고통지", "30일 전", "절차적 하자",
            "해고절차", "통보 절차", "서면으로 통지"
        ],
        "misconduct_overlap": [
            "비위", "징계", "성희롱", "횡령", "폭행", "폭언",
            "비위행위", "징계해고", "징계사유"
        ],
        "incompetence": [
            "근무성적", "업무능력 부족", "저성과", "성과미달",
            "근무태만", "업무수행 능력"
        ],
    }

    # negative_hits에서 매칭 (probation이 아닌 다른 쟁점이 주인 경우)
    neg_text = " ".join(negative_hits)
    for target_cat, patterns in SEGMENTATION_MAP.items():
        if any(p in neg_text for p in patterns):
            return target_cat

    # 3순위: evidence_snippet에서 매칭
    for target_cat, patterns in SEGMENTATION_MAP.items():
        if any(p in evidence for p in patterns):
            return target_cat

    # 4순위: positive_hits 강도 확인 — probation 신호가 여전히 강하면 유지
    PROBATION_STRONG = ["수습", "시용", "본채용 거부", "본채용거부", "수습기간", "시용기간"]
    pos_text = " ".join(positive_hits)
    if any(p in pos_text for p in PROBATION_STRONG):
        return "probation_pure"

    return "unknown_ambiguous"
```

### 1-4. 핵심 판별 기준 상세

ambiguous가 된 이유는 "positive와 negative가 모두 있어서"이다. 세분화의 핵심은:

1. **negative 쪽이 더 강한가?** → negative가 가리키는 카테고리로 이관
   - 예: positive에 "수습기간" 있지만, negative에 "계약만료", "갱신기대권" → `contract_expiry`
   - 예: positive에 "시용" 있지만, negative에 "사직서", "합의해지" → `no_dismissal`

2. **positive 쪽이 더 강한가?** → probation 유지
   - 예: negative에 약한 신호("해고")만 있고, positive에 "수습기간 중 본채용 거부" → `probation_pure`

3. **양쪽 다 약한가?** → `unknown_ambiguous`

### 1-5. 산출물

1. **`probation_ambiguous_segmentation_v6.json`**
   ```json
   {
     "total": 1100,
     "segmentation_distribution": {
       "probation_pure": N,
       "contract_expiry": N,
       "no_dismissal": N,
       "dismissal_procedure": N,
       "misconduct_overlap": N,
       "incompetence": N,
       "unknown_ambiguous": N
     },
     "items": [
       {
         "id": "...",
         "current_category": "probation",
         "current_sub_bucket": "ambiguous",
         "proposed_action": "migrate",
         "proposed_category": "contract_expiry",
         "segmentation_basis": "negative_hit: 갱신기대권, 계약만료",
         "positive_hits_summary": "수습, 시용기간",
         "negative_hits_summary": "갱신기대권, 계약만료, 기간제",
         "evidence_snippet": "...",
         "confidence": "high"
       }
     ]
   }
   ```

2. **`probation_ambiguous_samples_v6.md`** — 세분화 유형별 5건씩 샘플

3. **`probation_ambiguous_summary_v6.md`** — 분포 요약 + 검토 포인트

---

## Phase 2: 세분화 후 처리 방향

| 세분화 유형 | 처리 | confidence 기준 |
|---|---|---|
| `probation_pure` | probation 유지 (lean_keep 승격) | medium 이상 |
| `contract_expiry` | contract_expiry로 이관 | high: competitor, medium: negative, low: evidence |
| `no_dismissal` | no_dismissal로 이관 | high: competitor, medium: negative, low: evidence |
| `dismissal_procedure` | dismissal_procedure로 이관 | medium 이상 |
| `misconduct_overlap` | misconduct로 이관 | medium 이상 |
| `incompetence` | incompetence로 이관 | medium 이상 |
| `unknown_ambiguous` | review로 유지, 수동 확인 | — |

### 자동 이관 임계값
- `high` (competitor_category 직접 매칭): 자동 이관 OK
- `medium` (negative_hits 매칭): 자동 이관 OK (단, 샘플 검토 후)
- `low` (evidence만 매칭): review로 유지, 수동 확인 필요

---

## Phase 3: probation lean_remove 276건 처리

lean_remove 276건은 Step 1의 misconduct lean_remove와 동일한 로직 적용:
- `classify_lean_remove()` 함수 재사용 (Step 1에서 작성한 것)
- 단, probation → 다른 카테고리 이관이므로 `current_category`가 "probation"

산출물: `probation_lean_remove_migration_v6.json` (Step 1과 동일 포맷)

---

## 실행 순서

1. v5 산출물 로드 (probation review_sub_bucket == "ambiguous")
2. `classify_probation_ambiguous()` 적용 → 분포 확인
3. 세분화 유형별 샘플 5건씩 출력 → 정탐 확인
4. 분포 + 샘플 → summary 생성
5. (선택) probation lean_remove 276건도 classify_lean_remove() 적용
6. **DB 반영하지 않음** — 산출물만 생성

## 버전 라벨
- `--version-label v6-step2`

## 주의사항
- DB 반영(`--apply-db`) 절대 하지 마
- `search-modes.ts` 건드리지 마
- v5 산출물 디렉토리 경로: Windows에서는 `C:\dev\labor-decisions-search\evaluation\reason_category_refinement\20260402_224157\`
- 새 산출물은 새 타임스탬프 폴더에 생성
- probation_pure로 분류된 건은 **이관이 아니라 유지**임을 명확히 구분
