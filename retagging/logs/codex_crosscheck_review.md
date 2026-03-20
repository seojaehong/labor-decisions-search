# Codex Cross-Check Review

- 작성시각: 2026-03-20 21:47
- 범위: `probation_batch_015` ~ `probation_batch_030`
- 목적: Codex 산출물을 Claude rear 산출물의 보수적 기준에 맞춰 재검토할 후보만 추려서 제안
- 원칙: reviewed JSONL 직접 수정 금지, 아래는 모두 `case_id + 수정 제안` 메모

## 요약

- 전체 480건 기준으로 `worker_status` primary 31건, `procedure` primary 60건, `confidence=medium` 67건으로 앞 구간(`001~014`) 대비 상승폭이 큼
- 특히 `worker_status`와 `procedure`는 "선결 쟁점"을 primary로 올린 흔적이 보여, Claude rear 산출물의 기준보다 공격적으로 태깅된 흔적이 있음
- `id_3097` enum 위반은 이미 수정 반영된 상태로 확인됨

## 기준 재정렬

- `worker_status` primary:
  근로자성 자체가 최종 결론일 때만 유지. 수습 여부 확인 뒤 본채용거부/해고 정당성으로 결론이 가면 `dismissal_validity` 쪽이 더 안정적임.
- `procedure` primary:
  절차 하자가 유일한 결론축일 때만 유지. 실체 사유 심사가 충분히 들어가면 `dismissal_validity` 또는 `work_ability`를 primary로 두고 `procedure`는 secondary가 더 일관적임.
- `confidence=medium`:
  실제 애매함이 아니라 "복합 사건" 또는 "요약형 source" 때문에 낮춘 흔적이 많음. Claude rear는 같은 조건에서도 대부분 `high`를 유지했음.

## 1. `worker_status` 재검토 우선 후보

다음 건들은 `worker_status`가 선결 쟁점으로만 기능하고, 실제 결론은 본채용거부/해고 정당성으로 읽혀 `dismissal_validity` 전환 검토가 필요하다.

| case_id | batch | 현재 | 제안 | 근거 |
|---|---:|---|---|---|
| id_33473 | 17 | worker_status | dismissal_validity | `rejection_of_regular_employment` + `dismissal_validity/work_ability`가 이미 secondary에 함께 있음 |
| id_33901 | 17 | worker_status | dismissal_validity | 채용경력 은폐가 핵심 사유로 읽혀 status 자체보다 본채용거부 정당성 심사 구조에 가까움 |
| id_34195 | 17 | worker_status | dismissal_validity | 사용자 적격과 수습평가 재량이 같이 다뤄지나 결론은 본채용거부 판단 |
| id_344699 | 19 | worker_status | dismissal_validity | 평가/결근/본채용거부 사유가 모두 secondary에 있고 결론축도 rejection 쪽 |
| id_345355 | 20 | worker_status | dismissal_validity | 시용 부정 후 일반 해고 정당성 및 절차 위법으로 넘어가므로 status 단독축이 아님 |
| id_345787 | 20 | worker_status | dismissal_validity | 5인 이상 여부 + 본채용거부 실체/절차를 함께 봄 |
| id_345929 | 20 | worker_status | dismissal_validity | "시용 아님"은 선결단계이고 결론은 일반 해고 부당 판단 |
| id_346847 | 21 | worker_status | dismissal_validity | 시용 여부 확인 뒤 종료 원인과 실질 사유, 절차, 양정까지 들어감 |
| id_347213 | 21 | worker_status | dismissal_validity | 사용자 적격과 본채용거부 존재 인정 후 절차 하자까지 보는 2단 구조 |
| id_348647 | 22 | worker_status | dismissal_validity | 채용내정 취소/해고 존재 여부 판단으로 읽혀 status보다 dismissal frame이 강함 |

유지 가능 후보:

- `id_33921`
- `id_344509`
- `id_347399`
- `id_347401`
- `id_347491`
- `id_347895`
- `id_348825`

위 사건들은 근로계약 성립, 견습/실습의 근로자성, 기간제 종료 구조처럼 status 또는 법적 지위 자체가 결론에 더 가깝다.

## 2. `procedure` 재검토 우선 후보

