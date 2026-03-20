# absence_batch_014_reviewed.jsonl 1차 self-review 메모

## 배치 요약
- 총 30건 처리
- 결근 핵심(absence_without_leave primary): 7건
- 결근 배경(not_really_absence_case): 16건
- 기타 쟁점 우세: 7건

## 결근 핵심 사례 (issue_type_primary = absence_without_leave)

### id_21899
- primary: absence_without_leave
- 50일 장기 무단결근 외국인근로자, 해고부존재 판정
- exclusion: resignation_dispute (자진퇴사 성격)

### id_21947
- primary: absence_without_leave
- 복직통보 후 병가·휴직 미신청 무단결근 → 당연퇴직 정당

### id_22233
- primary: absence_without_leave
- 산재 불승인 + 37일 무단결근 → 징계해고 정당

### id_22237
- primary: absence_without_leave
- 정당한 인사명령 거부 + 무단결근·이탈 → 해고 정당

### id_22373
- primary: absence_without_leave
- 장기 무단결근 + 폭력행위 → 해고 정당

### id_22679
- primary: absence_without_leave
- 병가 미승인(진단서 미첨부) 후 장기결근 → 징계해고 정당

### id_2281
- primary: absence_without_leave
- 5일 이상 무단결근 → 인사규정상 직권면직 정당

## not_really_absence_case 플래그 부여 사례 (16건)

### id_21851
- primary: transfer_validity
- 부당전직 후 결근 → 양정과다. 전직 부당성이 핵심.

### id_22019
- primary: transfer_validity
- 부당 배치대기 불응 = 무단결근 아님

### id_22031
- primary: misconduct
- 업무방해·욕설·지시거부가 주된 비위. 결근은 부수.

### id_22137
- primary: renewal_expectation
- 무단결근 27일이나 판정 핵심은 계약기간 만료·구제이익 부존재

### id_22151
- primary: disciplinary_severity
- 무단결근 징계사유 자체가 불인정됨. 환자제재가 쟁점.

### id_22171
- primary: renewal_expectation
- 갱신기대권 불인정이 핵심. 결근은 신뢰훼손 근거 중 하나.

### id_22273
- primary: worker_status
- 사용자 적격 + 음주 비위가 핵심. 근무지 이탈은 음주의 부수.

### id_22327
- primary: misconduct
- 무단이탈 징계사유 자체가 불인정. 소란행위만 인정.

### id_22471
- primary: disciplinary_severity
- 무단결근 사실 자체가 없음. 지각·업무태만만 인정.

### id_22495
- primary: worker_status
- 등기감사 근로자성 판단. 결근과 완전 무관.

### id_22509
- primary: transfer_validity
- 부당 인사발령 불응을 결근으로 간주 불가.

### id_22555
- primary: transfer_validity
- 부당 배치대기 불응 = 결근 아님 + 900일 지연 징계 신의칙 위반.

### id_22591
- primary: unfair_treatment
- 부당 근무조건 변경 이의제기 과정 결근. 징계사유 전부 불인정.

### id_22713
- primary: misconduct
- 7가지 복합 비위. 근태불량은 부수적.

### id_22773
- primary: misconduct
- 상습 언어폭력·위협이 핵심. 교육명령 거부 결근은 보조.

### id_22791
- primary: disciplinary_severity
- 금전유용+개인정보유출+결근(강제억류). 양정 과다 판정.

### id_22805
- primary: misconduct
- 시설훼손·작업불량이 핵심. 과거 결근은 양정 참고사항.

## 기타 쟁점 우세 (not_really_absence_case 미부여, 결근 외 primary)

### id_21975
- primary: disciplinary_severity
- 신선기 파손 + 결근 복합. 결근도 주요 사유이므로 exclusion 미부여.

### id_22393
- primary: attendance
- 근태불량(지각·결근·이탈) 전반이 쟁점. 결근 관련 사례.

### id_22399
- primary: dismissal_validity
- 장기결근 → 해고부존재(자진퇴사). resignation_dispute 플래그.

### id_22405
- primary: misconduct
- 영업직 상습 자택체류. 근무태만/결근 경계. exclusion 미부여.

### id_22635
- primary: disciplinary_severity
- 결근·조퇴 일부 인정이나 양정·절차가 핵심.

### id_22823
- primary: disciplinary_severity
- 결근 사유 정당이나 정직 45일 양정 과다.

## 패턴 분석
1. **부당 인사명령/전직 → 결근 → 징계** 패턴 4건 (id_21851, 22019, 22509, 22555): 모두 not_really_absence_case
2. **장기 무단결근 → 직권면직/당연퇴직/해고 정당** 패턴 4건 (id_21947, 22233, 22679, 2281): 전형적 결근 핵심 사례
3. **복합 비위 중 결근은 부수적** 패턴 6건 (id_22031, 22327, 22713, 22773, 22791, 22805): 모두 not_really_absence_case
4. **계약만료/근로자성 등 결근 외 쟁점 우세** 4건 (id_22137, 22171, 22273, 22495)
