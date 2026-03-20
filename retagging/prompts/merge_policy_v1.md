# merge_policy_v1

reviewed 샘플 배치들을 `merged` 산출물로 전환하기 위한 현재 기준 문서.

목적:
- `tag_dictionary_v1.md`와 reviewed JSONL을 유지한 상태에서
- **v1.1 후보를 반영하지 않고**
- 현재 v1 기준으로 어떻게 병합할지 명확히 정한다.

적용 범위:
- `/mnt/c/dev/labor-decisions-search/retagging/output/reviewed/*.jsonl`
- 현재 우선순위 5개 주제군 reviewed 파일:
  - `probation_sample_reviewed.jsonl`
  - `violence_sample_reviewed.jsonl`
  - `absence_sample_reviewed.jsonl`
  - `incompetence_sample_reviewed.jsonl`
  - `workplace_bullying_sample_reviewed.jsonl`

---

## 1. merge 대상 파일 범위

### 포함 대상
- `output/reviewed/*_reviewed.jsonl`
- 각 reviewed 파일은 line-delimited JSON(JSONL) 형식이어야 함
- 각 레코드는 최소한 아래 필드를 가져야 함:
  - `case_id`
  - `issue_type_primary`
  - `review_status`
  - `tag_version`

### 제외 대상
- `output/draft/` 하위 파일
- `logs/` 하위 self-review 메모
- `rule_change_notes_v1.md` 등 정책 제안 문서
- enum validation 실패 레코드
- JSON 파싱 실패 레코드

원칙:
- merged는 **reviewed만을 입력 소스**로 삼는다.
- draft를 직접 merged에 넣지 않는다.

---

## 2. case_id 중복 처리 원칙

병합의 기본 키는 `case_id`다.

### 2-1. 중복이 없을 때
- 그대로 merged에 포함한다.

### 2-2. 동일 `case_id`가 여러 reviewed 파일에 있을 때
- 자동 merge 후보와 수동 검토 대상을 분리한다.
- 먼저 동일 `case_id` 레코드들을 모두 모아 충돌 필드 여부를 점검한다.

### 2-3. 자동 병합 허용 전제
아래 조건을 모두 만족할 때만 자동 병합 후보로 본다.
- `issue_type_primary`가 동일
- `employment_stage`가 동일
- `disposition_type`이 동일하거나, 정렬 기준으로 완전히 같은 집합
- `tag_version`이 동일(`v1`)
- `review_status`가 모두 `reviewed`

### 2-4. 자동 병합 금지 조건
아래 중 하나라도 해당하면 자동 병합 금지, 수동 검토로 보낸다.
- `issue_type_primary` 충돌
- `employment_stage` 충돌
- `disposition_type` 충돌
- 한쪽은 `no_formal_disposition`, 다른 쪽은 `dismissal`/`disciplinary_dismissal` 등 실질 처분 충돌
- probation 관련 사건에서 `probation_termination` vs `rejection_of_regular_employment` 충돌
- `review_status`가 `reviewed`가 아닌 항목 혼입

---

## 3. union 가능한 필드

중복 `case_id`의 reviewed 레코드가 자동 병합 조건을 만족할 때, 아래 필드는 **union 후보**로 본다.

### union 가능 필드
- `issue_type_secondary`
- `fact_markers`
- `legal_focus`
- `exclusion_flags`
- `include_for_queries`
- `exclude_for_queries`

### union 규칙
- 중복 제거 후 배열로 유지
- 정렬은 아래 우선순위를 권장:
  1. 사전 정의 enum 순서 유지(가능하면)
  2. 그 외 문자열은 사전식 정렬
- 빈 배열은 허용
- union 결과가 과도하게 넓어지는 경우 수동 검토로 전환 가능

### union 비권장 필드
아래 필드는 단순 union하지 않는다.
- `summary_short`
- `holding_summary`
- `retrieval_note`
- `notes`

이 필드들은 대표값 선택 또는 수동 검토 대상이다.

---

## 4. 수동 검토가 필요한 핵심 충돌 필드

다음 필드는 merged 단계에서 **핵심 충돌 필드**로 본다.

### 반드시 수동 검토
- `issue_type_primary`
- `employment_stage`
- `disposition_type`

### 높은 우선순위의 수동 검토 권장
- `confidence`
- `industry_context`
- `summary_short`
- `holding_summary`
- `retrieval_note`

### 이유
- `issue_type_primary`: 검색 진입점 자체를 바꾸므로 자동 결정 금지
- `employment_stage`: 사건 구조를 바꾸므로 자동 결정 위험 큼
- `disposition_type`: 처분 성격이 달라지면 검색 결과 오염 가능
- `confidence`: 병합 과정에서 과도한 high 유지 위험 존재
- `industry_context`: 추정 기반인 경우 충돌 가능

---

## 5. reviewed 우선순위 규칙

### 기본 우선순위
1. `review_status = reviewed`
2. 동일 case_id에서 더 구체적이고 모순이 적은 레코드
3. self-review 메모에서 수정 근거가 명확한 레코드
4. confidence가 더 보수적인 레코드(동률이면 notes가 더 충실한 쪽)

