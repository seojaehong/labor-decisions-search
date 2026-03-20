# AGENTS_TO_PM

이 파일은 코덱스 / 클로드 / 워커가 PM에게 남기는 상태 보고용이다.
작업 시작 직전, 작업 완료 직후에 갱신한다.

---

## 템플릿

### Running
- agent:
- batch:
- started_at:
- input:
- expected_outputs:

### Done
- agent:
- batch:
- changed_files:
- reviewed_count:
- representative_cases:
- new_rule_issues:
- ambiguities_or_blockers:
- finished_at:

### Waiting / Blocked
- agent:
- reason:
- needs_from_pm:

---

## 최근 상태
- (여기에 최신 작업 상태를 append)

### Running
- agent: Codex
- batch: probation_batch_030
- started_at: 2026-03-20 21:40
- input: `input/batches/probation_batch_030.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_030_reviewed.jsonl`
  - `logs/probation_batch_030_self_review.md`

### Running
- agent: Codex
- batch: probation_batch_028
- started_at: 2026-03-20 21:16
- input: `input/batches/probation_batch_028.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_028_reviewed.jsonl`
  - `logs/probation_batch_028_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_028
- changed_files:
  - `output/reviewed/probation_batch_028_reviewed.jsonl`
  - `logs/probation_batch_028_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_36857`: 배차거부와 징계해고 정당성이 함께 문제된 수습 운전기사 사건
  - `id_37015`: 시용근로자성보다 평가 부적합이 본론이었던 본채용 거부 사건
  - `id_37669`: 부당한 인사발령과 대기발령이 함께 문제된 사건
  - `id_38001`: 근로계약관계 성립 자체가 부정된 당사자적격 사건
  - `id_38337`: 근거자료와 평가기준이 부족했던 본채용 거부 부당 사건
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- validation: 30 valid, 0 error, 0 warning
- finished_at: 2026-03-20 21:16

### Running
- agent: Codex
- batch: probation_batch_026
- started_at: 2026-03-20 21:12
- input: `input/batches/probation_batch_026.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_026_reviewed.jsonl`
  - `logs/probation_batch_026_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_026
- changed_files:
  - `output/reviewed/probation_batch_026_reviewed.jsonl`
  - `logs/probation_batch_026_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_351341`: 서면통지 흠결이 결론을 좌우한 절차 경계 사례
  - `id_351481`: 정식근로계약 후 수습 노이즈를 분리한 `procedure` 사례
  - `id_351851`: 사직서 제출과 해고 부존재가 문제된 fixed-term 경계 사례
  - `id_351871`: 갱신기대권과 갱신거절 합리성이 핵심인 renewal 사례
  - `id_35405`: regular dismissal로 보정한 징계양정 경계 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 21:12

### Running
- agent: Codex
- batch: probation_batch_027
- started_at: 2026-03-20 20:45
- input: `input/batches/probation_batch_027.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_027_reviewed.jsonl`
  - `logs/probation_batch_027_self_review.md`

### Running
- agent: Codex
- batch: probation_batch_019
- started_at: 2026-03-20 20:25
- input: `output/reviewed/probation_batch_019_reviewed.jsonl` and `logs/probation_batch_019_self_review.md`
- expected_outputs:
  - `output/reviewed/probation_batch_019_reviewed.jsonl`
  - `logs/probation_batch_019_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_019
- changed_files:
  - `output/reviewed/probation_batch_019_reviewed.jsonl`
  - `logs/probation_batch_019_self_review.md`
- reviewed_count: 30
- representative_cases:
  - `id_344209`: 복직명령으로 구제이익이 소멸한 mootness 사건
  - `id_344317`: 갱신기대권이 핵심인 renewal_stage 사건
  - `id_344509`: 근로계약 성립 자체가 부정된 pre_hire 사건
  - `id_344699`: 사용자 적격과 시용성이 결합된 worker_status 경계 사건
  - `id_344953`: 2차 시용계약과 경미한 사유만으로는 정당성이 약한 사건
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:24

### Running
- agent: Codex
- batch: probation_batch_020
- started_at: 2026-03-20 20:20
- input: `output/reviewed/probation_batch_020_reviewed.jsonl` 생성 예정
- expected_outputs:
  - `output/reviewed/probation_batch_020_reviewed.jsonl`
  - `logs/probation_batch_020_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_020
