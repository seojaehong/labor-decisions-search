# violence_batch_015_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 30건 (violence 레거시 태그 포함 사건)
- 중점 분석: misconduct vs disciplinary_severity 구분
- violence 배치이나 실질 폭력이 핵심 쟁점이 아닌 사건 다수 포함

## misconduct vs disciplinary_severity 판단 기준
- **misconduct**: 비위행위 자체가 중하고 해고/징계가 정당하다고 인정된 사건 (양정 다툼 없거나 양정 적정 판단)
- **disciplinary_severity**: 비위사유는 인정되나 양정이 과다하다고 판단된 사건, 또는 양정 적정성이 핵심 쟁점인 사건

## 케이스별 리뷰

### id_24543
- primary: dismissal_validity / disposition: ['reprimand']
- secondary: ['disciplinary_severity', 'procedure']
- 변경 이유: 쟁의행위 정당성이 핵심. 폭언은 부수적. 징계사유 자체가 부존재하므로 misconduct 아님.
- exclusion: violence 배치이나 폭력 사건 아님

### id_24565
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity', 'attendance']
- 변경 이유: 복합 비위(폭언+성희롱+업무과실+지시불이행)로 해고 정당. 사유가 핵심이므로 misconduct.

### id_24571
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 폭행 사유 인정되나 결론은 양정 과다. 핵심 판단이 양정이므로 disciplinary_severity.

### id_24577
- primary: dismissal_validity / disposition: ['other']
- secondary: ['procedure']
- 변경 이유: 노동조합 내부 징계 규약 위반 사건. 일반 사용자 징계와 성격 다름. 폭행은 과거 사실 언급에 불과.
- confidence: medium (특수 사건 유형)

### id_24667
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'attendance', 'absence_without_leave']
- 변경 이유: 복수 근로자 중 일부 인용·일부 기각. 양정 판단이 분기점.

### id_24671
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['attendance', 'disciplinary_severity']
- 변경 이유: 9개월 17회 비위 축적으로 해고 정당. 비위 내용·반복성이 핵심.

### id_24693
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion: ['resignation_dispute', 'unrelated_to_dismissal']
- 변경 이유: 사직 자발성이 핵심. 폭행은 배경일 뿐 징계 쟁점 아님.

### id_24699
- primary: wage_dispute / disposition: ['other']
- exclusion: ['fact_specific_low_reusability', 'unrelated_to_dismissal']
- 변경 이유: 근로조건 위반 손해배상 사건. 폭행·감금은 근로조건과 무관하다고 판단. 특수 유형.

### id_24703
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['absence_without_leave', 'disciplinary_severity']
- 변경 이유: 폭언+차명거래+무단결근+1인시위 등 복합 비위 전부 인정. 해고 정당.

### id_24737
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct', 'absence_without_leave']
- 변경 이유: 노동위 판정에 따라 감경된 정직의 양정 적정성이 핵심.

### id_24785
- primary: misconduct / disposition: ['suspension']
- secondary: ['disciplinary_severity']
- 변경 이유: 성희롱+폭행 반복 비위로 정직 3월(해고 가능 사유를 감경). 비위 내용이 핵심.

### id_24829
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct']
- 변경 이유: 쌍방폭행 출근정지 20일의 양정 적정성이 핵심 판단.

### id_24833
- primary: disciplinary_severity / disposition: ['suspension']
- secondary: ['misconduct', 'comparative_fairness']
- 변경 이유: 화해·징계형평을 근거로 정직 1월 양정 과다. 감경사유 판단이 핵심.

### id_24839
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion: ['resignation_dispute', 'unrelated_to_dismissal']
- 변경 이유: 퇴직원 자발성 판단. violence 태그는 legacy 오류로 추정(본문에 폭행 없음).

### id_24849
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['procedure', 'comparative_fairness']
- 변경 이유: 형평성 위반(상대 정직2월 vs 근로자 해고) + 절차 하자(사전통지 미준수).

### id_24877
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct']
- 변경 이유: 징계사유 일부만 인정 + 동기 참작 사정 → 양정 과다.

### id_24893
- primary: misconduct / disposition: ['demotion']
- secondary: ['disciplinary_severity']
- 변경 이유: 상급자 고성·욕설 반복 + 동종 전력(공개사과→경위서→경고→감봉→강등). 비위 반복이 핵심.

