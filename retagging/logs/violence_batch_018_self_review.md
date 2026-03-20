# violence_batch_018_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건 (violence 레거시 태그 포함 사건)
- 중점 분석: misconduct vs disciplinary_severity 구분
- violence 배치이나 실질 폭력이 핵심 쟁점이 아닌 사건 다수 포함

## misconduct vs disciplinary_severity 판단 기준
- **misconduct**: 비위행위 자체가 중하고 해고/징계가 정당하다고 인정된 사건 (양정 다툼 없거나 양정 적정 판단)
- **disciplinary_severity**: 비위사유는 인정되나 양정이 과다하다고 판단된 사건, 또는 양정 적정성이 핵심 쟁점인 사건

## 통계 요약

| 구분 | 건수 |
|------|------|
| misconduct (primary) | 10건 |
| disciplinary_severity (primary) | 11건 |
| procedure (primary) | 2건 |
| dismissal_validity (primary) | 4건 |
| worker_status (primary) | 1건 |
| transfer_validity (primary) | 1건 |
| absence_without_leave (primary) | 1건 |

| confidence | 건수 |
|------------|------|
| high | 30건 |
| medium | 0건 |

## violence 배치에 폭력 쟁점이 없는 사건 (7건)
- id_27115: 불륜 사적 비위 양정 과다
- id_27205: 사직서 자발성 (해고 부존재)
- id_27273: 해외파견 사용자 지위
- id_27275: 징계사유 입증 부족
- id_27309: 사직서 자발성 (해고 부존재)
- id_27313: 무단결근 22회 해고 정당
- id_27597: 인트라넷 명예훼손·그룹쪽지 남용

## 케이스별 리뷰

### id_27023
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct', 'unfair_treatment']
- 변경 이유: 징계사유 일부 인정이나 양정 과다가 핵심 판단. 노조 관련 주장은 기각.
- 폭행 아닌 업무방해·무례 수준

### id_27061
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 승객 폭행 사유·절차 정당이나 양정 과다가 결론. 피해자 유발·합의·탄원서 감경.

### id_27091
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 노인학대(신체적+정서적) 비위 중대. CCTV 증거, 반성 없음, 기관 운영 위험. 해고 정당.

### id_27115
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 불륜만 인정. 사적 영역·업무 무관·장기근속으로 양정 과다. violence 쟁점 없음.
- exclusion: fact_specific_low_reusability

### id_27131
- primary: misconduct / disposition: ['suspension']
- secondary: ['disciplinary_severity']
- 변경 이유: 블랙박스 방해·무단운행·부당요금 등 복합 비위. 재심 정직 적정.

### id_27171
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['procedure']
- 변경 이유: 폭언 하나만으로 해고는 양정 과다. 소명기회 미부여 절차 하자도 병존.

### id_27197
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 환자 폭행 사유 인정이나 6년 근속·초범·반성·형사처벌 없음으로 양정 과다.
- id_27091(노인학대 해고 정당)과 대비 가치

### id_27205
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion: ['resignation_dispute', 'unrelated_to_dismissal']
- 변경 이유: 사직 자발성 판단. 폭력 쟁점 없음. 해고 부존재.

### id_27207
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'unfair_treatment']
- 변경 이유: 폭언·모욕 일부만 인정되어 해고 양정 과다. 부당노동행위 불인정.

### id_27243
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 6년 이상 전 폭행의 뒤늦은 징계가 신뢰보호 위반. 26년 근속·비교형평 등 양정 과다.

### id_27269
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 어깨 밀침 정도의 경미한 폭행. 가해자만 징계한 형평성 문제. 양정 과다.

### id_27273
- primary: worker_status / disposition: ['dismissal']
- secondary: ['dismissal_validity', 'transfer_validity']
- 변경 이유: 해외파견 사용자 지위가 핵심. 과거 폭행(공소권 없음)은 업무 무관. violence 쟁점 없음.

### id_27275
- primary: dismissal_validity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- exclusion: ['evidence_too_thin']
- 변경 이유: 징계사유 입증 부족이 핵심. 과거 폭언 전력은 배경일 뿐.

