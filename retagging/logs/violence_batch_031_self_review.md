# violence_batch_031_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, legacy 태그: violence/misconduct 계열
- 중점 판단: misconduct vs disciplinary_severity 구분
- violence 배치이나 실질 폭행(물리적) 사안은 소수, 대부분 폭언·모욕·위협 계열

## 분류 통계

### issue_type_primary 분포
| primary | 건수 | case_id 예시 |
|---------|------|-------------|
| disciplinary_severity | 14 | id_349013, id_34905, id_349169, id_349425, id_349459, id_34953, id_349709, id_34973, id_349775, id_34987, id_34993, id_350015, id_350295, id_34931 |
| dismissal_validity | 6 | id_34915, id_349271, id_349837, id_350075, id_34903, id_349227 |
| procedure | 3 | id_349109, id_349183, id_350173 |
| misconduct | 3 | id_34919, id_350089, id_3503 |
| workplace_harassment | 2 | id_349757, id_349773 |
| worker_status | 1 | id_349273 |

### misconduct vs disciplinary_severity 판단 기준
- **misconduct (3건)**: 비위행위 자체의 중대성이 핵심, 양정 다툼 없거나 양정 적정 인정
  - id_34919: 허위사진 편집+협박+경쟁사 접촉 — 중대 기망·협박
  - id_350089: 성희롱+스토킹+협박+괴롭힘 복합 — 공소장 사실과 일치
  - id_3503: 장애인 인권침해 — 시설폐쇄 수준 중대 비위
- **disciplinary_severity (14건)**: 일부/전부 사유 인정이나 양정(해고/정직 등)의 과다 여부가 핵심 쟁점
  - 대부분 "사유는 인정되나 해고/정직까지는 과하다" 패턴

### legacy violence 태그 오분류 (실질 무관) — 4건
- id_349271: 경비원 사직 합의해지, 폭력 관련 내용 없음
- id_349837: 사직서 제출 자발성 쟁점, 폭력 무관
- id_350075: 상급자 '나가라' 발언 후 자발적 사직, 폭력 무관
- id_349273: 학원 강사 근로자성 부정, 폭력 무관

### disposition_type 분포
| type | 건수 |
|------|------|
| disciplinary_dismissal | 14 |
| suspension | 8 |
| pay_cut | 5 |
| dismissal | 4 |
| reprimand | 1 |
| rejection_of_regular_employment | 2 |
| contract_termination | 1 |
| transfer | 2 |

### decision_result 분포
| result | 건수 |
|--------|------|
| dismissed (기각) | 11 |
| granted (인용) | 8 |
| upheld (초심유지-재심) | 6 |
| overturned (초심취소-재심) | 5 |

## 개별 케이스 리뷰

## id_349013
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'procedure', 'workplace_harassment']
- exclusion_flags: ['procedure_dominant']
- 변경 이유: 8개 사유 중 2개만 인정 + 절차하자 + 양정 과다 복합

## id_34903
- primary: dismissal_validity / disposition: ['rejection_of_regular_employment', 'pay_cut']
- secondary: ['misconduct', 'disciplinary_severity']
- 변경 이유: 수습 본채용 거부가 실질 쟁점, 폭언은 징계사유 중 하나

## id_34905
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'workplace_harassment']
- exclusion_flags: ['not_really_harassment_case']
- 변경 이유: 일부 사유만 인정, 직권면직은 양정 과다

## id_349109
- primary: procedure / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'disciplinary_severity']
- exclusion_flags: ['procedure_dominant']
- 변경 이유: 사유·양정 적정이나 단체협약상 징계위원 구성 위반으로 절차하자 단독 부당

## id_34915
- primary: dismissal_validity / disposition: ['suspension']
- secondary: ['misconduct', 'workplace_harassment']
- exclusion_flags: ['not_really_harassment_case', 'evidence_too_thin']
- 변경 이유: 모든 징계사유 부존재

## id_349169
- primary: disciplinary_severity / disposition: ['reprimand']
- secondary: ['misconduct']
- exclusion_flags: ['unrelated_to_dismissal', 'unrelated_to_harassment']
- 변경 이유: 혼잣말 욕설에 견책 — 서비스업 특성 반영 경징계 적정

## id_349183
- primary: procedure / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'disciplinary_severity', 'absence_without_leave']
- exclusion_flags: ['procedure_dominant']
- 변경 이유: 폭행+무단결근 인정, 양정 적정이나 징계통지서 사유 미기재 절차하자

## id_34919
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['dismissal_validity']
- 변경 이유: 허위사진 편집+협박+경쟁사 접촉 중대 비위 — misconduct 핵심

## id_349227
- primary: dismissal_validity / disposition: ['disciplinary_dismissal', 'transfer']
- secondary: ['workplace_harassment', 'transfer_validity']
- exclusion_flags: ['not_really_harassment_case', 'evidence_too_thin']
- 변경 이유: 괴롭힘(지위 우위 불인정)+성희롱(증거 부족) 모두 불인정 → 전보도 부당