### primary 충돌 시
- 자동 병합 금지
- self-review 메모를 먼저 확인
- 그래도 해결되지 않으면 merged 보류 목록으로 이동

### confidence 우선순위 정책
- `reviewed`끼리 병합할 때 confidence는 무조건 high를 택하지 않는다.
- 권장 정책:
  - 하나라도 `medium`이면 merged는 `medium` 우선 검토
  - 하나라도 `low`이면 수동 검토 대상
- 원칙: 병합은 confidence를 올리는 과정이 아니라 **보수적으로 유지하는 과정**이다.

### review_status 우선순위 정책
- merged 입력은 원칙적으로 모두 `reviewed`
- `pending`이 섞인 경우:
  - 자동 병합 금지
  - 해당 case_id 전체를 보류

---

## 6. notes 권장 조건

merged 레코드의 `notes`는 항상 길 필요는 없지만, 아래 경우에는 남기는 것을 권장한다.

### notes 권장 작성 조건
- 중복 source 2개 이상을 병합한 경우
- primary 후보가 둘 이상이었으나 하나를 선택한 경우
- `employment_stage` 또는 `disposition_type` 경계가 있었던 경우
- union 결과 exclusion이 추가된 경우
- confidence를 보수적으로 낮춘 경우
- v1 enum 공백 때문에 `other` 등으로 흡수한 경우

### notes에 적을 내용 예시
- 왜 해당 primary를 유지했는지
- 어떤 필드를 union했는지
- 어떤 source를 대표본으로 삼았는지
- 왜 수동 검토가 필요했는지 / 혹은 해소됐는지

---

## 7. merged 산출물 구조

권장 파일:
- `output/merged/merged_sample_v1.jsonl`

각 레코드는 reviewed 구조를 유지하되, 아래 원칙을 따른다.

### 유지 필드
- `case_id`
- `case_name`
- `summary_short`
- `holding_summary`
- `retrieval_note`
- `employment_stage`
- `issue_type_primary`
- `issue_type_secondary`
- `disposition_type`
- `fact_markers`
- `legal_focus`
- `industry_context`
- `exclusion_flags`
- `include_for_queries`
- `exclude_for_queries`
- `confidence`
- `notes`
- `review_status`
- `tag_version`

### merged 단계 권장값
- `review_status`: `reviewed` 유지
  - 현재 v1에는 별도 `merged` status가 없으므로 새 enum을 만들지 않는다.
- `tag_version`: `v1`

### merged 레코드 작성 원칙
- 대표 source 1개를 base로 삼고
- union 가능 필드만 합친다.
- 충돌 필드는 수동 확정 후 기록한다.

---

## 8. merge 후 남겨야 할 로그/리포트

병합 후 아래 로그를 남기는 것을 권장한다.

### 필수 로그/리포트
- `logs/merge_report.md`
- `logs/validation_report.md`

### merge_report.md에 포함할 내용
- 입력 파일 목록
- 총 입력 레코드 수
- 고유 `case_id` 수
- 중복 `case_id` 수
- 자동 병합 수
- 수동 검토 필요 수
- 보류 수
- merged 산출물 파일명

### validation_report.md에 포함할 내용
- JSON 파싱 실패 여부
- enum validation 실패 건수
- 필수 필드 누락 건수
- `issue_type_primary` 충돌 목록
- `employment_stage` 충돌 목록
- `disposition_type` 충돌 목록
- confidence 하향 조정 건수

### 선택 로그
- `logs/merge_conflicts_v1.md`
  - case_id별 충돌 상세 기록
- `logs/merge_decisions_v1.md`
  - 수동 확정 근거 기록

---

## 9. reviewed 5개 배치 병합 전략

현재 reviewed 5개 배치에 대해서는 아래 전략을 적용한다.

### 자동 병합 금지 항목
- `issue_type_primary` 충돌 시 자동 병합 금지

### 수동 검토 필수 항목
- `employment_stage` 충돌
- `disposition_type` 충돌

### union 후보 항목
- `issue_type_secondary`
- `fact_markers`
- `legal_focus`
- `exclusion_flags`

### review_status / confidence 정책
- `review_status`는 모두 `reviewed`만 merge 입력 허용
- `confidence`는 더 공격적인 값이 아니라 더 보수적인 값 우선
  - high + medium → medium 우선 검토
  - medium + low → low 또는 수동 검토

---

## 10. 병합 실행 순서 권장

1. 입력 reviewed 파일 목록 확정
2. JSON 파싱 검증
3. enum 검증
4. `case_id` 기준 그룹핑
5. 자동 병합 가능/불가 분류
6. union 가능 필드 병합
7. 핵심 충돌 필드 수동 검토
8. merged JSONL 작성
9. merge_report / validation_report 기록

---

## 11. 현재 기준의 운영 원칙 요약

- draft는 merge하지 않는다.
- reviewed만 merge한다.
- primary 충돌은 자동 병합 금지다.
- stage / disposition 충돌은 수동 검토다.
- secondary / markers / legal / exclusion은 union 후보다.
- confidence는 보수적으로 간다.
- v1 공백은 문서 수정이 아니라 로그로 남긴다.
