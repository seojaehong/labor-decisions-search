# absence_batch_012_reviewed.jsonl 1차 self-review 메모

## 배치 통계
- 총 건수: 30건
- 무단결근 핵심 사례: 8건 (id_20163, id_20223, id_20287, id_20431, id_20585, id_20589, id_20781, id_20861)
- not_really_absence_case 플래그: 17건
- confidence: high 30건, medium 0건, low 0건

## 무단결근 핵심 사례 (exclusion_flags 없음, absence 관련 primary)

### id_20163
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'transfer_validity']
- 사유: 인사명령 거부 후 무단결근·이탈·근로제공 거부. 1·2차 경고 후 해고 정당.

### id_20223
- primary: absence_without_leave / disposition: ['suspension']
- secondary: ['disciplinary_severity']
- 사유: 고용정지 3일 후 경고기간 내 재차 무단결근. 정직 1월 정당. 환경미화원.

### id_20287
- primary: absence_without_leave / disposition: ['dismissal']
- secondary: ['dismissal_validity']
- 사유: 진단서 제출했으나 병가/휴직 신청서 미제출, 치료기간 종료 후 복직 미연락. 당연퇴직 정당.

### id_20431
- primary: absence_without_leave / disposition: ['dismissal']
- secondary: ['dismissal_validity']
- 사유: 대표 질책 후 임의 귀가, 3일 이상 결근. 소명기회 부여 후 해고 정당.

### id_20585
- primary: absence_without_leave / disposition: ['dismissal']
- secondary: ['dismissal_validity']
- 사유: 무단결근이 핵심이나 사용자 귀책(복직명령 미협의·출퇴근 관리 소홀)으로 해고 부당.

### id_20589
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 사유: 약 3개월 무단결근 + 동료 폭행. 징계해고 정당.

### id_20781
- primary: absence_without_leave / disposition: ['dismissal']
- secondary: ['dismissal_validity']
- 사유: 당뇨족 장기결근(약 3개월). 산재 불승인. 해고 정당.

### id_20861
- primary: attendance / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'absence_without_leave']
- 사유: 근태관리 책임자의 지속적 근태불량 + 전산 부정입력 지시. 해고 정당.

## not_really_absence_case 플래그 부여 사례 (17건)

### id_19949
- primary: misconduct / disposition: ['disciplinary_dismissal']
- 사유: 무단이탈은 6개 징계사유 중 하나. 핵심은 복합비위(풍기문란·지시불복 등).

### id_2005
- primary: workplace_harassment / disposition: ['disciplinary_dismissal']
- 사유: 성희롱이 주된 비위. 무단이탈은 부수적.

### id_20111
- primary: worker_status / disposition: ['dismissal']
- 사유: 필라테스 강사 근로자성 부정. 결근은 근로자성 판단 고려요소일 뿐.

### id_20215
- primary: disciplinary_severity / disposition: ['suspension']
- 사유: 청소불량 근무태만이 핵심. 결근/무단결근 언급 전혀 없음.

### id_20347
- primary: dismissal_validity / disposition: ['disciplinary_dismissal']
- 사유: 해고 존부가 핵심. 무단결근은 이후 징계위원회 사유로만 언급.

### id_20365
- primary: procedure / disposition: ['dismissal']
- 사유: 수습기간·절차 하자가 핵심. 근태불량은 배경.

### id_20387
- primary: transfer_validity / disposition: ['transfer']
- 사유: 승무변경(전보) 정당성이 핵심. 무단결근 2회는 근무태도 불성실 근거.

### id_20409
- primary: dismissal_validity / disposition: ['no_formal_disposition']
- 사유: 외국인근로자 고용변동신고=해고인지 여부. 결근은 사실관계.

### id_20441
- primary: misconduct / disposition: ['disciplinary_dismissal']
- 사유: 언어폭력·인사명령 거부가 동등 이상 비중. 무단결근은 복합비위 일부.

### id_20445
- primary: dismissal_validity / disposition: ['no_formal_disposition']
- 사유: 합의해지 인정. 무단이탈은 전보 거부 맥락.

### id_20487
- primary: dismissal_validity / disposition: ['dismissal']
- 사유: 해고 존부·서면통지 위반이 핵심. 결근은 간접 사실.

### id_20553
- primary: disciplinary_severity / disposition: ['dismissal']
- 사유: 양정 과다·절차 위반이 핵심. 근무태만은 징계사유로도 부인.

### id_20683
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- 사유: 결근일 개인택시 영업 수입금 미납부. 핵심은 양정 과다·회사 묵인.

### id_20711
- primary: misconduct / disposition: ['probation_termination']
- 사유: 시용 중 문자 폭언·SNS 비방이 결정적. 무단이탈은 부수적.

### id_20723
- primary: dismissal_validity / disposition: ['dismissal']
- 사유: 해고 존부·서면통지 위반. 무단결근은 사용자 주장이나 후속조치 없음.

### id_20793
- primary: disciplinary_severity / disposition: ['suspension']
- 사유: 동료 특수폭행 벌금형. 근무태만은 과거 타인 사례 언급일 뿐.

### id_20823
- primary: disciplinary_severity / disposition: ['dismissal']
- 사유: 무단결근 사유 불인정. 인정된 사유는 환자 민원·경위서 제출 거부.

## 경계 사례 메모

### id_19959 (exclusion_flags 없음)
- 근태불량이 유일하게 인정된 징계사유이나, 핵심 법리는 이중징계·양정 과다. not_really_absence_case를 붙이지 않은 이유: 근태불량이 유일 인정 사유라 결근 검색에서 노출될 가치 있음.

### id_20199 (exclusion_flags 없음)
- 무단결근이 인정 징계사유이나 하루 결근+기존 경고 완료. 양정 과다 판단. 무단결근 양정 과다 검색에 유용.

### id_20345 (exclusion_flags 없음)
- 무단결근이 형식적 해고사유이나 실질은 병가 반려. 병가 불승인→결근 패턴 검색에 핵심적.

### id_20395 (exclusion_flags 없음)
- 무단결근이 3대 사유 중 하나. 허위경력이 더 중하나, 병가 미승인 결근도 독자적 비중 있음.

### id_20231 (not_really_absence_case)
- 단체협약 해석 견해제시 사건. 결근은 지급제한 사유 열거 항목. 해고와 무관.
