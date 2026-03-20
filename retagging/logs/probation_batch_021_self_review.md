# probation_batch_021 Self-Review

## 배치 개요
- 입력: `C:/dev/labor-decisions-search/retagging/input/batches/probation_batch_021.jsonl` (30건)
- 출력: `C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_021_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `dismissal_validity`: 11건
- `work_ability`: 7건
- `procedure`: 4건
- `renewal_expectation`: 3건
- `worker_status`: 3건
- `absence_without_leave`: 1건

## 수습 vs 비수습 분류
- 수습(probation): 24건
- 비수습 또는 전환/만료 사건: 6건

## confidence 낮춘 사례
- `id_34645`: dismissal_validity / ['rejection_of_regular_employment'] - 불친절이나 조직 화합 저해 사유가 추상적이라 객관적 입증 부족이 핵심.
- `id_34667`: dismissal_validity / ['dismissal'] - 수습기간 도과 뒤 옛 평가를 근거로 종료해 probation이 아니라 regular dismissal로 봄.
- `id_346795`: renewal_expectation / ['nonrenewal'] - 갱신이 사용자 재량으로 설계돼 있어 갱신기대권이 인정되지 않는 구조.
- `id_346855`: renewal_expectation / ['nonrenewal'] - 정규직 전환 기대와 갱신 관행이 핵심인 기간제 갱신기대권 사건.
- `id_346951`: dismissal_validity / ['no_formal_disposition'] - 품질팀장 면담만으로는 인사권자에 의한 해고의사표시로 보기 어려움.
- `id_34715`: renewal_expectation / ['nonrenewal'] - 계약 갱신 관행과 관리과장 계속근무 사실이 갱신기대권을 뒷받침.

## 주요 경계 사례
- `id_346787`: 실제론 해고 부존재/사직서 제출 구조라 `dismissal_validity` + `no_formal_disposition`으로 정리했다.
- `id_347151`: 시용성보다 기간제 계약만료와 근로자성 판단이 앞서 `worker_status` + `contract_termination`으로 정리했다.
- `id_347213`: 사용자 적격과 본채용 거부 존재는 인정되나 구두 통지로 절차 하자가 발생한 사례로 봤다.
- `id_347271`: 무기계약 전환 이후에도 확정적 해고의사표시가 없어 해고 부존재로 정리했다.
- `id_347379`: 본채용 거부 사유의 서면통지가 없어 절차 중심으로 정리했다.

## 검증 사항
- review_status: 전건 `pending`
- tag_version: 전건 `v1`
- 필수 필드 19개 전부 포함
- JSONL 형식으로 전수 생성

## 메모
- 평가점수와 업무적격성 문구가 강한 사건은 `work_ability`로, 서면통지와 절차가 핵심이면 `procedure`로 분리했다.
- 계약만료 또는 무기계약 전환 사건은 probation 노이즈를 줄이기 위해 `fixed_term` / `renewal_stage` / `worker_status`로 보정했다.
- 무단결근, 정류장 무정차, 사직서 제출, 노조 관련 주장처럼 실질 쟁점이 다른 사건은 `misconduct`, `absence_without_leave`, `no_formal_disposition`, `unfair_treatment`로 분기했다.
