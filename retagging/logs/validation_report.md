# validation_report

## 1. 개요
- 작업 목적: merge 전 reviewed 입력의 형식/enum/중복/충돌 상태를 검증
- 기준 문서:
  - `prompts/merge_policy_v1.md`
  - `prompts/validation_merge_checklist_v1.md`
- 작업 루트: `/mnt/c/dev/labor-decisions-search/retagging`

## 2. 검증 대상 파일
- `output/reviewed/probation_sample_reviewed.jsonl`
- `output/reviewed/violence_sample_reviewed.jsonl`
- `output/reviewed/absence_sample_reviewed.jsonl`
- `output/reviewed/incompetence_sample_reviewed.jsonl`
- `output/reviewed/workplace_bullying_sample_reviewed.jsonl`

## 3. 형식 검증
- JSON parse 실패 건수: 0
- 필수 필드 누락 건수: 0
- `review_status != reviewed` 건수: 0
- `tag_version != v1` 건수: 0

## 4. enum 검증
### 4-1. primary / stage / disposition
- `issue_type_primary` enum 실패 건수: 0
- `employment_stage` enum 실패 건수: 0
- `disposition_type` enum 실패 건수: 0

### 4-2. 배열형 필드 enum 검증
- `issue_type_secondary` enum 실패 건수: 0
- `fact_markers` enum 실패 건수: 0
- `legal_focus` enum 실패 건수: 0
- `exclusion_flags` enum 실패 건수: 0

### 4-3. enum 실패 상세
| case_id | field | invalid value | source file | 조치 |
|--------|-------|---------------|-------------|------|
| 없음 | - | - | - | - |

## 5. case_id 중복 검증
- 총 `case_id` 수: 100
- 고유 `case_id` 수: 84
- 중복 `case_id` 수: 15

### 중복 상세
| case_id | source file 수 | source 목록 | 자동 병합 후보 여부 |
|--------|----------------|-------------|----------------------|
| id_10051 | 2 | absence, workplace_bullying | 아니오 |
| id_10075 | 2 | violence, workplace_bullying | 아니오 |
| id_10207 | 2 | absence, violence | 아니오 |
| id_10419 | 2 | incompetence, probation | 아니오 |
| id_10555 | 2 | absence, workplace_bullying | 아니오 |

## 6. 핵심 충돌 필드 검증
### 6-1. `issue_type_primary` 충돌
| case_id | source A | source B | 충돌 값 | 메모 |
|--------|----------|----------|---------|------|
| id_10075 | violence | workplace_bullying | workplace_harassment vs disciplinary_severity | 수동 판정 반영 |
| id_10555 | absence | workplace_bullying | workplace_harassment vs misconduct | 수동 판정 반영 |

### 6-2. `employment_stage` 충돌
| case_id | source A | source B | 충돌 값 | 메모 |
|--------|----------|----------|---------|------|
| 없음 | - | - | - | - |

### 6-3. `disposition_type` 충돌
| case_id | source A | source B | 충돌 값 | 메모 |
|--------|----------|----------|---------|------|
| id_10207 | absence | violence | dismissal vs disciplinary_dismissal | 수동 판정 반영 |
| id_10051 | absence | workplace_bullying | dismissal vs disciplinary_dismissal | 수동 판정 반영 |
| id_10555 | absence | workplace_bullying | dismissal vs disciplinary_dismissal | 수동 판정 반영 |

## 7. confidence / notes 검증
- confidence 하향 조정 필요 후보 수: 1
- notes 작성 권장 후보 수: 15

### 후보 상세
| case_id | 사유 | 권장 조치 |
|--------|------|-----------|
| id_10051 | 중복 source 병합 + disposition 수동 확정 | notes 유지 |
| id_10075 | primary 수동 확정 | notes 유지 |
| id_10207 | disposition 수동 확정 | notes 유지 |
| id_10419 | industry_context 수동 확정 | notes 유지 |
| id_10555 | 복합 충돌 수동 확정 | notes 유지 |

## 8. merge 입력 적합성 판단
- 즉시 merge 가능한 레코드 수: 79
- 수동 검토 후 merge 가능한 레코드 수: 5
- 보류 권장 레코드 수: 0

## 9. 요약
- 형식 검증 결과: 이상 없음
- enum 검증 결과: 이상 없음
- 중복/충돌 상태 요약: 총 5건의 중복 충돌이 있었고 모두 수동 판정으로 해소 가능
- merge 실행 전 필수 조치: 수동 판정 5건을 병합 정책에 따라 반영

## 10. 후속 메모
- Claude Code / 스크립트 자동화 연결 포인트: 중복 감지 및 union은 자동화 가능, 핵심 충돌 필드는 수동 훅 필요
- 추가 batch 유입 전까지 유지할 기준: 현재 merged_sample_v1.jsonl을 샘플 merged 기준본으로 유지
- 사람이 최종 판단해야 할 필드: `issue_type_primary`, `employment_stage`, `disposition_type`, 대표 summary/retrieval_note 선택