- changed_files:
  - `output/reviewed/probation_batch_020_reviewed.jsonl`
  - `logs/probation_batch_020_self_review.md`
- reviewed_count: 30
- representative_cases:
  - `id_344971`: 신고 이후 경고장과 해임 발언이 겹친 보복성 경계 사례
  - `id_345151`: 사직서 수리로 해고가 존재하지 않는 합의해지 사례
  - `id_345355`: 시용근로자 아님이 핵심인 worker_status 사례
  - `id_345271`: 갱신기대권은 인정되지만 갱신거절 합리성이 있는 renewal 사례
  - `id_346315`: 본채용 거부가 아닌 통상해고로 보아 redundancy로 정리한 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:27

### Done
- agent: Codex
- batch: probation_batch_016
- changed_files:
  - `output/reviewed/probation_batch_016_reviewed.jsonl`
  - `logs/probation_batch_016_self_review.md`
- reviewed_count: 30
- representative_cases:
  - `id_31867`: 평가 근거의 구체성 부족을 `dismissal_validity`로 정리
  - `id_32003`: 태도·민원 결합 수습해지를 `probation_termination`으로 유지
  - `id_32455`: probation 표면 태그보다 갱신기대권 구조를 우선해 `renewal_expectation`으로 보정
  - `id_32575`: at-will 조항만으로 수습 성립이 어려워 `worker_status` 경계 사례로 처리
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:16

### Done
- agent: Codex
- batch: probation_batch_017
- changed_files:
  - `output/reviewed/probation_batch_017_reviewed.jsonl`
  - `logs/probation_batch_017_self_review.md`
- reviewed_count: 30
- representative_cases:
  - `id_33379`: 사직으로 구제이익 소멸이 먼저라 merits를 얇게 처리
  - `id_33859`: `suspension + rejection_of_regular_employment` 복합 처분으로 정리
  - `id_33921`: 순수 probation보다 `pre_hire` 성격이 강한 경계 사례
  - `id_33473`, `id_34195`: `worker_status` 경계가 강한 본채용 거부 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - Claude 시작 시 뒤 배치와 중복되지 않도록 현재 front queue 완료 범위를 확인해주면 좋음
- finished_at: 2026-03-20 20:11

### Done
- agent: Codex
- batch: probation_batch_018
- changed_files:
  - `output/reviewed/probation_batch_018_reviewed.jsonl`
  - `logs/probation_batch_018_self_review.md`
- reviewed_count: 30
- representative_cases:
  - `id_343`: 본채용 미임용 통지의 구체성 부족으로 `procedure`
  - `id_34301`: 평가 자체보다 서면사유 흠결이 커서 `procedure`
  - `id_343439`: 교육현장 비위가 직접 중심이라 `misconduct`
  - `id_343783`, `id_343897`, `id_343985`: 합의해지/구제이익 소멸 중심이라 `no_formal_disposition` 계열로 정리
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:12

### Waiting / Blocked
- agent: Codex
- reason:
  - merge 재실행 결과 신규 수동 판정 대상 3건 발생
  - `id_30811`: `procedure` vs `dismissal_validity`
  - `id_30879`: `industry_context unknown` vs `service`
  - `id_32113`: `probation_termination` vs `rejection_of_regular_employment`
- needs_from_pm:
  - `merge_collisions_report.md` 검토 후 override 여부 판단

