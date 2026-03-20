# probation_batch_015 self-review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_015.jsonl`
- 출력: `retagging/output/reviewed/probation_batch_015_reviewed.jsonl`
- 총 30건

## primary/secondary가 흔들린 대표 사례
- `id_3091`
  - 평가점수 미달도 있으나 핵심은 업무지시 거부·무단이탈의 비위성이라 `misconduct`를 primary로 선택.
- `id_31517`
  - 수습근로자 사건이지만 폭행·욕설·지시불응이 해고 정당성을 좌우해 `misconduct + disciplinary_dismissal`로 정리.
- `id_31787`
  - 평가점수와 욕설/지시거부가 함께 있으나, 실제 중심은 위계질서 훼손과 지시거부라 `misconduct` 쪽으로 기울였음.
- `id_31465`
  - 교육과 직무평가가 반복되며 개선 여부를 보는 구조라 `work_ability`를 유지.

## rejection vs termination 판단이 애매했던 사례
- `id_29589`, `id_29941`, `id_30401`, `id_30453`, `id_31583`, `id_31609`
  - 시용기간 중 중도 종료이므로 `probation_termination`으로 분류.
- `id_30723`, `id_30757`, `id_3077`, `id_30827`, `id_31321`, `id_31653`
  - 수습 만료 시점의 정규직 전환 거부 구조라 `rejection_of_regular_employment`로 유지.
- `id_30881`
  - 수습기간 경과 후의 일반해고라 `dismissal`로 이동.

## 비수습/노이즈 처리 사례
- `id_30839`, `id_30977`, `id_31313`, `id_29883`
  - 수습 태그가 있으나 실질은 기간만료/갱신기대권 사건이라 `renewal_stage` 또는 `fixed_term`로 이동시키고 `unrelated_to_probation` 부여.
- `id_30885`, `id_31209`, `id_31243`, `id_31331`
  - 수습보다 일반 징계해고 또는 일반해고 프레임이 중심이라 `regular`로 보정.

## enum 밖 값 또는 v1 공백이 필요했던 사례
- `id_30885`, `id_31243`
  - 근로자성 판단이 선결쟁점이라 `worker_status`를 primary로 쓰고 싶었으나 v1 공백이라 secondary/notes로 흡수.
- `id_30839`, `id_31799`
  - 전환 기대권/갱신 기대권이 섞여 있으나 현 v1에서는 `renewal_expectation`으로 포괄 처리.

## v1 유지 가능 규칙
- 수습 만료 시 정규직 전환 거부는 `rejection_of_regular_employment`, 시용기간 중 중도 해고는 `probation_termination`으로 구분하는 원칙은 계속 유효함.
- 평가점수가 있어도 실제 결론이 업무적격성 종합판단이면 `work_ability` 우선이 안정적임.
- 수습 태그가 붙어 있어도 실질이 계약만료/갱신기대권이면 `unrelated_to_probation`과 함께 다른 단계로 이동시키는 것이 맞음.

## v1.1 후보 제안
- `worker_status` 선결사건이 probation 배치에 반복 혼입되므로, 장기적으로는 primary enum 승격을 다시 검토할 필요가 있음.
- 전환기대권과 갱신기대권을 보다 세밀하게 나눌 필요가 있으나, 현재 v1 범위에서는 `renewal_expectation`으로 유지 가능.
