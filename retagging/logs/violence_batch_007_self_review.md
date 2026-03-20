# violence_batch_007_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, violence 배치 수록
- misconduct vs disciplinary_severity 구분 중점 검토

## 통계
| primary | 건수 |
|---------|------|
| misconduct | 15 |
| disciplinary_severity | 10 |
| transfer_validity | 2 |
| procedure | 1 |
| renewal_expectation | 1 |
| unfair_treatment | 1 |

| decision_result | 건수 |
|-----------------|------|
| dismissed (기각) | 14 |
| granted (인용) | 12 |
| upheld (초심유지) | 4 |

## misconduct vs disciplinary_severity 판단 근거

### misconduct로 태깅 (15건)
- id_16767: 이메일 명예훼손·성희롱 비위 존부 다툼, 전부 인정 → 기각
- id_16901: 협박·인신공격 문자의 비위 존부가 핵심 → 기각
- id_16911: 협박문자·악의적 고발 비위 존부 → 기각
- id_16965: 폭언·직무태만 비위 존부(일부 불인정, 대부분 인정) → 기각(초심유지)
- id_17095: 업무지시 불응·지각·협박메일 비위 존부 → 기각(초심유지)
- id_17201: 무단결근·과속운전 비위 → 기각 (violence 배치이나 폭행 직접 쟁점 아님)
- id_1725: 아동 폭행 비위 존부 → 기각
- id_17249: 음주 출근 비위 → 기각 (violence 배치이나 폭행 무관)
- id_17261: 저성과·폭행·허위고소 복합 비위 존부 → 기각
- id_17557: 폭언·업무지시 거부·이탈 비위 존부 → 기각
- id_17575: 동료 폭행·경고성 메일 비위 존부(누가 먼저 밀쳤는지) → 기각(초심유지)
- id_1767: CCTV로 부적절 보육 비위 존부 확인 → 기각
- id_17729: 반복 폭언·폭행 비위 존부 → 기각
- id_17741: 폭언·성희롱·질서문란 복합 비위 존부 → 기각

### disciplinary_severity로 태깅 (10건)
- id_16821: 쌍방폭행 인정, 합의 후 7개월 지연 해고 양정 과다 → 인용
- id_16927: 이력서 허위기재·욕설 인정, 해고 양정 과다 → 인용(초심유지)
- id_17007: 쌍방폭행 인정, 한쪽만 감경하여 형평성 위반 → 인용
- id_17171: 특수폭행(칼) 인정, 쌍방과실 형평성 위반 → 인용
- id_17247: 근무태만·폭언 인정, 우수 실적·시정 가능성 있어 양정 과다 → 인용
- id_17367: 업무지시 불이행·서류파손 인정, 사용자 폭행 선행 고려 양정 과다 → 인용
- id_17369: 욕설·질서문란 인정, 징계전력 없어 정직 1월 양정 과다 → 인용
- id_17403: 욕설·언쟁 인정, 징계전력·중대피해 없어 정직 2월 양정 과다 → 인용
- id_17535: 5개 사유 중 3개만 인정, 인정 사유 대비 해고 양정 과다 → 인용
- id_1759: 욕설·고성 인정, 해고에 이를 정도 아님 + 서면통지 위반 → 인용(초심유지)
- id_17629: 쌍방폭행 인정, 상대에게 더 큰 벌금형인데 정직 2주만 → 형평성 위반 양정 과다 → 인용

### 기타 primary로 태깅 (5건)
- id_16845: transfer_validity — 강임(직급하향)의 정당성이 핵심, 폭행은 사유 중 하나
- id_16925: unfair_treatment — 사용자의 폭언이 지배·개입 부당노동행위인지가 쟁점
- id_16953: transfer_validity — 폭행 피해자를 오히려 전보한 것의 업무상 필요성
- id_17205: procedure — 대기발령=실질 징계 → 이중징계 해당 여부가 핵심
- id_17591: renewal_expectation — 갱신기대권 존부가 핵심, 폭행은 갱신거절 사유 중 하나

## violence 배치 특이사항
- 음주 출근(id_17249), 무단결근·과속(id_17201) 등 폭행과 직접 무관한 사례 포함
- 부당노동행위(지배·개입) 사건(id_16925)은 근로자 비위가 아닌 사용자 행위가 쟁점
- 쌍방폭행 비교 징계 형평성 사례가 3건(id_17007, id_17171, id_17629)으로 패턴화 가능

## exclusion_flags 부여 건
- id_16845: not_really_harassment_case
- id_16925: unrelated_to_dismissal
- id_16953: unrelated_to_dismissal
- id_17201: not_really_absence_case
- id_17249: (없음 — 음주 출근 자체가 misconduct)
- id_17369: unrelated_to_dismissal
- id_17403: unrelated_to_dismissal
- id_17575: unrelated_to_dismissal
- id_17591: renewal_expectation_dominant
