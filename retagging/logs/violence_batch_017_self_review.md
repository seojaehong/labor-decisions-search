# violence_batch_017_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 입력: 30건 (violence 배치)
- 출력: 30건 reviewed
- 핵심 판단 축: misconduct vs disciplinary_severity

## primary 분류 통계
| issue_type_primary | 건수 | case_id |
|---|---|---|
| misconduct | 10 | id_26013, id_2631, id_26329, id_26477, id_26557, id_26615, id_26721, id_26787, id_26849, id_26961 |
| disciplinary_severity | 13 | id_26071, id_26181, id_26203, id_26415, id_26455, id_26503, id_26589, id_26711, id_269, id_26797, id_26863, id_26955, id_26957 |
| unfair_treatment | 2 | id_26205, id_26357 |
| procedure | 2 | id_26343, id_26875 |
| absence_without_leave | 1 | id_26221 |
| renewal_expectation | 1 | id_2629 |
| dismissal_validity | 1 | id_27007 |

## misconduct vs disciplinary_severity 판단 기준
- **misconduct**: 비위행위 자체가 중대하여 징계사유의 존부가 핵심 쟁점이거나, 사유·양정·절차 모두 정당 판정
  - 예: 야구방망이 폭행(id_26721), 아동 폭행(id_2631), 반복비위+신뢰파괴(id_26329, id_26849, id_26961)
- **disciplinary_severity**: 징계사유는 인정되나 양정 과다 여부가 핵심 판단
  - 예: 우발적 폭행 해고 과다(id_26181, id_26415), 소급징계(id_26589), 폭언에 해고(id_269)

## 배치 오분류 교정 (violence 배치이나 실질 쟁점이 다른 건)
- **id_26221**: 실질 쟁점 = 무단결근 (폭행·겁박은 근로자의 결근 정당화 주장으로만 등장)
- **id_2629**: 실질 쟁점 = 갱신기대권 (폭언·괴롭힘은 갱신거절 사유)
- **id_26205**: 실질 쟁점 = 부당노동행위 (폭행/협박 주장이 사용자측이었으나 불인정)
- **id_26503**: 실질 쟁점 = 근무태만/수면 (폭행은 과거 비교사례에서만 언급)
- **id_26875**: 실질 쟁점 = 제척기간 도과 (폭행은 직접 쟁점 아님)
- **id_27007**: 실질 쟁점 = 사직서 진정성립/해고 부존재

## disposition_type 보정
- legacy sanction_type에 "dismissal"이었으나 실제 처분이 정직·감봉·강등인 건은 실제 처분으로 교정
  - id_26477: sanction_type=dismissal → disposition_type=suspension (출근정지 20일)
  - id_26071: sanction_type=suspension → disposition_type=pay_cut (감봉 3개월)
  - id_26849: sanction_type=pay_cut → disposition_type=disciplinary_dismissal (정년 만료로 다툴 실익 없으나 원래 징계해고)

## 주요 개별 건 메모

### id_26013 — misconduct
- 대표 폭행 + 형사처벌 확정. 징계권 불행사 신뢰 부정. 비위 자체가 중대하여 misconduct.

### id_26181 — disciplinary_severity
- 형사처벌 확정이지만 우발적+비직접 가담. 양정 비례성이 핵심 → disciplinary_severity.

### id_26343 — procedure
- 폭행 사유는 인정되나 노측위원 미참석 징계위 개최로 절차위반이 결정적 하자 → procedure.

### id_26357 — unfair_treatment
- 정당한 쟁의행위를 징계사유로 삼은 것이 핵심. 폭언 견책만 정당. 불이익취급 인정.

### id_26955 — disciplinary_severity
- 술자리 주선 → 성범죄 발생이나 직접 가담 아님. 간접 책임에 면직은 과다. 사실관계 특수.

### id_26957 — disciplinary_severity
- 성희롱+폭행+당직비부당수령+업무태만. 복합이지만 징계이력 없어 해고 과다.

## confidence 분포
- high: 29건
- medium: 1건 (id_26875 — 제척기간 도과 사건, violence와 무관하여 태깅 확신도 낮음)