## id_349271
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion_flags: ['resignation_dispute', 'settlement_or_mutual_termination']
- 변경 이유: 사직 합의해지, violence legacy 오분류

## id_349273
- primary: worker_status / disposition: ['contract_termination']
- exclusion_flags: ['unrelated_to_harassment', 'unrelated_to_dismissal']
- 변경 이유: 근로자성 부정이 핵심, violence/괴롭힘 legacy 오분류

## id_34931
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 청탁금지법 위반(과태료 수준)+음주 폭언 — 해고는 양정 과다

## id_349425
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'workplace_harassment']
- 변경 이유: 5개 사유 중 3개 인정이나 해임은 양정 과다 (초심유지)

## id_349459
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'workplace_harassment']
- exclusion_flags: ['not_really_harassment_case']
- 변경 이유: 3개 사유 중 1개(비하발언)만 인정, 우발적·초범으로 양정 과다

## id_34953
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 증정품 현금화+위협 메일 인정이나 해고까지는 과다 (초심유지)

## id_349709
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 5개 사유 중 폭언만 인정, 해고는 양정 과다

## id_34973
- primary: disciplinary_severity / disposition: ['pay_cut']
- secondary: ['misconduct']
- exclusion_flags: ['unrelated_to_dismissal']
- 변경 이유: 음주 고성+욕설 + 유사 전력 — 감봉 3월 적정

## id_349757
- primary: workplace_harassment / disposition: ['pay_cut']
- secondary: ['disciplinary_severity']
- 변경 이유: 6개 괴롭힘 행위 모두 인정, 재범으로 감봉 3월 적정

## id_349773
- primary: workplace_harassment / disposition: ['suspension']
- secondary: ['misconduct', 'disciplinary_severity', 'attendance']
- 변경 이유: 폭언+보복암시 괴롭힘 인정, 개전의 정 없음으로 정직 2월 적정

## id_349775
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct']
- exclusion_flags: ['unrelated_to_harassment']
- 변경 이유: 일회성 대표 모욕에 정직 1월 — 양정 과다 전형

## id_349837
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion_flags: ['resignation_dispute', 'settlement_or_mutual_termination']
- 변경 이유: 사직서 자발 제출, 해고 부존재. violence legacy 오분류

## id_34987
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 성희롱(비의도적) 인정이나 장기근속 감안 해고 양정 과다

## id_34993
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct', 'absence_without_leave']
- 변경 이유: 4개 사유 인정이나 경미(카드 소액, 불복 2회)하여 정직 2월 과다

## id_350015
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct']
- 변경 이유: 폭언에 정직 1월 — 선례 비교로 양정 적정

## id_350075
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion_flags: ['resignation_dispute', 'settlement_or_mutual_termination']
- 변경 이유: 자발적 사직서 + IRP 수령 — 해고 부존재. violence legacy 오분류

## id_350089
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['workplace_harassment', 'disciplinary_severity']
- 변경 이유: 성희롱+스토킹+협박+괴롭힘 복합 중대 비위 — 해임 정당

## id_350173
- primary: procedure / disposition: ['suspension', 'transfer']
- secondary: ['transfer_validity', 'misconduct']
- exclusion_flags: ['procedure_dominant']
- 변경 이유: 징계사유 미특정(재심에서야 일시 특정) + 전보 부당

## id_350295
- primary: disciplinary_severity / disposition: ['pay_cut']
- secondary: ['misconduct']
- exclusion_flags: ['unrelated_to_dismissal']
- 변경 이유: 다수 비위 모두 인정 + 책임자 직급 — 감봉 적정

## id_3503
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity', 'procedure', 'absence_without_leave']
- 변경 이유: 장애인 인권침해로 시설폐쇄·허가취소 수준 중대 비위 — 해고 정당

## id_350303
- primary: dismissal_validity / disposition: ['rejection_of_regular_employment']
- secondary: ['misconduct']
- exclusion_flags: ['unrelated_to_harassment']
- 변경 이유: 수습 본채용 거부, 폭언은 복합사유 중 하나

## 주요 패턴 및 교훈

### 1. violence 배치의 실질 분포
- 물리적 폭행 사안: 2건 (id_349183 상급자 폭행, id_3503 장애인 폭행)
- 폭언·모욕·위협: 20건+ (대다수)
- violence와 무관(legacy 오분류): 4건 (사직 합의해지, 근로자성 부정)

### 2. misconduct vs disciplinary_severity 판단 기준
- **misconduct**: 비위 자체가 "고용관계 존속 불가" 수준으로 중대 (3건)
- **disciplinary_severity**: 비위는 인정되나 양정(처분 수준)의 적정성이 핵심 쟁점 (14건)
- 이 배치는 "사유 인정 + 양정 과다" 패턴이 압도적

### 3. 절차 하자 단독 부당 판정 — 3건
- 사유·양정 적정임에도 절차 하자만으로 부당 판정 (id_349109, id_349183, id_350173)
- 징계통지서 사유 미기재, 징계위원 구성 위반, 사유 미특정 등