### Running
- agent: Codex
- batch: probation_batch_021
- started_at: 2026-03-20 20:23
- input: `input/batches/probation_batch_021.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_021_reviewed.jsonl`
  - `logs/probation_batch_021_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_021
- changed_files:
  - `output/reviewed/probation_batch_021_reviewed.jsonl`
  - `logs/probation_batch_021_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_346787`: 실제 해고보다 사직서 제출 구조라 `no_formal_disposition`으로 정리
  - `id_347151`: 시용보다 기간제 만료/근로자성 판단이 앞서 `worker_status`로 보정
  - `id_347213`: 본채용 거부 자체는 인정되지만 구두 통지라 `procedure`로 정리
  - `id_347379`: 서면통지 흠결이 핵심이라 절차 사건으로 분류
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:24


### Running
- agent: Codex
- batch: probation_batch_023
- started_at: 2026-03-20 20:29
- input: `input/batches/probation_batch_023.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_023_reviewed.jsonl`
  - `logs/probation_batch_023_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_023
- changed_files:
  - `output/reviewed/probation_batch_023_reviewed.jsonl`
  - `logs/probation_batch_023_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_348715`: 1, 2차 평균을 충족했는데 3차 평가만으로 뒤집은 hidden criteria 사례
  - `id_348825`: 계약만료로 구제이익이 사라진 fixed-term 경계 사례
  - `id_349175`: 채용내정 성립 후 사직 오해로 취소된 pre_hire 사례
  - `id_349463`: 의료기관 직장 내 괴롭힘과 위계질서 훼손이 직접 사유인 사례
  - `id_349395`: 갱신기대권이 없어 기간만료 종료가 정리된 renewal 사건
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:29

### Running
- agent: Codex
- batch: probation_batch_022
- started_at: 2026-03-20 20:30
- input: output/reviewed/probation_batch_022_reviewed.jsonl and logs/probation_batch_022_self_review.md
- expected_outputs:
  - output/reviewed/probation_batch_022_reviewed.jsonl
  - logs/probation_batch_022_self_review.md

### Done
- agent: Codex
- batch: probation_batch_022
- changed_files:
  - output/reviewed/probation_batch_022_reviewed.jsonl
  - logs/probation_batch_022_self_review.md
  - logs/orchestrator/AGENTS_TO_PM.md
- reviewed_count: 30
- representative_cases:
  - id_347873: 성희롱 감봉과 본채용 거부가 함께 정당화된 징계양정 사례
  - id_348049: 서면통지 미준수가 결론을 좌우한 절차 사례
  - id_348647: 채용내정 성립과 취소가 문제된 pre_hire 경계 사례
  - id_348705: 본채용 확정 뒤 해고 사유 부당성이 핵심인 regular dismissal 사례
  - id_34871: 환자 이송지연, 파손, 근무지 이탈이 결합된 수습 해고 정당 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - id_348371은 holding_points가 상태 인식만 담고 있어 source_text 기준으로 본채용 거부 부당성을 함께 반영함
  - id_348647은 채용내정 취소라 probation보다 pre_hire에 가깝게 정리함
- finished_at: 2026-03-20 20:30

### Running
- agent: Codex
- batch: probation_batch_024
- started_at: 2026-03-20 20:32
- input: `input/batches/probation_batch_024.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_024_reviewed.jsonl`
  - `logs/probation_batch_024_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_024
- changed_files:
  - `output/reviewed/probation_batch_024_reviewed.jsonl`
  - `logs/probation_batch_024_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_349575`: 본채용 거부와 부당노동행위 주장보다 평가·절차 적법성이 중심인 수습 사건
  - `id_349649`: 수습기간 비위는 일부 인정되지만 징계양정 과다와 절차 하자가 함께 문제된 사건
  - `id_350085`: 기간제 전환기대권은 인정되나 재교육 후에도 민원이 반복된 갱신 거절 사건
  - `id_350223`: 권고사직 합의와 퇴사 처리 요청으로 해고가 부존재한 사건
  - `id_350277`: 전환기대권이 인정되면서도 단기 결근과 질환 우려를 이유로 전환 거절이 정당한 사건
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:32


### Done
- agent: Codex
- batch: probation_batch_022
- changed_files:
  - `output/reviewed/probation_batch_022_reviewed.jsonl`
  - `logs/probation_batch_022_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- correction: reviewed output was rewritten to valid 30-record JSONL after an earlier malformed/null state
