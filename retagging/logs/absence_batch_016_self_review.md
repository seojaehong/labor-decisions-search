# absence_batch_016_reviewed.jsonl 1차 self-review 메모

## 배치 통계
- 총 30건
- absence 핵심 사건: 12건
- absence 배경(not_really_absence_case): 12건
- absence 관련이나 배제 불필요(증거 부족 등): 6건

## not_really_absence_case 플래그 부여 (12건)

### id_23551
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['workplace_harassment', 'misconduct']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 무단결근은 과거 서면경고 배경. 핵심은 폭언·폭행·권한남용·지시불이행에 대한 정직 3개월.

### id_23631
- primary: dismissal_validity / disposition: ['dismissal', 'probation_termination']
- secondary: ['absence_without_leave']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 석가탄신일 미출근을 무단결근이라 하나 부인됨. 실질은 수습·본채용거부 사건.

### id_23683
- primary: transfer_validity / disposition: ['dismissal', 'transfer']
- secondary: ['disciplinary_severity', 'absence_without_leave']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 핵심은 전보(인사명령) 부당성. 결근은 연차휴가 반려의 결과.

### id_23801
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['attendance']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 지각 사건. 무단결근 전력 없음이 양정 과다 근거로 언급된 것일 뿐.

### id_23845
- primary: renewal_expectation / disposition: ['nonrenewal']
- secondary: ['absence_without_leave']
- exclusion_flags: ['not_really_absence_case', 'renewal_expectation_dominant']
- 변경 이유: 핵심은 갱신기대권 인정 여부. 무단결근 40일은 신뢰관계 훼손의 배경.

### id_2413
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct', 'absence_without_leave']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 무단결근은 징계사유로 불인정. 인정된 사유는 업무지시 위반·보고 누락뿐.

### id_24323
- primary: dismissal_validity / disposition: ['dismissal']
- secondary: ['procedure']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 핵심은 해고 존재 여부와 서면통지 위반. 결근은 배경사실.

### id_24367
- primary: dismissal_validity / disposition: ['dismissal']
- secondary: ['absence_without_leave', 'misconduct']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 구제이익 존부가 핵심. 무단결근은 추가 해고사유일 뿐 판단 초점 아님.

### id_24435
- primary: worker_status / disposition: ['other']
- secondary: ['disciplinary_severity', 'misconduct']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 핵심은 근로자공급 노동조합의 사용자 적격 여부. 비위는 음주·근무지 이탈.

### id_24483
- primary: dismissal_validity / disposition: ['no_formal_disposition']
- secondary: ['worker_status']
- exclusion_flags: ['not_really_absence_case', 'resignation_dispute']
- 변경 이유: 건설일용근로자 지위+해고 부존재가 핵심. 결근은 배경.

### id_24555
- primary: disciplinary_severity / disposition: ['dismissal']
- secondary: ['attendance']
- exclusion_flags: ['not_really_absence_case']
- 변경 이유: 지각·근태불량 사건. 무단결근 아님.

### id_23551 (재확인 완료 — 위 참조)

## absence 핵심 사건 (12건)

### id_23629 — 무단결근 핵심(해고 정당)
- 휴직 미신청 상태 무단결근. 취업규칙·단체협약 근거. 운수업.

### id_23637 — 무단결근 핵심(해고 부당)
- 사용자 업무정지 후 결근 → 근로자 귀책 부인.

### id_23783 — 무단결근 핵심(해고 정당)
- 33일간 무단결근. 폭행 가해자 회피가 정당사유 불인정.

### id_23805 — 무단결근 핵심(해고 정당)
- 인사명령 불응 375일 결근. 재심에서 초심 취소(해고 정당).

### id_23925 — 무단결근 핵심(양정 과다)
- 임신 중 휴직 불승인 후 무단결근. 모성보호 관점 양정 과다.

### id_24005 — 무단결근 핵심(해고 정당)
- 전보명령 불응 15일 무단결근. 출근 독려 불응.

### id_24051 — 무단결근 핵심(해고 정당)
- 복직지시 불응 약 5주 무단결근. 업무상 부상 주장 배척.

### id_24317 — 무단결근 핵심(해고 정당)
- 취업규칙 7일 초과 무단결근 해고. 우울증 방어 배척.

### id_24495 — 무단결근 핵심(양정 과다)
- 유일 인정 사유이나 사용자 부당 근무조건 변경에 기인.

### id_24281 — 무단결근 관련(절차 하자)
- 무단결근 사유 해고이나 징계절차 미이행이 핵심 하자.

### id_23827 — 무단결근 관련(해고 부존재)
- 파견근로자 출근지시 불응 → 자동퇴사. 해고 부존재.

### id_24391 — 무단결근 관련(수습 부적격)
- 수습기간 중 무단결근이 부적격 사유 중 하나.

## absence 관련이나 배제 불필요 (6건)

### id_23623 — 무단결근 포함 전 사유 불인정
### id_23651 — 근무지 무단이탈 → 양정 과다
### id_23731 — 무단결근+배임 전부 증거 부족
### id_2391 — 복합 비위(결근+법인카드+직장이탈) 강등 정당
### id_24393 — 무단결근+위협적 언사 정직 정당
### id_24427 — 무단결근+차량유지비 부정+무단이석 정직 정당
### id_24453 — 수습 1일 무단결근+미숙련 실수 → 양정 과다

## 특기 사항
- id_23925: 임신 중 무단결근 사건 — 모성보호 관점의 양정 판단 중요 사례
- id_23637, id_24495: 사용자 귀책 결근(업무정지/부당 근무조건 변경)으로 결근 책임 부인
- id_23805: 375일 최장기 결근 사례
- id_24281: 통상해고도 징계절차를 거쳐야 한다는 판시 포함