### id_2491
- primary: procedure / disposition: ['disciplinary_dismissal']
- secondary: ['workplace_harassment', 'retaliation']
- 변경 이유: 직장내괴롭힘 가해자가 징계위원장으로 참석한 구성 하자가 핵심. violence는 '언어 폭행'.

### id_25007
- primary: misconduct / disposition: ['pay_cut']
- secondary: ['disciplinary_severity']
- 변경 이유: 감봉 후 6일 만에 동종 재발. 반복 비위가 핵심. 장애인 복지택시 겸직도 중대.

### id_25025
- primary: dismissal_validity / disposition: ['disciplinary_dismissal']
- secondary: ['worker_status']
- 변경 이유: 징계사유 4건 전부 불인정. violence는 '협박성 발언' 때문이나 자기방어로 판단.

### id_25077
- primary: misconduct / disposition: ['disciplinary_dismissal', 'transfer']
- secondary: ['absence_without_leave', 'worker_status', 'transfer_validity']
- 변경 이유: 무단결근+겸직+모욕으로 해고 정당. 당사자적격·제척기간도 병합.

### id_25091
- primary: procedure / disposition: ['reprimand']
- secondary: ['misconduct']
- 변경 이유: 사유 정당이나 재심위원회 구성 + 변론기회 미부여로 절차 하자. 절차가 결론 결정.

### id_25105
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 폭행 벌금형 + 9차례 전력으로 해고 정당. 비위·전력이 핵심.

### id_25133
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'procedure']
- 변경 이유: 난동·폭행 우발적+피해 경미 → 해임 양정 과다. 절차 하자(위원회 구성)도 병존.

### id_25157
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity', 'misconduct']
- 변경 이유: 폭행은 징계시효 도과. 무단결근만으로 해고 정당. 실질은 무단결근 사건.
- exclusion: violence 배치이나 폭행은 시효 도과

### id_25293
- primary: dismissal_validity / disposition: ['dismissal']
- exclusion: ['resignation_dispute', 'unrelated_to_dismissal']
- 변경 이유: 사직서 자발성 판단. 폭행은 사직 배경일 뿐.

### id_25323
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'procedure']
- 변경 이유: 6건 중 1건만 인정 + 양정 과다 + 절차 하자(궐석 징계위원회).

### id_25341
- primary: misconduct / disposition: ['disciplinary_dismissal']
- secondary: ['disciplinary_severity']
- 변경 이유: 사고다발+무정차+폭언 복합으로 해고 정당. 비위 내용이 핵심.

### id_2537
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal']
- secondary: ['misconduct', 'comparative_fairness']
- 변경 이유: 쌍방폭행인데 일방만 해고. 편향 조사+형평 위반으로 양정 과다.

### id_25407
- primary: disciplinary_severity / disposition: ['disciplinary_dismissal', 'suspension']
- secondary: ['procedure', 'misconduct']
- 변경 이유: 사유 인정되나 양정 과다 + 해고통지서 사유 미기재 등 절차 하자. 복합.

## 통계 요약

### issue_type_primary 분포
| primary | 건수 |
|---------|------|
| disciplinary_severity | 12 |
| misconduct | 9 |
| dismissal_validity | 5 |
| procedure | 2 |
| absence_without_leave | 1 |
| wage_dispute | 1 |

### 핵심 패턴
1. **violence 배치이나 실질 폭력이 아닌 사건**: 6건 (id_24543 쟁의행위, id_24693/24839/25293 사직, id_24699 근로조건 위반, id_25025 징계사유 부존재)
2. **징계사유 인정 + 양정 과다**: 10건 — disciplinary_severity의 전형
3. **복합 비위 해고 정당**: 7건 — misconduct의 전형
4. **절차 하자 결정적**: 2건 (id_2491 괴롭힘 가해자 위원장, id_25091 재심위원회 구성)
5. **징계형평 위반**: 3건 (id_24833, id_24849, id_2537) — 쌍방폭행에서 일방만 중징계

### exclusion_flags 사용
- resignation_dispute: 3건 (사직 자발성 사건)
- unrelated_to_dismissal: 4건
- fact_specific_low_reusability: 2건
- not_really_performance_case: 3건

### confidence 분포
- high: 29건
- medium: 1건 (id_24577 노동조합 내부 징계 특수 사건)
