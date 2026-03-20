# violence_batch_016_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건, violence 레거시 태그 배치
- 핵심 판단 축: misconduct vs disciplinary_severity
- misconduct: 비위행위 자체의 존부·중대성이 쟁점
- disciplinary_severity: 비위 인정되나 처분 수준(양정)이 과다 여부가 쟁점

## 분류 통계
| primary | 건수 |
|---------|------|
| misconduct | 11 |
| disciplinary_severity | 10 |
| procedure | 3 |
| dismissal_validity | 3 |
| worker_status | 2 |
| transfer_validity | 1 |

## id_2543
- primary: disciplinary_severity / disposition: ['reprimand']
- 변경 이유: 견책이라는 경미한 처분이고 양정 적정 여부가 주된 판단. 사유도 인정.

## id_25431
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- 변경 이유: 폭언·폭행 사유 인정되나 해고라는 최중 처분이 과다 — 양정이 핵심 쟁점.

## id_25453
- primary: misconduct / disposition: ['disciplinary_dismissal']
- 변경 이유: 상급자 폭행이라는 비위 자체의 중대성이 핵심. 해고 정당 판정.

## id_255
- primary: procedure / disposition: ['pay_cut', 'suspension']
- 변경 이유: violence 배치이나 실질은 괴롭힘 신고에 대한 사실조사 미비. 사유 자체가 입증 부족으로 불인정.
- exclusion_flags: ['not_really_harassment_case', 'emotional_conflict_not_harassment']

## id_25521
- primary: transfer_validity / disposition: ['transfer']
- 변경 이유: violence 배치이나 실질은 대기발령의 징벌성·사유 정당성. 협박은 혐의없음.
- exclusion_flags: ['not_really_performance_case']

## id_25525
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- 변경 이유: 쌍방 폭행에서 상대방 감봉2월 vs 근로자 해고 — 형평성 결여로 양정 과다.

## id_25527
- primary: disciplinary_severity / disposition: ['suspension']
- 변경 이유: 팀장 경고 vs 근로자 정직2월 — 형평성 결여 + 표창감경 미적용.

## id_25557
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- 변경 이유: violence 배치이나 폭력 무관. 사적 영역 불륜에 대한 해고 양정 과다.
- exclusion_flags: ['fact_specific_low_reusability']

## id_25581
- primary: misconduct / disposition: ['disciplinary_dismissal']
- 변경 이유: 허위인력 신고·폭행 유죄판결·사용자 협박·자료삭제 등 다수 중대 비위. 해고 정당.

## id_25605
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- 변경 이유: 무단결근 사유 인정되나 사용자가 폭행 가해자와 동일팀 배치한 귀책 — 양정 과다.

## id_25637
- primary: worker_status / disposition: ['transfer']
- 변경 이유: 비등기 임원 근로자성 판단이 선결 쟁점. 업무배제 정당성은 부차적.
- exclusion_flags: ['unrelated_to_dismissal']
- 참고: id_25751과 동일 사건(초심/재심)

## id_25645
- primary: dismissal_validity / disposition: ['no_formal_disposition']
- 변경 이유: violence 배치이나 실질은 사직서의 자발성 여부. 합의해지 인정으로 해고 부존재.
- exclusion_flags: ['resignation_dispute', 'settlement_or_mutual_termination']

## id_25655
- primary: dismissal_validity / disposition: ['dismissal']
- 변경 이유: violence 배치이나 폭력 무관. 무단결근·배임 사유 전부 입증 부족.
- exclusion_flags: ['evidence_too_thin']

## id_25707
- primary: misconduct / disposition: ['suspension']
- 변경 이유: 공개장소에서 상사 멱살·폭언 — 비위행위의 중대성 핵심. 정직3월 정당.

## id_25709
- primary: misconduct / disposition: ['suspension']
- 변경 이유: 동료 여직원 폭행(진단서·치료비 확인) — 비위행위 인정이 핵심. 정직3월 정당.

## id_25751
- primary: worker_status / disposition: ['transfer']
- 변경 이유: id_25637 초심. 비등기 임원 근로자성 + 업무배제 정당성.
- exclusion_flags: ['unrelated_to_dismissal']