- reviewed_count: 30
- validation: local parser + tagging validator rerun
- finished_at: 2026-03-20 20:40


### Running
- agent: Codex
- batch: probation_batch_025
- started_at: 2026-03-20 20:45
- input: `input/batches/probation_batch_025.jsonl`
- expected_outputs:
  - `output/reviewed/probation_batch_025_reviewed.jsonl`
  - `logs/probation_batch_025_self_review.md`

### Done
- agent: Codex
- batch: probation_batch_025
- changed_files:
  - `output/reviewed/probation_batch_025_reviewed.jsonl`
  - `logs/probation_batch_025_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_350529`: 수습이 성립하지 않는 정식근로자 해고라 절차 쟁점이 핵심인 사례
  - `id_350633`: 갱신기대권은 인정되지만 갱신거절의 합리성이 있는 renewal 사례
  - `id_350887`: 폭행 사유는 인정되지만 서면통지의 구체성 결여가 문제된 사례
  - `id_351039`: 시용기간 연장 권한과 절차 하자가 본채용 거절을 무효로 만든 사례
  - `id_351167`: 반복 계약과 공사중단 조항으로 기간제 계약만료를 본 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- finished_at: 2026-03-20 20:45

### Done
- agent: Codex
- batch: probation_batch_027
- changed_files:
  - `output/reviewed/probation_batch_027_reviewed.jsonl`
  - `logs/probation_batch_027_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_36221`: 사직서 제출과 합의해지로 해고 부존재가 정리된 합의종료 경계 사례
  - `id_36337`: 상시근로자 수 판단과 수습 여부가 함께 걸린 threshold/probation 혼합 사례
  - `id_36533`: 차별시정 신청으로 probation보다 기간제 차별 판단이 앞서는 사례
  - `id_36807`: 감봉 후 본채용 거부가 문제된 징계양정 경계 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- validation: 30 valid, 0 error, 0 warning
- finished_at: 2026-03-20 20:49

---

## Claude Rear Queue Report — batch_033 (2026-03-20 21:15)

### Status: Done

| batch | 건수 | 에러 | 상태 |
|-------|------|------|------|
| absence_batch_033 | 20 | 0 | Done |
| violence_batch_033 | 17 | 0 | Done |
| workplace_bullying_batch_033 | 19 | 0 | Done |
| **합계** | **56** | **0** | |

### Representative Cases
- id_348207: 5개월 장기 무단결근 해고 정당 (absence 핵심)
- id_351665: violence 레거시 태그 오류 — 실질은 부당노동행위
- id_45889/id_45933: 동일 사업장 괴롭힘 사건 추정

### New Rule Issues
- violence 배치에 부당노동행위 사건 혼입 (legacy 태그 오류)

### Next
- batch_032 진행 예정 (absence, violence, workplace_bullying)


### Done
- agent: Codex
- batch: probation_batch_030
- changed_files:
  - `output/reviewed/probation_batch_030_reviewed.jsonl`
  - `logs/probation_batch_030_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_39293`: 근무성적 평가 미달과 서면통지 적법성이 함께 인정된 본채용 거부 사례
  - `id_39475`: 감봉 처분과 본채용 거부 논리가 결합된 경계 사례
  - `id_39945`: 사직서 제출로 해고 부존재가 정리된 사례
  - `id_400259`: 시용성이 부정되어 일반해고 서면통지 하자가 문제된 사례
  - `id_400483`: 계약기간 만료와 구제이익 소멸이 핵심인 fixed-term 사건
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- validation: local `validate_tagging_jsonl.py` 통과 완료
- finished_at: 2026-03-20 21:40

