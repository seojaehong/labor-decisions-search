# absence_batch_011_reviewed.jsonl 1차 self-review 메모

## 배치 요약
- 총 30건 (id_19077 ~ id_19935)
- 무단결근 핵심 사건: 8건 (27%)
- 배경사실·레거시 태그 사건: 22건 (73%)

## 무단결근 핵심 사건 (exclusion_flags 없음)

### id_19315
- primary: absence_without_leave / disposition: ['dismissal']
- 판단: 월 3회 이상 무단결근이 유일한 해고사유. 전형적 결근 해고 정당 판정.

### id_19329
- primary: absence_without_leave / disposition: ['probation_termination']
- 판단: 수습기간 중 개장 당일 무단결근이 채용취소 직접 사유.

### id_19497
- primary: absence_without_leave / disposition: ['probation_termination']
- 판단: 경비원 수습기간 중 무단결근. 결근이 유일한 핵심 해고사유.

### id_19555
- primary: absence_without_leave / disposition: ['no_formal_disposition']
- 판단: 외국인근로자 5일 이상 무단결근 → 고용변동신고. 결근이 핵심 사실관계.

### id_19601
- primary: absence_without_leave / disposition: ['suspension', 'transfer']
- 판단: 취업규칙 월3회 무단결근 징계 규정 적용. 전보+결근 모두 핵심.

### id_19767
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 판단: 정직 감경 후 출근의무에도 무단결근. 누적 비위+결근이 해고 직접 사유.

### id_19879
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 판단: 타사 대표이사 겸직 + 약 2개월 장기 무단결근. 겸업+결근 병행.

### id_19935
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 판단: 전보 불응 후 1년3개월 장기 무단결근. 전형적 결근 해고 정당.

## 배경사실 사건 (not_really_absence_case 플래그 부여)

### id_19077
- primary: dismissal_validity
- 변경 이유: 무단결근은 면담 계기일 뿐 징계사유 아님. 사직 자발성이 핵심.

### id_19111
- primary: dismissal_validity
- 변경 이유: 결근은 복직 거부 맥락. 구제이익 소멸이 핵심.

### id_19139
- primary: dismissal_validity
- 변경 이유: 결근 사실관계 없음. 수습 해당 여부+해고사유 부당성이 핵심.

### id_19165
- primary: worker_status
- 변경 이유: 결근 사실관계 없음. 근로자성+서면통지 절차위반이 핵심.

### id_19187
- primary: renewal_expectation
- 변경 이유: 결근 관련 사실관계 없음. 갱신기대권+본채용 거부가 핵심.

### id_19297
- primary: disciplinary_severity
- 변경 이유: 회의 불참·지각이 징계사유이나 무단결근 아님. 양정 과다가 핵심.

### id_19317
- primary: dismissal_validity
- 변경 이유: 결근은 자진퇴사 맥락. 해고부존재가 핵심.

### id_19435
- primary: low_sales
- 변경 이유: 결근 사실관계 없음. 영업실적 전무(근무태만)가 핵심.

### id_19451
- primary: procedure
- 변경 이유: 무단결근(1일)은 배경. 재심절차 하자+양정 과다가 핵심.

### id_19493
- primary: misconduct
- 변경 이유: 근태불량의 실체는 겸업·사적활동. 무단결근이 아닌 근무시간 중 이탈.

### id_19533
- primary: dismissal_validity
- 변경 이유: 결근 관련 사실관계 전혀 없음. 의사 진료권 관련 징계사유 전부 부정당.

### id_19541
- primary: dismissal_validity
- 변경 이유: 1회 결근은 배경. 근무평가 공정성+본채용 거부 합리성이 핵심.

### id_19569
- primary: disciplinary_severity
- 변경 이유: 무단결근은 대기발령 이후 발생. 대기발령 부당성+양정 과다 핵심.

### id_19575
- primary: disciplinary_severity
- 변경 이유: 무단이탈은 사유 중 하나. 양정 과다+절차 하자가 핵심.

### id_19641
- primary: disciplinary_severity
- 변경 이유: 출퇴근 대리체크만 인정. 양정 과다가 핵심.

### id_19655
- primary: unfair_treatment
- 변경 이유: 무급병가를 무단결근으로 본 것 부정당. 노조설립 이유 불이익취급이 핵심.

### id_19747
- primary: dismissal_validity
- 변경 이유: 확정적 출근명령 없어 무단결근 불인정. 징계사유 전부 부존재.

### id_19805
- primary: misconduct
- 변경 이유: 결근 사실관계 없음. 관리감독 소홀+배치전환 거부가 핵심.

### id_1981
- primary: dismissal_validity
- 변경 이유: 무단결근 경고는 있으나 해고 의사표시 부존재가 핵심.

### id_19923
- primary: disciplinary_severity
- 변경 이유: 결근계 관행상 무단결근 문제삼지 않았던 점. 양정 과다가 핵심.

### id_19927
- primary: disciplinary_severity
- 변경 이유: 6년간 무단이탈 6회는 경미. 폭언 등 비위의 양정 과다가 핵심.

## 특이 사항 / 경계 판단

### id_1983 (confidence: medium)
- 무단결근+배임 병행 사유. primary를 misconduct로 잡음 (배임이 더 중한 사유).
- 결근도 독립적 해고사유로 인정되어 exclusion_flags 미부여.
- 재검토 필요: primary를 absence_without_leave로 할지 misconduct로 할지 경계.

### id_19879
- 겸업금지 위반+장기 무단결근 병행. primary를 absence_without_leave로 잡음.
- 2개월 장기결근이 양적으로 더 무거운 사유로 판단.

### id_19601
- 전보 정당성+무단결근 병행 쟁점. primary를 absence_without_leave로 잡음.
- 취업규칙 월3회 결근 규정이 직접 적용된 사건.

## 통계
| 구분 | 건수 |
|------|------|
| absence_without_leave (핵심) | 8 |
| disciplinary_severity | 7 |
| dismissal_validity | 7 |
| misconduct | 3 |
| procedure | 1 |
| worker_status | 1 |
| renewal_expectation | 1 |
| low_sales | 1 |
| unfair_treatment | 1 |
| **합계** | **30** |
