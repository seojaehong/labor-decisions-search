# probation_batch_030 Self-Review

## 배치 개요
- 입력: `retagging/input/batches/probation_batch_030.jsonl` (30건)
- 출력: `retagging/output/reviewed/probation_batch_030_reviewed.jsonl` (30건)
- 작업일: 2026-03-20

## 분류 요약
- `disciplinary_severity`: 2건
- `dismissal_validity`: 12건
- `misconduct`: 1건
- `procedure`: 3건
- `renewal_expectation`: 2건
- `work_ability`: 10건

## 수습 vs 비수습 분류
- `probation`: 26건
- `fixed_term`: 2건
- `regular`: 2건

## rejection vs termination 구분
- `rejection_of_regular_employment`: 17건
- `dismissal`: 4건
- `probation_termination`: 1건
- `no_formal_disposition`: 4건
- `pay_cut`: 1건
- `suspension`: 1건
- `contract_termination`: 2건

## 주요 경계 사례
- `id_39293`: 근무성적 평가 미달과 서면통지 적법성이 함께 인정된 본채용 거부 사례
- `id_39475`: 감봉 처분과 본채용 거부 논리가 결합된 경계 사례
- `id_39945`: 사직서 제출로 해고 부존재가 정리된 사례
- `id_400259`: 시용성이 부정되어 일반해고 서면통지 하자가 문제된 사례
- `id_400483`: 계약기간 만료와 구제이익 소멸이 핵심인 fixed-term 사건

## 검증 사항
- 30건 전수 태깅 완료
- 필수 필드 19개 전부 포함
- `review_status`: 전건 `pending`
- `tag_version`: 전건 `v1`
- 로컬 스키마/값 검증: 30/30, 오류 0, 경고 0

## 메모
- 수습평가, 절차, 징계양정, 계약만료가 강하게 섞여 있어 primary를 먼저 분리했다.
- `unrelated_to_probation`은 실제로 probation 쟁점이 아닌 fixed-term / regular 경계에서만 제한적으로 사용했다.
- `notes`는 전건 채워 검색 맥락이 끊기지 않도록 했다.
