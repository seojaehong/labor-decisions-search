# Claude Rear Review

- 작성시각: 2026-03-20 21:47
- 범위: `absence/violence/workplace_bullying_batch_031~033`
- 총량: 9배치, 236건
- 목적: Claude rear 산출물을 기준축으로 삼아 이후 전체 corpus의 스타일을 통일할 파일 기준 정리

## 총평

- 구조 품질은 안정적이다.
- `notes` 공란 0건
- `confidence=medium` 8건으로 절제되어 있음
- exclusion flag가 주제와 실제 결론의 간극을 설명하는 방식으로 적극 사용되어, "레거시 배치명"과 "실제 판단축"이 잘 분리됨

이 구간은 이후 통합 QA의 기준 샘플로 삼아도 된다.

## Claude 기준 파일 스타일

아래 4가지를 통일 기준으로 삼는 것이 좋다.

1. `confidence`
- 본문이 짧아도 결론축이 명확하면 `high`
- 진짜 경계 사건이나 source 빈약 사례만 `medium`

2. `exclusion_flags`
- 배치 주제와 실제 쟁점이 어긋날 때 숨기지 않고 바로 표시
- 예: `not_really_absence_case`, `not_really_harassment_case`, `unrelated_to_dismissal`

3. `notes`
- 비워두지 않고, 왜 이 primary를 잡았는지 한 문장으로 남김
- 경계 사건은 competing frame을 notes에 드러냄

4. `primary` 선택
- topic batch 이름을 억지로 따라가지 않고, 실제 위원회 판단구조를 그대로 우선
- 그래서 violence/bullying 배치에서도 `disciplinary_severity`, `misconduct`, `dismissal_validity`, `transfer_validity`가 자연스럽게 분산됨

## 분포 점검

### absence 031~033

- 상위 primary:
  - `absence_without_leave` 21
  - `misconduct` 19
  - `dismissal_validity` 14
  - `disciplinary_severity` 11
- 해석:
  - 무단결근이 핵심일 때만 absence를 유지하고
  - 배경 사유일 때는 `misconduct`나 `dismissal_validity`로 자연스럽게 이동시킴

### violence 031~033

- 상위 primary:
  - `disciplinary_severity` 32
  - `misconduct` 19
  - `dismissal_validity` 9
  - `procedure` 6
- 해석:
  - 폭행 사실 자체보다 징계 양정 또는 복합 비위 구조를 우선한 흔적이 뚜렷함
  - violence batch를 "폭행 keyword bucket"이 아니라 "판정 구조 재선별"로 다룬 점이 안정적임

### workplace_bullying 031~033

- 상위 primary:
  - `disciplinary_severity` 31
  - `workplace_harassment` 24
  - `transfer_validity` 9
  - `dismissal_validity` 8
- 해석:
  - 괴롭힘 성립 사건과, 괴롭힘 allegations를 전제로 한 징계/전보 사건을 분리한 점이 좋음

## exclusion flag 사용 점검

전체 상위 flag:

- `not_really_absence_case` 43
- `not_really_harassment_case` 34
- `resignation_dispute` 16
- `procedure_dominant` 11
- `unrelated_to_dismissal` 11

평가:

- 배치 주제와 실제 판정축이 다를 때 flag를 적극적으로 남겨서 후속 merge/검색 품질에 유리함
- 특히 absence와 bullying에서 "주제가 배경일 뿐"이라는 사실을 잘 보존하고 있음

## watchlist

즉시 수정 요청은 아니지만, 아래 8건은 medium으로 둔 이유를 유지 메모로 삼으면 좋다.

| case_id | batch | 현재 primary | 관찰 |
|---|---:|---|---|
| id_346751 | absence_031 | misconduct | 무단결근과 타 비위가 동급으로 섞인 복합 사건 |
| id_346845 | absence_031 | misconduct | 직무태만/명령불복종/무단결근 혼합 |
| id_347069 | absence_031 | misconduct | 무단결근과 기밀유출이 함께 서는 사례 |
| id_351665 | violence_033 | unfair_treatment | violence 레거시와 실제 쟁점의 간극이 큰 특수 사건 |
| id_45347 | bullying_032 | disciplinary_severity | 괴롭힘 성립 불명확 + 조직갈등 혼재 |
| id_4537 | bullying_032 | disciplinary_severity | 같은 이유로 양정 중심 처리 |
| id_45943 | bullying_033 | workplace_harassment | source 요약이 짧아 세부 행위유형 분해는 제한적 |
| id_45985 | bullying_033 | disciplinary_severity | source가 짧지만 양정 과다 결론은 유지 가능 |

## 결론

- Claude rear 031~033은 현재 corpus에서 가장 일관적인 "보수적 태깅 기준"에 가깝다.
- 앞으로 Codex QA는 이 스타일을 기준선으로 삼아
  - `worker_status` 축소
  - `procedure` 단독 사용 축소
  - `medium` 절제
  - `notes` 설명력 유지
  방향으로 맞추면 통합 결과가 한 사람이 한 것처럼 보일 가능성이 높다.

## Incremental QA Snapshot (2026-03-20 22:06)

- 범위: `absence, violence, workplace_bullying` / `batch_015~017`
- 원칙: 직접 수정 없이 `case_id + 수정 제안 + 근거`만 누적

### absence

- 완료 레코드: 90건
- `worker_status`: 3건
- `procedure`: 7건
- `confidence=medium`: 1건 (1.1%)
- `notes` 공란: 0건
- 상위 primary: `absence_without_leave` 25, `dismissal_validity` 20, `disciplinary_severity` 15, `misconduct` 14, `procedure` 7
- 상위 exclusion_flags: `not_really_absence_case` 49, `resignation_dispute` 7, `procedure_dominant` 3, `evidence_too_thin` 3, `unrelated_to_dismissal` 2

- `worker_status` 재검토 후보: `id_22873`, `id_23407`, `id_24435`
- `procedure` 재검토 후보: `id_22851`, `id_23129`, `id_24281`, `id_24605`, `id_24749`
- `medium` 재검토 후보: `id_23427`

### violence

- 완료 레코드: 90건
- `worker_status`: 2건
- `procedure`: 7건
- `confidence=medium`: 3건 (3.3%)
- `notes` 공란: 0건
- 상위 primary: `disciplinary_severity` 33, `misconduct` 30, `dismissal_validity` 11, `procedure` 7, `absence_without_leave` 2
- 상위 exclusion_flags: `not_really_performance_case` 7, `resignation_dispute` 7, `unrelated_to_dismissal` 7, `fact_specific_low_reusability` 5, `not_really_harassment_case` 4

- `worker_status` 재검토 후보: `id_25637`, `id_25751`
- `procedure` 재검토 후보: `id_2491`, `id_25091`, `id_255`, `id_25945`, `id_25949`
- `medium` 재검토 후보: `id_24577`, `id_24699`, `id_26875`

### workplace_bullying

- 완료 레코드: 90건
- `worker_status`: 0건
- `procedure`: 3건
- `confidence=medium`: 0건 (0.0%)
- `notes` 공란: 0건
- 상위 primary: `workplace_harassment` 50, `transfer_validity` 11, `disciplinary_severity` 8, `misconduct` 7, `dismissal_validity` 3
- 상위 exclusion_flags: `not_really_harassment_case` 32, `unrelated_to_harassment` 3, `procedure_dominant` 3

- `procedure` 재검토 후보: `id_403775`, `id_404371`, `id_404419`
