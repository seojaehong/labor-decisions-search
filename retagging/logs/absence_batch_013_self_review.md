# absence_batch_013_reviewed.jsonl 1차 self-review 메모

## 배치 요약
- 총 30건 처리
- 무단결근 핵심 사례: 13건
- 무단결근 배경(not_really_absence_case): 14건
- 경계 사례: 3건 (id_21181, id_21533, id_21595)

## 핵심 absence 사례 (exclusion_flags 없음, absence_without_leave 또는 attendance가 primary)

| case_id | primary | 결근 유형 | 판정 |
|---------|---------|-----------|------|
| id_20947 | absence_without_leave | 근무지 반복 이탈 | 정직30일 정당 |
| id_20949 | absence_without_leave | 노선변경 거부 후 3개월+ 무단결근 | 해고 정당 |
| id_2129 | absence_without_leave | 병가 후 5일+ 무단결근 | 해고 정당 |
| id_21305 | absence_without_leave | 19일 무단결근+근무지 이탈 | 해고 정당 |
| id_21319 | absence_without_leave | 평가거부 후 무단결근 | 해고 정당 |
| id_21369 | absence_without_leave | 무단결근+수입금 미납 | 감봉 정당 |
| id_21415 | attendance | 반복 무단지각 | 해고 정당 |
| id_21523 | absence_without_leave | 폭행+14일 무단결근 | 해고 정당 |
| id_21633 | absence_without_leave | 전직발령 불응 28일 결근 | 정직3월 정당 |
| id_21651 | absence_without_leave | 42일 무단결근 | 해고 정당 |
| id_21797 | absence_without_leave | 교통사고 후 69일 결근(휴직 미신청) | 해고 정당 |
| id_21805 | absence_without_leave | 80일 무단결근 | 해고 정당 |

## 양정 과다 but absence 관련 (결근이 인정된 사유이나 결론은 부당)

| case_id | primary | 비고 |
|---------|---------|------|
| id_2105 | disciplinary_severity | 근태불량 전체가 사유이나 15년 무징계 → 양정 과다 |
| id_21595 | disciplinary_severity | 무단이탈 인정되나 양정 과다+절차 하자 |

## not_really_absence_case 판정 (14건)

| case_id | primary | 실질 쟁점 | 사유 |
|---------|---------|-----------|------|
| id_20917 | dismissal_validity | 수습 본채용거부 평가 합리성 | 근태불량은 3개 사유 중 하나 |
| id_21035 | disciplinary_severity | 보직해임+징계해고 양정 | 무단결근은 당연퇴직 부분에서만 등장 |
| id_21087 | disciplinary_severity | 성희롱(근로자1)+양정(근로자2) | 2인 복합 사건 |
| id_21117 | dismissal_validity | 해고 존부(사직 vs 해고) | 무단결근은 발단 |
| id_21165 | dismissal_validity | 수습 본채용거부 | 폭행+결근+평가미달 복합 |
| id_21183 | disciplinary_severity | 운송수입금 미납+양정 과다 | 결근일 운행이 사유이지 결근 자체 아님 |
| id_21185 | misconduct | 훈계의 징벌 해당 여부 | 본문에 결근 직접 등장 안함 |
| id_21287 | performance | 영업실적 전무(직무태만) | 전통적 결근이 아닌 실적 부진 |
| id_21295 | disciplinary_severity | 선거중립의무 위반 | 무단결근은 사유 철회됨 |
| id_21459 | disciplinary_severity | 성실의무 위반 | 근무지 이탈 사유 불인정 |
| id_21607 | dismissal_validity | 합의해지 여부 | 전 직장 결근 이력이 배경 |
| id_21681 | procedure | 서면통지 절차위반 | 해외근무지 이탈은 배경 |
| id_21785 | misconduct | 폭언·권한남용 | 과거 결근 경고이력만 언급 |
| id_21789 | unfair_treatment | 배차변경 부당노동행위 | 타인의 결근이 원인 |

## 경계 판단 메모

### id_21181 / id_21533 (영업직 근무태만)
- 두 건 모두 영업직이 근무시간 중 사적활동(자택/카페 체류)한 사례
- primary를 misconduct로 설정 (근로제공의무 해태/겸업 성격)
- not_really_absence_case 미부여 — 근무시간 중 부재라는 점에서 absence 검색에도 의미 있음

### id_2105 (15년 근속 근태불량)
- 근무지이탈+무단결근+연차문제 등 근태불량이 징계사유 전부
- primary를 disciplinary_severity로 (결론이 양정 과다)
- not_really_absence_case 미부여 — 사유 자체는 전부 absence 관련

### id_21595 (병원 무단이탈)
- 무단이탈+업무지시 거부가 인정된 사유
- primary를 disciplinary_severity로 (양정 과다 결론)
- not_really_absence_case 미부여 — 인정된 사유가 무단이탈

## 산업별 분포
- transport: 6건 (id_20949, id_21183, id_21369, id_21651, id_21789, id_21797)
- education: 3건 (id_21185, id_21459, id_21785)
- healthcare: 2건 (id_21305, id_21595)
- sales: 2건 (id_21181, id_21533)
- finance: 2건 (id_21287, id_21681)
- public: 2건 (id_21295, id_21319)
- service: 1건 (id_20947)
- unknown: 12건
