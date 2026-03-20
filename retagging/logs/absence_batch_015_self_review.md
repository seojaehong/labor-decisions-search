# absence_batch_015 Self-Review

## 배치 개요
- **입력**: 30건 (id_22839 ~ id_23547)
- **출력**: 30건 전량 태깅 완료
- **작업일**: 2026-03-20

## 무단결근 핵심 vs 배경 분류

### 핵심 결근 사례 (absence_without_leave / attendance가 primary) — 10건
| case_id | 요약 | primary |
|---------|------|---------|
| id_22875 | 11일 무단결근(연차 미승인), 해고 정당 | absence_without_leave |
| id_22997 | 장기 무단결근+폭행, 정직 전력 후 재범, 해고 정당 | absence_without_leave |
| id_23063 | 택시기사 42일 무단결근+운송수입금 미납, 해고 정당 | absence_without_leave |
| id_23067 | 5회 이상 무단이탈+영리겸업, 해임 정당 | absence_without_leave |
| id_23081 | 19일 무단결근이나 질병 입원 감안 양정 과다 | absence_without_leave |
| id_23187 | 반복적 결근+무단이탈+지각, 중징계 전력, 해고 정당 | absence_without_leave |
| id_23223 | 장기 무단결근+성희롱+업무태만, 해고 정당 | absence_without_leave |
| id_23373 | 무단결근+형사처벌, 정직 정당 | absence_without_leave |
| id_23381 | 버스기사 승무거부=장기 무단결근, 해고 정당 | absence_without_leave |
| id_23403 | 9개월 83회 상습 지각, 해고 정당 | attendance |

### 배경 결근 사례 (not_really_absence_case) — 20건
| case_id | 실질 primary | 배경 판단 근거 |
|---------|-------------|---------------|
| id_22839 | misconduct | 허위근태입력 지시·경력위조가 핵심, 근태불량은 부수 |
| id_22851 | procedure | 사직 vs 해고 구분·서면통지 위반이 핵심 |
| id_22873 | worker_status | 근로자성 판단이 유일 쟁점 |
| id_22913 | disciplinary_severity | 무단결근 증거 부족, 양정 과다가 핵심 |
| id_22945 | dismissal_validity | 합의해지 여부가 핵심, 무단이탈은 정황 |
| id_22955 | transfer_validity | 부당전직 → 결근 패턴 |
| id_22973 | disciplinary_severity | 쟁의행위 맥락의 복합 비위, 결근은 일부 |
| id_22983 | misconduct | 시용기간 업무적격성이 핵심, 결근 통보 누락은 부수 |
| id_23003 | disciplinary_severity | 무단촬영·업무방해가 주, 무단이탈은 부수, 양정 과다 |
| id_23027 | transfer_validity | 부당전보+부당노동행위가 핵심, 근무태만은 입증 부족 |
| id_23097 | misconduct | 근무 중 사적업무 수행이 핵심, 결근 아님 |
| id_23129 | procedure | 이사회 정족수 하자가 핵심, 무단결근은 복수 사유 중 하나 |
| id_23179 | misconduct | 시용기간 복합 비위(폭행+결근), 시용 해약권이 핵심 |
| id_23299 | dismissal_validity | 고용승계 거부 후 복직 → 구제이익 부존재 |
| id_23407 | worker_status | 근로자성 인정이 핵심, 지각 2회는 해고사유 불인정 소재 |
| id_23427 | misconduct | 겸업금지 위반·모욕이 결근과 동등 이상 비중 |
| id_23435 | dismissal_validity | 합의해지 판단이 핵심, 출근 미이행은 정황 |
| id_23509 | dismissal_validity | 해고 부존재가 핵심, 결근은 배경 사실 |
| id_23535 | work_ability | 신체장애 직무수행 불능이 핵심, 결근은 질병 수반 현상 |
| id_23547 | misconduct | 업무지시 불이행이 핵심, 결근과 무관 |

## 통계
- **핵심 결근 비율**: 10/30 = 33.3%
- **배경 결근 비율**: 20/30 = 66.7%
- **confidence**: high 29건, medium 1건 (id_23427)

## 산업 분포
- transport: 4건 (id_22983, id_23063, id_23381, id_23435)
- public: 2건 (id_22973, id_23067)
- sales: 2건 (id_22873, id_23407)
- service: 2건 (id_23027, id_23299)
- finance: 1건 (id_23097)
- education: 1건 (id_23179)
- it: 1건 (id_22839)
- unknown: 17건

## 특기사항
1. **id_23403**: 지각 83회 사례로 absence_without_leave가 아닌 attendance를 primary로 부여. 지각과 결근은 성격이 다름.
2. **id_23427**: 무단결근 11일이 주요 사유이나 겸업금지 위반·모욕이 동등 비중이어서 misconduct로 분류. confidence medium.
3. **id_22873, id_23407**: 동일하게 부동산 판매 용역의 근로자성 사례이나 결론이 반대(전자 불인정, 후자 인정).
4. **배경 비율 66.7%**: absence 레거시 태그가 붙어 있으나 실제 핵심 쟁점이 결근이 아닌 사례가 2/3. 검색 품질 향상에 기여 예상.
