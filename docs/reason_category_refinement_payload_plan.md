# reason_category 정제 payload 계획

## 목적

`browse/list` 품질을 우선 회복하기 위해 `reason_category` 과태깅이 심한 범주부터
**DB 반영 직전 payload**를 준비한다.

이번 단계는 실제 DB 업데이트가 아니라, 안전하게 검토할 수 있는
`updates.jsonl`, 샘플 비교, 요약 리포트를 만드는 데 초점을 둔다.

## 현재 우선순위

1. `worker_status`
2. `no_dismissal`
3. `incompetence`

## 최신 payload 기준 수치

- 전체 대상: `28,665`
- 유지: `12,413`
- 제거 후보: `16,252`
- 인정(구제) browse/list 전/후: `5,765 -> 1,976`

### worker_status

- 전체: `12,196`
- 유지: `3,704`
- 제거 후보: `8,492`
- 인정(구제) 전/후: `2,487 -> 631`

핵심 해석:
- `도급/파견` 자체가 아니라, `근로자성 판단 문맥`이 없는 사건이 많이 섞여 있다.
- 양정, 전보, 일반 해고 정당성 사건이 크게 섞여 있어 우선 정제 가치가 가장 높다.

### no_dismissal

- 전체: `14,230`
- 유지: `7,755`
- 제거 후보: `6,475`
- 인정(구제) 전/후: `2,754 -> 1,105`

핵심 해석:
- `권고사직/사직서/합의해지/당연퇴직/해고 존재 여부` 문맥이 없는 사건이 섞여 있다.
- `해고 절차`, `양정`, 일반 징계 사건과의 혼선이 크다.

### incompetence

- 전체: `2,239`
- 유지: `954`
- 제거 후보: `1,285`
- 인정(구제) 전/후: `524 -> 240`

핵심 해석:
- `업무능력 부족`, `저성과`, `개선기회`, `경고/시정/교육` 문맥이 없는 사건이 많다.
- 일반 비위행위, 양정, 수습/본채용 계열 사건과의 경계 정리가 필요하다.

## 산출물 위치

- payload 리포트:
  - `evaluation/reason_category_refinement/20260401_*/report.json`
- 전체 업데이트 payload:
  - `evaluation/reason_category_refinement/20260401_*/all_updates.jsonl`
- 범주별 payload:
  - `evaluation/reason_category_refinement/20260401_*/worker_status_updates.jsonl`
  - `evaluation/reason_category_refinement/20260401_*/no_dismissal_updates.jsonl`
  - `evaluation/reason_category_refinement/20260401_*/incompetence_updates.jsonl`

## 다음 반영 순서

1. `worker_status` 제거 후보 샘플 1회 수동 검토
2. `worker_status`만 DB 반영
3. browse/list 확인
4. 같은 방식으로 `no_dismissal`
5. 마지막으로 `incompetence`

## 주의

- 현재 browse/list 가드는 이미 서비스 코드에 들어가 있어 화면 품질 방어는 시작된 상태다.
- 그러나 실제 태그 재정제는 대량 DB 업데이트이므로, 반영 전 최종 확인이 필요하다.
