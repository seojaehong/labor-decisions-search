# Phase C Labeling v2

## 목적

`decision_result` 기반 1차 이진 라벨링에서 남는 `upheld / overturned / 특수 사건`의 `판단불가`를 줄여, Phase C 학습 데이터셋 usable 수를 늘린다.

## 1차 기준

- `worker_win`
  - `granted`
  - `partial`
- `user_win`
  - `dismissed`
  - `rejected`
- `undecidable`
  - `upheld`
  - `overturned`
  - `other`

이 기준은 보수적이지만 usable 손실이 컸다.

## 2차 보강 전략

### 1. 직접 매핑 유지

- `전부인정`, `일부인정`, `인용`, `일부시정`, `전부시정` → `worker_win`
- `기각`, `각하` → `user_win`

### 2. 재심 사건 heuristic

대상:

- `upheld`
- `overturned`
- `초심유지`
- `초심취소`
- `초심일부취소`

판정 텍스트는 아래 3개를 결합한다.

1. `holding_summary`
2. `key_issue`
3. `holding_points` 마지막 300자

### 3. 결론 패턴

`worker_win` 패턴:

- `부당하다`
- `양정이 과하`
- `합리적 이유가 없`
- `부당한`
- `위반에 해당`
- `부당하므로`
- `근로자에 해당`
- `갱신기대권이 인정`
- `해고가 존재한다`

`user_win` 패턴:

- `정당하다`
- `하자가 없`
- `존재하지 않`
- `적격이 없`
- `볼 수 없`
- `이유 없다`
- `근로자에 해당하지 않`
- `갱신기대권이 인정되지 않`
- `해고가 존재하지 않`

### 4. 판정 규칙

- 양쪽 다 안 잡히면 `undecidable`
- 양쪽 다 잡히면:
  - 마지막 등장 위치가 더 뒤인 쪽 우선
  - `holding_summary`/`key_issue` 쪽이 잡히면 tail보다 더 강한 신호로 본다

## 목표

- usable `36,000+`
- undecidable `6,000 이하`

## 운영 원칙

- 원본 DB 값을 수정하지 않는다
- 라벨 생성은 별도 JSONL 산출물로만 관리한다
- `upheld/overturned`는 heuristic으로 풀되, 실패군은 계속 `undecidable`로 남긴다
- Phase C 1차 모델은 “깨끗한 usable”이 우선이며, 억지 분류로 오염시키지 않는다
