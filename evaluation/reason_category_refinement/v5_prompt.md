# reason_category v5 — review 구조화 + 정밀도 미세조정

## 배경

v4까지의 성과:
- probation: keep 1,466 / remove 708 / review 1,810 (45.4%)
- misconduct: keep 6,632 / remove 278 / review 6,848 (49.8%)
- browse/list 오염 방어는 충분, DB 반영 전 최종판 후보

v5의 목표: **review 절반을 실질적으로 줄이는 구조화 단계**

---

## Phase 1: review 서브클러스터링

### 1-1. review를 3개 서브버킷으로 분리

현재 `needs_review`는 단일 버킷이다. 이걸 아래 3개로 나눠라:

| 서브버킷 | 기준 | 예상 행동 |
|---|---|---|
| `review_lean_keep` | score_current > 0 AND positive_hits >= 1 AND competitor_score <= score_current | 높은 확률로 keep — 다음 라운드에서 자동 승격 후보 |
| `review_lean_remove` | score_current < 0 AND (competitor_category 존재 OR negative_hits >= 2) | 높은 확률로 remove — 다음 라운드에서 자동 제거 후보 |
| `review_ambiguous` | 위 둘 다 아닌 경우 | 진짜 사람이 봐야 하는 건 |

### 1-2. 구현 방법

`evaluate_row()`에서 outcome이 `needs_review`일 때, `review_priority` 대신 (또는 추가로) `review_sub_bucket` 필드를 EvaluationResult에 추가해라.

```python
@dataclass
class EvaluationResult:
    # ... 기존 필드 ...
    review_sub_bucket: str = ""  # "lean_keep" | "lean_remove" | "ambiguous"
```

분류 로직은 `evaluate_row()` 끝에서 outcome == "needs_review"인 경우에만 적용:

```python
if outcome == "needs_review":
    if score_current > 0 and positive_hits and score_competitor <= score_current:
        review_sub_bucket = "lean_keep"
    elif score_current < 0 and (competitor_category or len(negative_hits) >= 2):
        review_sub_bucket = "lean_remove"
    else:
        review_sub_bucket = "ambiguous"
```

### 1-3. 산출물에 반영

- `report.json`의 각 reason 항목에 `review_sub_buckets: {lean_keep: N, lean_remove: N, ambiguous: N}` 추가
- `summary.md`에 서브버킷 분포 한 줄 추가
- `samples_v5.md`에서 검토필요 섹션을 3개 서브섹션으로 분리

---

## Phase 2: negative 그룹핑 + 차등 가중치

### 2-1. 현재 문제

misconduct의 negative가 40개+ 플랫 리스트. 전부 동일 가중치(-10)로 처리되는데, 실제로는:
- `성희롱`, `성추행` → 거의 확실히 sexual_harassment (강한 제거 신호)
- `절차`, `양정` → misconduct 자체 문맥에서도 자주 등장 (약한 노이즈)

### 2-2. NegativePattern 도입

```python
@dataclass
class NegativePattern:
    pattern: str
    weight: int  # 기본 -10 대신 차등
    group: str   # "strong_competitor" | "context_noise" | "default"
```

CategoryRule의 `negative`를 `list[str]` → `list[NegativePattern]`로 변환하되, 하위호환을 위해:

```python
@dataclass
class CategoryRule:
    # ... 기존 ...
    negative: list[str | NegativePattern] = field(default_factory=list)
```

`find_hits()` 내부에서 NegativePattern이면 weight를 사용, str이면 기본 -10.

### 2-3. misconduct 그룹 분류 예시

| 그룹 | weight | 패턴 예시 |
|---|---|---|
| strong_competitor | -15 | 성희롱, 성추행, 성비위, 폭행, 횡령, 배임, 갱신기대권, 계약만료 |
| context_noise | -3 | 절차, 양정, 징계위원회, 인사위원회, 서면통지 |
| default | -10 | 나머지 (사직서, 합의해지, 전보 등) |

→ 이렇게 하면 `징계사유+양정+절차` 3개가 다 걸려도 score -= 9 (vs 현재 -30)로 review 대신 keep 판정 가능

### 2-4. probation도 동일 적용

| 그룹 | weight | 패턴 예시 |
|---|---|---|
| strong_competitor | -15 | 갱신기대권, 계약만료, 갱신거절, 해고부존재, 사직서 |
| context_noise | -3 | 해고, 절차, 통상해고 |
| default | -10 | 나머지 |

---

## Phase 3: dui subtype 발전

### 3-1. 현재 상태
- `subtype=dui`로 태깅만 되고, 스코어링에 미치는 영향은 `subtype_penalty` 뿐

### 3-2. 목표
- dui 사건 중 `당연퇴직`, `면허취소`, `운전직` 키워드가 함께 있으면 → `subtype=dui_termination`
- 일반 dui 비위(음주운전으로 징계)와 dui 후속처분(면허취소→당연퇴직)을 구분

### 3-3. 구현

`infer_subtype()`에서:
```python
if subtype == "dui":
    dui_termination_signals = ["당연퇴직", "면허취소", "면허 취소", "운전직", "운전업무"]
    if any(s in text for s in dui_termination_signals):
        subtype = "dui_termination"
        # penalty는 동일하게 유지하되, 태그만 세분화
```

---

## Phase 4: probation keep 누수 최종 점검

### 4-1. 현재 문제
- `시용근로자` 문맥이 있으면 positive 히트로 keep되는데, 실제 사건 핵심이 `해고 존재/절차 위반`인 경우가 있음

### 4-2. 보정 규칙

keep 판정인데 아래 조건을 **모두** 만족하면 → `review_lean_remove`로 강등:
1. positive_hits에 `시용` 또는 `수습` 관련만 있고 `본채용 거부`가 없음
2. negative_hits에 `해고부존재` 또는 `사직서` 또는 `합의해지`가 있음
3. evidence_snippet에 `해고가 존재하지` 또는 `사직의 의사`가 포함됨

```python
# evaluate_row() 내 keep 판정 직후
if outcome == "keep" and reason == "probation":
    has_core_positive = any(h in ("본채용 거부", "본채용거부") for h in positive_hits)
    has_dismissal_negative = any(h in negative_hits for h in ["해고부존재", "사직서", "합의해지", "해고가 존재하지"])
    if not has_core_positive and has_dismissal_negative:
        # keep → review_lean_remove로 강등
        outcome = "needs_review"
        review_sub_bucket = "lean_remove"
```

---

## 실행 순서

1. Phase 1 (서브클러스터링) 먼저 구현 + 실행 → 분포 확인
2. Phase 2 (차등 가중치) 구현 + 실행 → review 감소량 확인
3. Phase 3 (dui) + Phase 4 (probation 누수) 함께 구현
4. 전체 v5 실행 → report/summary/samples 생성
5. v4 대비 비교 리포트 생성

## 버전 라벨
- `--version-label v5`
- `--compare-report` 에 v4 report.json 경로 지정

## 주의사항
- `search-modes.ts`의 REASON_TEXT_GUARDS는 이번에는 건드리지 마. v5는 payload 스코어링 내부만 변경
- Phase 2에서 NegativePattern 도입 시 기존 str 패턴과 하위호환 유지 필수
- 산출물 디렉토리는 새 타임스탬프로 생성
- DB 반영(`--apply-db`)은 하지 마. payload만 생성
