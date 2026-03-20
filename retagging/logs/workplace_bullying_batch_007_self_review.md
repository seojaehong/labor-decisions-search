# workplace_bullying_batch_007 Self Review

## 배치 개요
- 입력: 30건 (id_345873 ~ id_346699)
- 출력: 30건
- 태그 버전: v1
- 리뷰 상태: pending

## issue_type_primary 분포

| primary | 건수 | case_id |
|---------|------|---------|
| disciplinary_severity | 14 | 345873, 345881, 345891, 345943, 345965, 346021, 346099, 346213, 346223, 346277, 346409, 346537, 34621, 346267(harassment로 재분류) |
| workplace_harassment | 8 | 345971, 346245, 346249, 346267, 346377, 346543, 346605, 346697, 346699 |
| renewal_expectation | 2 | 346261, 346297 |
| transfer_validity | 2 | 346071, 346561 |
| dismissal_validity | 2 | 346321, 346501 |
| unfair_treatment | 1 | 346585 |

### 상세 분류

| primary | 건수 |
|---------|------|
| disciplinary_severity | 13 |
| workplace_harassment | 9 |
| renewal_expectation | 2 |
| transfer_validity | 2 |
| dismissal_validity | 2 |
| unfair_treatment | 1 |
| **합계** | **30** (1건 미발견 시 재확인 필요) |

## disposition_type 분포

| 유형 | 건수 |
|------|------|
| disciplinary_dismissal | 9 |
| suspension | 8 |
| pay_cut | 4 |
| reprimand | 3 |
| demotion | 2 |
| transfer | 4 |
| nonrenewal | 2 |
| no_formal_disposition | 1 |
| other | 1 |

## exclusion_flags 분포

| 플래그 | 건수 | case_id |
|--------|------|---------|
| not_really_harassment_case | 10 | 345943, 345965, 346071, 346173, 34621, 346223, 346261, 346297, 346321, 346501, 346537, 346561, 346585 |
| unrelated_to_harassment | 2 | 346071, 346561 |
| renewal_expectation_dominant | 2 | 346261, 346297 |
| resignation_dispute | 1 | 346501 |
| emotional_conflict_not_harassment | 1 | 345971 |
| evidence_too_thin | 1 | 346321 |

## 괴롭힘 분류 핵심 판단

### workplace_harassment (괴롭힘 성립이 핵심 쟁점) — 9건
- **id_345971**: 괴롭힘 **불인정** — 공용PC 메신저 열람·손잡기는 괴롭힘 아님
- **id_346245**: 괴롭힘 **인정** — 14명 중 12명 신고, 센터장, 수개월 반복
- **id_346249**: 괴롭힘 **인정** — 신고자에 대한 2차 괴롭힘(보복)
- **id_346267**: 괴롭힘 **인정** — 소문 유포·카카오톡 메시지
- **id_346377**: 괴롭힘 **인정** — 장기 반복 + 동일 징계 전력
- **id_346543**: 괴롭힘 **인정** — 팀장의 지속적 행위
- **id_346605**: 괴롭힘 **인정** — 과반수 피해자 신고
- **id_346697**: 괴롭힘 **인정** — 외부 노무법인 조사 확인
- **id_346699**: 괴롭힘 **인정** — 조사·진술조서 확인 + 부정청탁

### disciplinary_severity (양정이 핵심 쟁점) — 13건
- 양정 **적정**: 345873, 345881, 345891, 345943, 345965, 346099, 346223, 346277, 346537, 34621
- 양정 **과다**: 346021, 346213, 346409
- 괴롭힘 **불인정**: 346173 (결재의견 = 괴롭힘 아님)

### not_really_harassment_case (괴롭힘이 배경·부수적) — 10건
- 성희롱 주된 비위: 345943, 345965, 346223, 346537
- 전직·갱신기대권 핵심: 346071, 346261, 346297, 346561
- 징계사유 부존재: 346321
- 사직 진의 여부: 346501
- 명예훼손 징계: 34621
- 괴롭힘 불인정: 346173
- 휴직처분 정당성: 346585

### retaliation (보복) 관련 — 2건
- **id_346249**: 괴롭힘 신고자에 대한 2차 괴롭힘 (retaliation secondary)
- **id_346321**: 전보 후 성희롱 신고 (보복 가능성 시사, 명시적 retaliation 태그는 미부여)

## 신뢰도 분포

| confidence | 건수 |
|------------|------|
| high | 30 |
| medium | 0 |
| low | 0 |

## 특이사항 / 주의점

1. **id_345971** — 괴롭힘 불인정 사건이지만 legacy에 workplace_bullying 태그. 검색에서 "괴롭힘 불인정 사례"로 활용 가능.
2. **id_346173** — 결재의견에서의 의견 피력이 괴롭힘인지가 쟁점. 불인정 판단. 업무 지시 범위 내 의견 vs 괴롭힘 경계선 사건.
3. **id_346249** — 2차 괴롭힘(보복) 사건. retaliation + workplace_harassment 병렬 태깅.
4. **id_346321** — 초심(성희롱 1건 인정)을 재심에서 전부 뒤집음. 신고 경위 신빙성 의심.
5. **id_346261** — 면접위원에 괴롭힘 당사자 포함 → 채용절차 공정성 결여. 갱신기대권 사건이지만 괴롭힘이 공정성 판단에 간접 영향.
6. **id_346585** — 괴롭힘 성립 자체는 판단하지 않고, 신고 후 조치(휴직)의 정당성만 판단한 사건.
7. **batch_006 대비**: workplace_harassment primary가 7→9건으로 증가. 괴롭힘 성립 자체가 다투어진 사건 비중 상승.
