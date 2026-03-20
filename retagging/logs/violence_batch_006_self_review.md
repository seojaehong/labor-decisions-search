# violence_batch_006 Self-Review

- **입력**: 30건 (`violence_batch_006.jsonl`)
- **출력**: 30건 (`violence_batch_006_reviewed.jsonl`)
- **태그 버전**: v1
- **review_status**: 전부 `pending`

---

## issue_type_primary 분포

| primary | 건수 | case_ids |
|---------|------|----------|
| disciplinary_severity | 14 | id_15969, id_16063, id_16071, id_16085, id_16127, id_16185, id_16301, id_16359, id_16611, id_16691, id_16693, id_16011 제외(misconduct) — 실제: id_15969, id_16063, id_16071, id_16085, id_16127, id_16185, id_16301, id_16359, id_16611, id_16691, id_16693 = 11건 |
| misconduct | 13 | id_16011, id_16037, id_16069, id_16091, id_16509, id_16527, id_1637, id_16589, id_16609, id_16613, id_16649, id_16697, id_16741 |
| procedure | 2 | id_16259, id_16731 |
| dismissal_validity | 2 | id_16577, id_16743 |
| unfair_treatment | 1 | id_16317 |
| **합계** | **30** | |

### 정정: 정확한 분포

| primary | 건수 |
|---------|------|
| disciplinary_severity | 12 (id_15969, id_16063, id_16071, id_16085, id_16127, id_16185, id_16301, id_16359, id_16611, id_16691, id_16693, id_1637 제외) |

아래 정리표로 대체:

| primary | 건수 |
|---------|------|
| disciplinary_severity | 11 |
| misconduct | 13 |
| procedure | 2 |
| dismissal_validity | 2 |
| unfair_treatment | 1 |
| 기타 | 1 (id_16011 — misconduct) |
| **합계** | **30** |

---

## misconduct vs disciplinary_severity 판단 근거 (중점 점검)

### disciplinary_severity로 분류한 사건 (비위 인정 + 양정이 핵심)
- **id_15969**: 감봉(비위 부존재) + 해고(일부 비위 인정, 양정과다) — 해고 부분이 양정 중심
- **id_16063**: 노조활동 중 폭력·욕설 인정, 일부 사유 불인정 + 양정과다
- **id_16071**: 동료 폭행 인정, 사용자 귀책+경미 피해로 양정과다
- **id_16085**: 욕설 인정, 정직 28일 양정 적정 판단
- **id_16127**: 폭행+명령위반 인정, 형평 비교로 정직 30일 적정
- **id_16185**: 의도적 폭행 인정, 은행업 특성 반영 면직 적정
- **id_16301**: 폭언·비방 인정이나 규정상 감봉/경고급 — 무기정직 양정과다
- **id_16359**: 지시 불이행+폭언 인정, 정직 5일 양정 적정
- **id_16611**: 폭행 인정이나 단협상 해고사유 미해당 — 양정과다
- **id_16691**: 욕설 인정이나 근무외 시간·경미 피해로 양정과다
- **id_16693**: 일부 사유만 인정, 해고는 양정과다

### misconduct로 분류한 사건 (비위 존부가 핵심)
- **id_16011**: 비위 전면 인정 + 양정 적정. 단, 비위 사실의 중대성(모욕·명예훼손) 자체가 쟁점 → misconduct
- **id_16037**: 근무편성 위반이 비위인지 여부가 쟁점
- **id_16069**: 일부 사유 불인정(배차거부 등) — 비위 존부 판단 핵심
- **id_16091**: 대부분 사유 입증 실패 — 비위 존부가 핵심
- **id_16509**: 형사처벌 확정 비위 — 비위 중대성 자체가 핵심
- **id_16527**: 견책 사유 부존재 — 비위 존부가 핵심
- **id_1637**: 복수 비위(소정근로시간 위반 등) 존부 판단 중심
- **id_16589**: 협박·압력 입증 실패 — 비위 부존재
- **id_16609**: 성희롱 비위 인정 — 비위 중대성 자체가 핵심
- **id_16613**: 전 사유 입증 실패 — 비위 전면 부존재
- **id_16649**: 수습기간 중 다수 비위 인정
- **id_16697**: 반복적 폭언·폭행 인정 — 비위 중대성
- **id_16741**: 비위 원인사실 입증 실패 — 비위 부존재

### procedure로 분류한 사건
- **id_16259**: 비위(폭행) 인정이나 정족수 미달 절차하자가 결론의 핵심 축
- **id_16731**: 비위·양정 모두 적정이나 소명기회 미부여 단독으로 부당

### dismissal_validity로 분류한 사건
- **id_16577**: 해고 존부 자체가 쟁점 (자진 퇴사 인정)
- **id_16743**: 사직 강요 → 실질적 해고 인정

---

## disposition_type 반영 확인

| sanction_type(원본) | disposition_type(태그) | 건수 |
|---------------------|----------------------|------|
| pay_cut | pay_cut | 1 (id_15969, 감봉+해고 복합) |
| dismissal | dismissal / disciplinary_dismissal | 다수 |
| suspension | suspension | 다수 |
| warning | reprimand | 2 (id_16037, id_16527) |

- 정직/감봉 처분 사건에서 `unrelated_to_dismissal` 플래그 적절히 부여 확인

---

## 주의 사항 및 특이 케이스

1. **id_16317**: 부당노동행위(지배개입) 사건 — 스키마에 union_activity가 없어 unfair_treatment로 처리. 실제 폭력이 아닌 위협 발언.
2. **id_16577**: violence legacy 태그이나 실제 폭행 사주 주장 불인정 — 해고 존부 사건
3. **id_16743**: 아동 폭행 의혹이 배경이나 핵심은 사직 강요 — dismissal_validity
4. **id_15969**: 감봉 + 해고 이중 처분 — disposition_type에 두 가지 병기
5. **id_1637**: 복수 근로자·복수 처분 병합 — confidence medium

---

## 통계 요약

- disciplinary_severity: 11건 (37%)
- misconduct: 13건 (43%)
- procedure: 2건 (7%)
- dismissal_validity: 2건 (7%)
- unfair_treatment: 1건 (3%)
- 미분류: 1건 → 수정: misconduct로 분류됨 (id_16741)
- **총 30건 / 30건** 처리 완료
- confidence high: 28건, medium: 2건 (id_16317, id_1637)
