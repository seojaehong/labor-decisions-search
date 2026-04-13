# v6 Step 1: misconduct lean_remove 자동 이관

## 배경

v5 결과:
- misconduct 전체 13,758건
- review_sub_bucket 분포: lean_remove 4,376 / ambiguous 1,924 / lean_keep 245
- lean_remove 4,376건은 "높은 확률로 misconduct가 아닌" 건들 — 이걸 하위유형별로 분류하여 올바른 카테고리로 자동 이관하는 것이 목표

## 목표

misconduct `lean_remove` 4,376건을 하위유형별로 분류하고, 각 유형에 대한 **자동 이관 규칙**을 생성한다.

---

## Phase 1: lean_remove 하위유형 클러스터링

### 1-1. v5 report.json에서 misconduct lean_remove 전체 로드

```python
# v5 산출물에서 misconduct의 review_sub_bucket == "lean_remove"인 건들 추출
# 각 건의 negative_hits, competitor_category, evidence_snippet을 수집
```

### 1-2. 이관 대상 카테고리 분류

lean_remove의 negative_hits와 evidence_snippet을 기반으로 아래 하위유형으로 분류:

| 이관 대상 | 식별 기준 (negative_hits 또는 evidence 기반) | 예상 규모 |
|---|---|---|
| `sexual_harassment` | 성희롱, 성추행, 성비위, 성적 언동 | 대 |
| `violence` | 폭행, 폭언, 상해, 물리적 위력 | 중 |
| `embezzlement` | 횡령, 배임, 금전, 공금, 비자금 | 중 |
| `workplace_bullying` | 괴롭힘, 직장 내 괴롭힘, 따돌림 | 중 |
| `transfer` | 전보, 인사이동, 대기발령, 직위해제 | 소 |
| `probation` | 수습, 시용, 본채용 거부, 본채용 | 소 |
| `incompetence` | 저성과, 근무성적, 업무능력 부족, 성과미달 | 소 |
| `contract_expiry` | 계약만료, 갱신거절, 갱신기대권, 기간만료 | 소 |
| `no_dismissal` | 사직서, 합의해지, 권고사직, 해고 부존재 | 중 |
| `redundancy` | 경영상 해고, 정리해고, 구조조정, 인원감축 | 소 |
| `unknown_remove` | 위 어디에도 해당 안 되는 잡음 (비노동 등) | 소 |

### 1-3. 분류 로직 구현

`reason_category_refine_payloads.py`에 새 함수 추가:

```python
def classify_lean_remove(negative_hits: list[str], evidence: str, competitor_category: str) -> str:
    """lean_remove 건의 이관 대상 카테고리를 결정한다."""

    # 1순위: competitor_category가 이미 있으면 그대로 사용
    if competitor_category and competitor_category != "misconduct":
        return competitor_category

    # 2순위: negative_hits 기반 매칭 (강한 신호 우선)
    MIGRATION_MAP = {
        "sexual_harassment": ["성희롱", "성추행", "성비위", "성적 언동", "성적 수치심"],
        "violence": ["폭행", "폭언", "상해", "물리적 위력", "주먹", "멱살"],
        "embezzlement": ["횡령", "배임", "공금", "비자금", "금전 유용"],
        "workplace_bullying": ["괴롭힘", "직장 내 괴롭힘", "따돌림", "괴롭힘 행위"],
        "transfer": ["전보", "인사이동", "대기발령", "직위해제", "보직변경"],
        "probation": ["수습", "시용", "본채용 거부", "본채용거부", "견습"],
        "incompetence": ["저성과", "근무성적", "업무능력 부족", "성과미달", "근무태만"],
        "contract_expiry": ["계약만료", "갱신거절", "갱신기대권", "기간만료", "기간제"],
        "no_dismissal": ["사직서", "합의해지", "권고사직", "해고 부존재", "해고가 존재하지"],
        "redundancy": ["경영상 해고", "정리해고", "구조조정", "인원감축", "긴박한 경영상"],
    }

    # negative_hits에서 직접 매칭
    for target_cat, patterns in MIGRATION_MAP.items():
        if any(p in " ".join(negative_hits) for p in patterns):
            return target_cat

    # 3순위: evidence_snippet에서 매칭
    for target_cat, patterns in MIGRATION_MAP.items():
        if any(p in evidence for p in patterns):
            return target_cat

    return "unknown_remove"
```

### 1-4. 산출물

1. **`misconduct_lean_remove_migration_v6.json`**
   ```json
   {
     "total": 4376,
     "migration_distribution": {
       "sexual_harassment": N,
       "violence": N,
       "embezzlement": N,
       "workplace_bullying": N,
       "transfer": N,
       "probation": N,
       "incompetence": N,
       "contract_expiry": N,
       "no_dismissal": N,
       "redundancy": N,
       "unknown_remove": N
     },
     "items": [
       {
         "id": "...",
         "current_category": "misconduct",
         "proposed_category": "sexual_harassment",
         "migration_basis": "negative_hit: 성희롱",
         "evidence_snippet": "...",
         "confidence": "high"  // high: competitor match, medium: negative match, low: evidence match
       }
     ]
   }
   ```

2. **`misconduct_lean_remove_samples_v6.md`** — 이관 대상별 5건씩 샘플

3. **`misconduct_lean_remove_summary_v6.md`** — 분포 요약 + 검토 포인트

---

## Phase 2: 자동 이관 confidence 임계값

- `high` (competitor_category 직접 매칭): 자동 이관 OK
- `medium` (negative_hits 매칭): 자동 이관 OK (단, 샘플 검토 후)
- `low` (evidence만 매칭): review로 유지, 수동 확인 필요

---

## 실행 순서

1. v5 산출물 로드 (misconduct review_sub_bucket == "lean_remove")
2. `classify_lean_remove()` 적용 → 분포 확인
3. 이관 대상별 샘플 5건씩 출력 → 정탐 확인
4. 분포 + 샘플 → summary 생성
5. **DB 반영하지 않음** — 산출물만 생성

## 버전 라벨
- `--version-label v6-step1`

## 주의사항
- DB 반영(`--apply-db`) 절대 하지 마
- `search-modes.ts` 건드리지 마
- v5 산출물 디렉토리 경로: Windows에서는 `C:\dev\labor-decisions-search\evaluation\reason_category_refinement\20260402_224157\`
- 새 산출물은 새 타임스탬프 폴더에 생성