## id_25757
- primary: dismissal_validity / disposition: ['no_formal_disposition']
- 변경 이유: violence 배치이나 폭력 무관. 사직 권유 후 자발적 사직원 제출 — 합의해지.
- exclusion_flags: ['resignation_dispute', 'settlement_or_mutual_termination']

## id_25779
- primary: misconduct / disposition: ['reprimand']
- 변경 이유: 시위 중 관리직원에 대한 위협·폭력이 핵심 비위. 견책 최경 처분.

## id_25781
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- 변경 이유: 사내폭행 사유 인정되나 양정 과다 + 단체협약 징계행위기간 위반 절차 하자.

## id_25791
- primary: misconduct / disposition: ['transfer', 'suspension']
- 변경 이유: 상무이사의 폭언·협박·항명 비위의 중대성이 핵심. 전보+대기발령+정직 모두 정당.

## id_25803
- primary: disciplinary_severity / disposition: ['suspension']
- 변경 이유: 다수 사유 중 주된 사유 불인정, 인정 사유 대비 무기한 정직 과다.

## id_2583
- primary: misconduct / disposition: ['suspension']
- 변경 이유: 회사 협박·운행 중 전화통화 비위 인정. 정직18일 적정. violence 배치이나 폭력 아님.

## id_25879
- primary: misconduct / disposition: ['pay_cut', 'suspension']
- 변경 이유: 관리자급의 센터장 모욕·지시불이행이 핵심 비위. 감급1월+정직1월 정당.

## id_25907
- primary: misconduct / disposition: ['disciplinary_dismissal']
- 변경 이유: 일방적 폭행 + 교통사고·민원 다수 누적 — 비위 중대성 핵심. 해고 정당.

## id_25923
- primary: dismissal_validity / disposition: ['no_formal_disposition']
- 변경 이유: 외국인 근로자 사업장 이탈. 폭행 주장 증거불충분. 해고 부존재.
- exclusion_flags: ['resignation_dispute', 'evidence_too_thin']

## id_25945
- primary: procedure / disposition: ['disciplinary_dismissal']
- 변경 이유: 폭행 등 사유 모두 인정되나 소명기회 미부여 절차 하자가 결정적.
- exclusion_flags: ['procedure_dominant']

## id_25949
- primary: procedure / disposition: ['disciplinary_dismissal']
- 변경 이유: 서면통지 미이행이 일차적 위법 사유 + 사유 일부 불인정 + 양정 과다.
- exclusion_flags: ['procedure_dominant']

## id_25963
- primary: misconduct / disposition: ['disciplinary_dismissal']
- 변경 이유: 허위기재·폭언·불량생산·지시불이행 복수 비위 누적 — 해고 정당.

## id_25991
- primary: disciplinary_severity / disposition: ['pay_cut']
- 변경 이유: 사유 인정되나 징계이력 없음·표창·상급자 욕설 원인 등 참작 시 감봉3월 과다.

## id_25999
- primary: misconduct / disposition: ['disciplinary_dismissal']
- 변경 이유: 장기간 반복 폭언·막말 + 언론보도 — 비위 중대성 핵심. 공공기관 해고 정당.

## 주요 패턴 및 특이사항
1. **violence 배치이나 폭력 무관 사건 6건**: id_255(괴롭힘 조사미비), id_25521(대기발령), id_25557(불륜), id_25645/25757(합의해지), id_25655(입증부족) — exclusion_flags 적극 부여
2. **misconduct vs disciplinary_severity 구분 기준**: 판정문이 "징계사유 인정 + 양정 과다"를 명시하면 disciplinary_severity, "비위 중대하여 해고/징계 정당"이면 misconduct
3. **형평성(comparative_fairness) 사건**: id_25525(감봉2월 vs 해고), id_25527(경고 vs 정직2월) — 비교 대상 존재가 양정 과다 판단의 핵심 근거
4. **초심/재심 쌍**: id_25637/id_25751 동일 사건
5. **procedure 우선 사건**: id_25945(소명기회), id_25949(서면통지) — 사유 인정되더라도 절차 하자가 결정적이면 procedure를 primary로
