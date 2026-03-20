# review_upto_batch_015

기준: `/mnt/c/dev/labor-decisions-search/retagging/output/reviewed` 내 batch 001~015 reviewed 파일 전수 스캔

## 요약
- reviewed 파일 수: 66
- reviewed 레코드 수: 1,972
- `review_status=pending` 레코드: 1,282
- confidence 분포:
  - high: 1,842
  - medium: 128
  - low: 2

## 핵심 특이값 / 이상치

### 1. enum drift가 꽤 큼
특히 absence 006~011 구간에서 v1 사전 밖 값이 반복 유입됨.

대표 사례:
- `issue_type_primary`
  - `absence_without_leave`
  - `transfer_validity`
  - `attendance`
  - `performance`
  - `other`
  - `wage_dispute`
  - `low_sales`
- `disposition_type`
  - `reprimand`
- `fact_markers`
  - `investigation_conducted`
  - `warning_given`
  - `long_tenure`
  - `sales_target_not_met`
- `legal_focus`
  - `comparative_fairness`
- `exclusion_flags`
  - `not_really_performance_case`

판단:
- 현재 v1 가이드와 실제 bulk 산출물 사이에 drift가 다시 커지고 있음.
- 특히 absence 계열에서 primary enum을 더 자유롭게 쓰는 경향이 강함.

### 2. industry_context 확장이 암묵적으로 진행됨
반복 등장:
- `education`
- `construction`
- `transport`
- `sales`
- `it`
- `retail`

판단:
- 현재 실제 산출물은 sample 단계 때보다 더 세분화된 industry_context를 쓰고 있음.
- 이건 사실상 운영 스키마가 확장된 것으로 봐야 함.

### 3. primary 분포상 disciplinary_severity 편중이 큼
상위 primary:
- disciplinary_severity: 532
- dismissal_validity: 437
- misconduct: 293
- work_ability: 163
- workplace_harassment: 111

판단:
- `disciplinary_severity` 과대포착 가능성은 계속 모니터링 필요.
- 다만 현재 merged/검색 품질 테스트 결과와 함께 보면 아직은 운영 가능 범위.

### 4. reviewed / pending 혼재
- 현재 batch 001~015 전체에 `pending`이 1,282건 존재

판단:
- 운영상 reviewed 파일명인데 review_status는 pending인 구조가 유지되고 있음.
- 이건 의도된 current workflow일 가능성이 높지만, 보고서/대시보드에서 혼동 가능.

## 우선 체크해야 할 파일군
특히 이상치가 많이 보인 파일:
- `absence_batch_006_reviewed.jsonl`
- `absence_batch_007_reviewed.jsonl`
- `absence_batch_008_reviewed.jsonl`
- `absence_batch_009_reviewed.jsonl`
- `absence_batch_010_reviewed.jsonl`
- `absence_batch_011_reviewed.jsonl`

## 대표 특이값 사례
- `id_15623` → `issue_type_primary=transfer_validity`
- `id_16487` → `issue_type_primary=absence_without_leave`, `disposition_type=reprimand`
- `id_17003` → `issue_type_primary=performance`, `exclusion_flags=not_really_performance_case`
- `id_18817` → `issue_type_primary=wage_dispute`
- `id_19435` → `issue_type_primary=low_sales`, `fact_markers=sales_target_not_met`

## 내 해석
1. batch 015까지는 파이프라인 자체는 잘 굴러가고 있음
2. 다만 absence 계열부터 v1 스키마를 벗어나는 값이 다시 늘고 있음
3. 따라서 앞으로는
   - 충돌뿐 아니라
   - enum drift 자체를 별도 모니터링해야 함
4. 코덱스 오케스트레이터가 붙으면 validate 단계에서 enum drift를 더 강하게 잡는 게 좋음

## 권장 후속 조치
- validate 단계에서 enum drift 리포트를 별도 분리
- absence 계열에 대해 primary normalization 규칙 재강화
- reviewed 파일명과 `review_status=pending` 관계를 운영상 어떻게 볼지 명시
