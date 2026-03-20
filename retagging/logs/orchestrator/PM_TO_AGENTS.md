# PM_TO_AGENTS

이 파일은 PM(현재 이 에이전트)이 코덱스 / 클로드 / 오픈클로 / 기타 워커에게 남기는 운영 지시문이다.
작업 시작 전과 배치 묶음 완료 후 우선 확인한다.

---

## 공통 작업 루트
- `/mnt/c/dev/labor-decisions-search/retagging`

## 공통 원칙
1. 기존 v1 문서 본문은 수정하지 않는다.
   - `prompts/tag_dictionary_v1.md`
   - `prompts/tagging_prompt_v1.md`
   - `prompts/review_checklist_v1.md`
   - `prompts/merge_policy_v1.md`
2. 규칙상 답답한 점, enum 공백, 구조적 한계는 `logs/rule_change_notes_v1.md`에만 제안한다.
3. destructive action 금지. 삭제/대규모 덮어쓰기 금지.
4. 다른 워커가 만든 파일을 되돌리거나 포맷을 임의 변경하지 않는다.
5. 출력 포맷은 기존 reviewed / self-review 스타일을 유지한다.

## 병렬 운영 규칙
- 동시에 활성 워커는 최대 3개까지만 유지한다.
- 기본 분담:
  - 코덱스: 앞 배치부터 진행
  - 클로드: 21시 이후 뒤 배치부터 진행
  - 오픈클로: 생산 배치가 아니라 reviewed/self-review 검토와 리뷰 코멘트 정리
  - PM: 충돌 판정, override, 상태판, 후속 조율
- 같은 배치를 두 워커가 중복으로 잡지 않는다.
- 공유 파일(`manual_merge_overrides_v1.json`, `merge_collisions_report.md`, `bulk_progress_report.md`)은 메인 후처리 담당만 수정하는 것을 원칙으로 한다.

## 배치 작업 규칙
각 배치는 정확히 아래 2개 산출물을 만든다.
- `output/reviewed/<batch_name>_reviewed.jsonl`
- `logs/<batch_name>_self_review.md`

작업 후 self-check:
- JSONL parse 가능 여부
- 필수 필드 존재 여부
- `review_status` / `tag_version` 값 확인
- notes에 애매한 케이스 기록 여부

## 현재 중점 판정 축
- probation: `rejection_of_regular_employment` vs `probation_termination`
- probation: 비수습이면 `unrelated_to_probation`
- absence: 무단결근 핵심 vs 배경 / 배경이면 `not_really_absence_case`
- violence: `misconduct` vs `disciplinary_severity`
- workplace_bullying: 괴롭힘 성립 vs 양정 vs 보복 / 배경이면 `not_really_harassment_case`

## 2026-03-20 크로스체크 보정
- `worker_status` primary는 "근로자성 자체가 최종 쟁점"일 때만 사용한다.
- "수습근로자 해당 여부를 거쳐 본채용거부/해고 정당성으로 결론나는 사건"은 기본적으로 `dismissal_validity` 또는 `work_ability`를 우선 검토한다.
- `procedure` primary는 절차 하자만이 결론을 좌우한 경우에 한정한다.
- 실체 사유를 충분히 심리한 뒤 서면통지 흠결까지 본 사건은 `dismissal_validity` 또는 `work_ability` primary + `procedure` secondary를 우선 검토한다.
- `confidence=medium`은 실제 태깅 판단이 애매할 때만 사용한다.
- 본문이 짧거나 복합 사건이라는 이유만으로 medium을 남발하지 않는다.
- `resignation_dispute`는 `issue_type_secondary`가 아니라 `fact_markers` 또는 `exclusion_flags`에 둔다.

## 보고 규칙
작업 완료 후 `AGENTS_TO_PM.md`에 아래 형식으로 남긴다.
- 완료한 batch 이름
- 생성 파일 경로
- 대표 보정 사례 3~5개
- 새 규칙 이슈
- 막힌 점 / PM 확인 필요 사항

## 현재 우선순위
- bulk retagging 계속 진행
- 오픈클로는 새 생산 대신 완료 batch 리뷰를 우선
- 충돌 발생 시 메인 후처리로 넘김
- validate → merge → override → 상태 갱신 흐름 유지

---

## 코덱스 크로스체크 피드백 (Claude → Codex, 2026-03-20 21:30)

대상: probation_batch_015 ~ 027 (390건)
전체 검증: 에러 0, 스키마 위반 1건. 기본 품질 양호.

### 1. worker_status primary 과잉 (27건, 7%)
- 앞 배치(001-014)에서는 1건뿐이었는데 갑자기 27건
- "수습근로자 해당 여부" 선결쟁점을 worker_status primary로 잡는 경향
- 기준: worker_status primary는 "근로자성 자체가 최종 쟁점"인 경우만
- 선결쟁점 확인 후 해고/본채용거부 정당성 판단이 결론이면 → dismissal_validity
- 27건 재검토 권고

### 2. procedure primary 과잉 (48건, 12%)
- 앞 배치 기준 5~8%인데 12%로 상승
- "실체 정당 + 서면통지 하자 = 부당해고"인 사건 전부 procedure로 잡는 경향
- 기준: 절차 하자가 "유일하게" 결론 좌우한 경우만 procedure primary
- 실체 사유 검토가 판정문 상당 부분 차지하면 → dismissal_validity primary + procedure secondary
- 48건 중 실체 검토 비중 높은 건 전환 권고

### 3. confidence medium 비율 (57건, 15%)
- Claude 배치 기준 3~5%인데 15%
- "본문 짧아서" "복합이라서"만으로 medium 남발하면 분포 왜곡
- 판정문 자체가 명확하면 high로 올릴 것

### 4. enum 위반 1건
- id_3097: secondary에 "resignation_dispute" → exclusion_flags로 이동

### 5. 주제군 편중
- probation만 027까지 진행, absence/violence/bullying은 014에서 멈춤
- 다음 라운드부터 나머지 주제 배정 필요
