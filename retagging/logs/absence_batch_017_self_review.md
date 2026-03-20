# absence_batch_017_reviewed.jsonl 1차 self-review 메모

## 통계 요약
- 총 30건 처리
- 결근 진성(absence_without_leave primary): 7건
- 결근 배경(not_really_absence_case): 19건
- 기타(결근 사유이나 입증 실패 등): 4건

## 결근 진성 사건 (absence_without_leave가 primary)

### id_24667
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 근로자1·2의 무단결근이 핵심 해고사유. 운수업.

### id_24677
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 출근명령 불응 + 11일 무단결근. 취업규칙 해고기준(연속3일/월5일) 적용. 단독 결근 사유.

### id_24821
- primary: absence_without_leave / disposition: ['reprimand']
- 근무지 무단이탈이 유일한 징계사유. 견책 처분.

### id_24887
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 장기 무단결근 사유 인정되나 사용자 책임 상당하여 양정 과다.

### id_25011
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 산업기능요원 반복 근태불량. 3차 경고장 후에도 미개선. 단독 결근 사유.

### id_25145
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 무단결근이 형식적 사유이나 실질은 병가 승인 거부 재량권 남용. 결근 자체가 쟁점.

### id_25157
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 장기 무단결근 단독 사유(폭행은 시효 도과). 단체협약 6일 기준.

## 결근 배경 사건 (not_really_absence_case)

### id_24565
- primary: misconduct
- 근태불량은 증거 없어 불인정. 핵심은 폭언·성희롱적 발언·업무과실·지시불이행.

### id_24605
- primary: procedure
- 근태불량은 합의 종결 + 입증 없음. 핵심은 일사부재리 원칙 위배.

### id_24671
- primary: misconduct
- 무단지각은 복합 비위 중 일부. 핵심은 업무오류·욕설·기물파손.

### id_24703
- primary: misconduct
- 무단결근은 5개 사유 중 하나. 차명거래법 위반이 더 중한 비위.

### id_24737
- primary: misconduct
- 결근은 횡령 배경. 핵심은 운송수입금 미납·폭언·업무방해.

### id_24779
- primary: misconduct
- 무단결근은 3개 사유 중 하나. 고객금전 유용이 핵심.

### id_24817
- primary: dismissal_validity
- 무단결근 통보는 출근 독려 맥락. 핵심은 해고 존부·구제이익.

### id_24929
- primary: dismissal_validity
- 결근은 해고 존부 판단 배경. 핵심은 '푹 쉬세요' 발언의 해고 의사표시 여부.

### id_24961
- primary: disciplinary_severity
- 근태불량 배경. 핵심은 근무태만(가수금 미정리)과 양정 과다.

### id_24965
- primary: dismissal_validity
- 무단결근 주장 입증 안 됨. 핵심은 사직 의사표시 해석.

### id_24991
- primary: procedure
- 근태불량이 사유이나 입증 부족으로 불인정. 절차 하자도 인정.

### id_25067
- primary: procedure
- 무단결근은 사용자 측 주장. 실제는 사직 권고 후 일방적 종료. 서면통지 흠결.

### id_25077
- primary: misconduct
- 무단결근은 복합 비위 중 하나. 육아휴직 중 겸업·모욕이 핵심.

### id_25105
- primary: misconduct
- 무단결근은 과거 징계이력 중 일부. 핵심 사유는 폭행.

### id_25125
- primary: disciplinary_severity
- 근무지 무단이탈은 3개 사유 중 하나. 민원 과다 야기가 핵심.

### id_25187
- primary: misconduct
- 무단결근은 월권행위·직무유기 등 복합 비위 중 하나.

### id_2527
- primary: dismissal_validity
- 승무거부 결근은 배경. 핵심은 4대보험 상실신고의 해고 해당 여부.

### id_25289
- primary: dismissal_validity
- 무단결근은 복직명령 배경. 핵심은 해고 존부·구제이익 소멸.

## 기타 (결근 사유이나 입증 실패 / 양정 쟁점)

### id_24749
- primary: procedure
- 무단결근 자체는 다투지 않으나 해고일 소급으로 논리적 모순 발생.

### id_24911
- primary: dismissal_validity
- 무단결근으로 근로관계 자동 해지, 해고 부존재 판정.

### id_24921
- primary: dismissal_validity
- 사용자 무단결근 주장 입증 실패. 이탈신고 부당.

### id_25245
- primary: disciplinary_severity
- 무단결근 사유 인정되나 연차휴가 반려 형평성 문제로 양정 과다.

### id_25297
- primary: dismissal_validity
- 무단결근 입증 자료 부족으로 사유 불인정.

## 판단 기준 메모
- 무단결근이 **유일하거나 가장 중한 징계사유**이면 진성(absence_without_leave primary)
- 무단결근이 **복합 비위 중 하나이고 다른 사유가 더 중하면** 배경(not_really_absence_case)
- 무단결근이 **사용자 주장일 뿐 입증 안 되거나**, 해고 존부·절차가 핵심이면 배경
- 무단결근 사유 인정되더라도 **양정 과다가 핵심 쟁점**이면 disciplinary_severity primary로