다음 건들은 절차 하자가 중요하더라도, 실체 사유 심사가 함께 충분히 들어가 있어 Claude rear 기준이면 `dismissal_validity` 또는 `work_ability` primary가 더 자연스럽다.

| case_id | batch | 현재 | 제안 | 근거 |
|---|---:|---|---|---|
| id_32189 | 16 | procedure | work_ability | 시용해지 사유의 적절성 검토가 함께 보임 |
| id_34301 | 18 | procedure | dismissal_validity | 평가 객관성은 대체로 인정하되 서면통지 흠결을 추가로 본 구조 |
| id_343979 | 18 | procedure | dismissal_validity | 지시불이행/사직 의사/평가 공정성 등 실체 판단 비중이 큼 |
| id_344115 | 18 | procedure | work_ability | 평가자 1인 주관, 정성 평가 등 실체 심사가 상당 부분 차지 |
| id_344865 | 19 | procedure | work_ability | 객관적 근무평가 부재가 중심이어서 절차보다 평가 실체가 앞섬 |
| id_347379 | 21 | procedure | dismissal_validity | attendance/evaluation/work_ability/worker_status가 함께 붙은 복합 본채용거부 사건 |
| id_348295 | 22 | procedure | dismissal_validity | `misconduct + dismissal_validity` secondary를 가진 복합 사건 |
| id_348735 | 23 | procedure | dismissal_validity | `dismissal_validity + work_ability` secondary가 이미 붙어 있음 |
| id_348827 | 23 | procedure | dismissal_validity | 본채용거부 사유와 평가 적정성 심사가 동반됨 |
| id_349169 | 23 | procedure | dismissal_validity | dismissal frame이 분명하고 procedure는 보조축에 가까움 |

유지 가능 후보:

- `id_343`
- `id_344041`
- `id_344159`
- `id_347949`

위 사건들은 서면통지 또는 절차 흠결이 결론을 거의 단독으로 좌우하는 쪽에 가까워 현재 태그 유지 여지가 있다.

## 3. `confidence=medium` 상향 검토 후보

`015~030`의 medium 67건 중 아래 건들은 notes가 이미 명확하고 결론 구조도 비교적 선명해 `high` 상향 여지가 크다.

| case_id | batch | 현재 primary | 제안 | 근거 |
|---|---:|---|---|---|
| id_32081 | 16 | dismissal_validity | high | 사직의사표시 효력 다툼이라는 결론축이 명확 |
| id_32245 | 16 | renewal_expectation | high | 수습이 아니라 기간제 종료라고 notes가 선명하게 적시 |
| id_32455 | 16 | renewal_expectation | high | 갱신 관행 비교라는 판단 구조가 분명 |
| id_32741 | 16 | renewal_expectation | high | 형식적 평가에 의한 갱신거절 구조가 명확 |
| id_33185 | 17 | renewal_expectation | high | 수습 표기 혼입에도 실질은 기간제 사건이라고 notes가 명확 |
| id_34143 | 17 | dismissal_validity | high | 일반 해고 사유 입증 실패라는 결론축이 선명 |
| id_343689 | 18 | dismissal_validity | high | source가 짧아도 결론은 이미 명확하게 정리됨 |
| id_344209 | 19 | dismissal_validity | high | 복직명령으로 구제이익 소멸이라는 mootness 구조가 명확 |
| id_344359 | 19 | dismissal_validity | high | 해고 존재 자체 부정이라는 축이 분명 |
| id_34667 | 21 | dismissal_validity | high | 수습기간 도과 후 일반 해고로 본다는 논리가 선명 |

medium 유지 쪽이 더 안전한 후보:

- `id_32575`
- `id_33901`
- `id_33921`
- `id_343783`
- `id_343855`
- `id_343897`
- `id_343985`

위 사건들은 status/합의해지/복직명령 진정성처럼 경계 판단 요소가 살아 있어 medium 유지가 이해된다.

## 메모

- 이번 검토는 직접 수정이 아니라 "재검토 우선순위" 제안이다.
- 앞으로 통일 기준은 Claude rear 산출물처럼
  - `worker_status` 보수 사용
  - `procedure` 단독 결정사유일 때만 primary
  - `medium` 최소화
  - `notes`는 결론축을 한 문장으로 명확히 남기기
  로 맞추는 편이 전체 corpus를 한 사람이 한 것처럼 보이게 한다.