### Running
- agent: Codex
- batch: probation_batch_029
- target_files:
  - `output/reviewed/probation_batch_029_reviewed.jsonl`
  - `logs/probation_batch_029_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- status: in_progress

### Done
- agent: Codex
- batch: probation_batch_029
- changed_files:
  - `output/reviewed/probation_batch_029_reviewed.jsonl`
  - `logs/probation_batch_029_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_38361`: 구두해고와 서면통지 위반이 함께 걸린 절차 쟁점 사례
  - `id_38417`: 강요된 사직과 노조 관련 주장 혼입을 분리한 unfair_treatment 경계 사례
  - `id_38433`: 갱신기대권과 비갱신 통보가 핵심인 renewal_stage 사례
  - `id_38595`: 징계사유가 핵심인 misconduct 사례
  - `id_39135`: 정직/감봉 경력과 수습 종료가 섞인 disciplinary_severity 경계 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- validation: local `validate_tagging_jsonl.py` 통과 완료
- finished_at: 2026-03-20 21:55

### Codex Cross-Check Report — probation_batch_001_015 (2026-03-20)

#### Scope
- 대상: `probation_batch_001` ~ `probation_batch_015`
- 총량: 450건

#### Quick Counts
- `worker_status` primary: 8건
- `procedure` primary: 39건
- `confidence=medium`: 31건

#### Representative Cases
- `id_11225`: 적용대상성/5인 미만 여부가 핵심인 선결쟁점 사례로 `worker_status` primary가 무리 없이 읽힘
- `id_18475`: 수습기간 만료 후 정규직 전환 구조라 status 쟁점이 보이지만, 본안은 `dismissal_validity`로 이어지는 경계 사례
- `id_21037`: 실체 사유는 인정되나 서면통지 흠결이 결론을 좌우하는 `procedure` 중심 사례

#### Rule Issues
- 신규 enum 위반은 발견하지 못함
- `worker_status`/`procedure`/`medium`는 일부 경계 사례에서만 주의가 필요하고, 001~015 전체로 보면 즉시 보정할 정도의 구조적 이상은 없음

#### Blockers
- 없음

### Running
- agent: Codex
- batch: probation_batch_032
- target_files:
  - `output/reviewed/probation_batch_032_reviewed.jsonl`
  - `logs/probation_batch_032_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- status: in_progress

### Done
- agent: Codex
- batch: probation_batch_032
- changed_files:
  - `output/reviewed/probation_batch_032_reviewed.jsonl`
  - `logs/probation_batch_032_self_review.md`
  - `logs/orchestrator/AGENTS_TO_PM.md`
- reviewed_count: 30
- representative_cases:
  - `id_401701`: 출퇴근기록 조작이 인정된 수습 중 misconduct 사례
  - `id_401719`: 해고사유 서면통지 부재가 결론을 좌우한 procedure 사례
  - `id_402439`: 권고사직 합의로 해고 부존재가 정리된 사례
  - `id_402605`: 시용근로관계 부정이 결론을 좌우한 worker_status 사례
- new_rule_issues:
  - 없음
- ambiguities_or_blockers:
  - 없음
- validation: local `validate_tagging_jsonl.py` 통과 완료
- finished_at: 2026-03-20 22:05

---

## Claude Rear Queue Report — batch_031-032 (2026-03-20 21:50)

### Status: Done

| batch | 건수 | 에러 |
|-------|------|------|
| absence_batch_031 | 30 | 0 |
| absence_batch_032 | 30 | 0 |
| violence_batch_031 | 30 | 0 |
| violence_batch_032 | 30 | 0 |
| workplace_bullying_batch_031 | 30 | 0 |
| workplace_bullying_batch_032 | 30 | 0 |
| **합계** | **180** | **0** |

### Claude Rear Queue 전체 완료 요약
- batch_031~033: 3개 주제 × 3묶음 = 9배치, 236건
- 에러 0, 코덱스 front와 겹침 없음

### Rear queue 종료
- 코덱스가 030까지 잡았으므로 여기서 stop