### id_27289
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 복합 비위(무단외근+폭언+침뱉기+AED 위협+경찰신고) 누적. 해고 정당.

### id_27309
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion: ['resignation_dispute', 'unrelated_to_dismissal']
- 변경 이유: 사직서 자발성 판단. 폭력 쟁점 없음.

### id_27313
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'disciplinary_severity']
- 변경 이유: 22회 무단결근이 핵심. violence 쟁점 없음.

### id_27323
- primary: misconduct / disposition: ['disciplinary_dismissal', 'suspension', 'pay_cut']
- secondary: ['disciplinary_severity', 'attendance']
- 변경 이유: 복수 근로자 단계적 징계. 폭행 포함 해고 양정 적정. misconduct 전형.

### id_27413
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 관리사무소장의 입주민 폭행·폭언·운영마비 등 중대 비위. 해고 정당.

### id_27447
- primary: misconduct / disposition: ['suspension']
- secondary: ['disciplinary_severity', 'procedure']
- 변경 이유: 음주·폭언·명예훼손·허위사실유포 등 복합 비위. 정직 정당. 단체협약 구속력 쟁점 포함.

### id_27469
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 상급자 일방적 폭행. 해고 정당. misconduct 전형 중의 전형.

### id_2755
- primary: disciplinary_severity / disposition: ['pay_cut', 'transfer']
- secondary: ['transfer_validity']
- 변경 이유: 점장 관리감독 책임 감봉 양정 과다 + 부당한 징계 근거 인사명령도 부당.

### id_27583
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct']
- 변경 이유: 폭행 사유 인정이나 피해자 원인 제공으로 정직 양정 과다.

### id_27597
- primary: misconduct / disposition: ['suspension']
- secondary: ['disciplinary_severity']
- 변경 이유: 인트라넷 명예훼손·그룹쪽지 남용 등 사내 질서위반. 정직 3개월 적정. violence 쟁점 없음.

### id_27603
- primary: transfer_validity / disposition: ['transfer']
- secondary: ['misconduct']
- 변경 이유: 파견근로자 대기발령 정당성이 핵심. 폭행은 대기발령 사유 배경.

### id_27693
- primary: dismissal_validity / disposition: ['dismissal']
- secondary: ['misconduct']
- 변경 이유: 고용승계 의무 인정 여부가 핵심. 비위 유무별 승계 거부 정당/부당 비교 판단.

### id_27759
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 야구방망이·식칼 위협 + 형사유죄. 가장 중한 유형의 폭력. 해고 정당.

### id_27775
- primary: procedure / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- exclusion: ['procedure_dominant']
- 변경 이유: 징계사유 전부 인정이나 인사위원회 외부위원 미포함 절차 하자가 결정적.

### id_27821
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 무방비 직원 일방적 폭행 + 교통사고·민원 다수. 해고 정당.

### id_27937
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct']
- 변경 이유: 회식 중 말다툼 수준. 출근정지 5일 양정 과다. 22년 무징계 감경.

### id_27971
- primary: procedure / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- exclusion: ['procedure_dominant']
- 변경 이유: 단체협약 절차 미준수가 결정적 하자. 폭행 비위 인정→부당노동행위 불인정.

## misconduct vs disciplinary_severity 주요 분기 패턴

### misconduct로 판단한 경우
1. **일방적 폭행**: id_27469, id_27821 - 피해자 유발 없이 일방적 가해
2. **중대 비위**: id_27091(노인학대), id_27759(흉기위협), id_27289(복합 비위 누적)
3. **양정 적정**: id_27131, id_27323, id_27413, id_27447, id_27597 - 비위 정도에 비례한 징계

### disciplinary_severity로 판단한 경우
1. **피해자 유발 존재**: id_27061(승객 유발), id_27583(피해자 원인 제공)
2. **비위 경미**: id_27269(어깨 밀침), id_27937(말다툼)
3. **정상참작 미반영**: id_27197(장기근속·초범), id_27243(뒤늦은 징계)
4. **사유 일부만 인정**: id_27023, id_27171, id_27207

### 비폭력 사건 (violence 배치 부적합)
- 7건이 실질 폭력 쟁점 없음 → exclusion_flags 또는 retrieval_note에 명시
