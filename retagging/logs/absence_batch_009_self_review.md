# absence_batch_009_reviewed.jsonl 1차 self-review 메모

## 통계 요약
- 총 건수: 30건
- 진정한 무단결근/결근 사례 (exclusion_flags 없음): 8건
- not_really_absence_case 플래그 부여: 19건
- resignation_dispute만 부여 (결근 자체는 핵심이나 퇴직 존부 쟁점): 3건

## 진정한 무단결근 핵심 사례 (8건)

### id_1807
- primary: absence_without_leave / disposition: ['disciplinary_dismissal']
- 28일 무단결근 + 동료 폭언 → 징계해고 정당
- 무단결근이 핵심 징계사유로 명확

### id_18077
- primary: absence_without_leave / disposition: ['suspension']
- 휴무 불승인 무시 결근 → 정직 5일 정당
- 운수업 특성 반영, 무단결근이 직접적 징계사유

### id_18093
- primary: procedure / disposition: ['dismissal']
- 근태불량 해고사유 정당하나 구두해고 → 서면통지 절차위반
- 무단결근이 해고사유이나 절차 쟁점이 결론을 좌우

### id_18099
- primary: absence_without_leave / disposition: ['dismissal']
- 병가 7회 반송 후 무단결근 처리 → 부당해고
- 결근 귀책이 사용자에게 있는 특수 사례

### id_18353
- primary: absence_without_leave / disposition: ['dismissal']
- 무단결근 4일이 유일 인정 해고사유이나 양정 과다
- 사용자 사전 협의 미비에 기인

### id_18369
- primary: absence_without_leave / disposition: ['dismissal']
- 정직 후 복직 → 업무 미이행·무단이탈 반복 → 해고 정당

### id_18401
- primary: absence_without_leave / disposition: ['dismissal']
- 질책 반발 후 장기 출근거부 → 해고 정당

### id_17975
- primary: dismissal_validity (자진퇴직 판단이 핵심)
- 무단결근 + 타 사업장 근무 → 자진퇴직 인정
- 결근이 핵심 근거이나 resignation_dispute 플래그

## not_really_absence_case 부여 사례 (19건)

### id_17879 — 자진퇴사 간주 해고 존부 + 서면통지 위반
### id_17909 — 폭언·폭행 징계양정이 핵심, 무단결근은 과거 전력
### id_17977 — 구제신청 의사 포기 각하, 무단결근은 배경
### id_18001 — 부당전보 불응 출근거부, 전보 정당성이 핵심
### id_18009 — 보정요구 불응 각하, 무단결근은 보충 판단
### id_18019 — 성추행이 핵심 징계사유, 무단결근 3일은 부수적
### id_18023 — '그만두겠다' 발언 + 퇴직금 청구 → 해고 존부
### id_18039 — 기간제 계약만료 해고 존부, 무단이탈은 보조적
### id_18041 — 운행질서 위반 34회 등 다수 비위, 무단결근은 일부
### id_18049 — 연락두절 자발적 퇴직 인정, 해고 존부 쟁점 (resignation_dispute)
### id_18121 — 상사 폭행 양정 과다, 근태불량은 부수 사유
### id_18237 — 업무태만 정직 양정 과다, 무단결근은 비교 사례로만 등장
### id_18243 — 외국인 근로자 고용변동신고 해고 존부
### id_1827 — 승무정지 처분 존부, 결근은 자발적 미복귀
### id_18311 — 경비유용 양정 과다, 무단결근은 증거 부족 불인정
### id_18321 — 갱신기대권 존부, 결근은 평가 항목 중 하나
### id_18337 — 갱신기대권 + 평가 부당, 근태불량은 미입증
### id_18341 — 업무지시 불이행 징계해고, 근태불량은 불인정
### id_18351 — 병가 중 당연퇴직 처리 해고 존부 + 서면통지 위반
### id_18367 — 겸업금지 위반 양정 과다 + 절차 위반
### id_18403 — 쟁의행위 한계 일탈 징계, 무단이탈은 파업 참여로 불인정

## 판단 근거 정리

| 구분 | 기준 |
|------|------|
| 진정한 결근 사례 | 무단결근/출근거부 자체가 징계사유의 핵심이거나 유일한 인정 사유 |
| not_really_absence_case | 무단결근이 (1) 배경사실에 불과, (2) 징계사유로 불인정, (3) 다른 쟁점이 결론을 지배 |
| resignation_dispute | 결근 상태가 자진퇴직/해고 존부 판단의 근거이나 결근 '징계'가 아닌 경우 |

## 주의 사항
- id_18093: 무단결근 해고사유는 정당하나 primary를 procedure로 태깅 — 절차위반이 최종 결론을 좌우하므로 적절
- id_17975: 자진퇴직 판정이므로 primary는 dismissal_validity이나, 무단결근이 자진퇴직 판단의 핵심 근거이므로 exclusion_flags에 not_really_absence_case 미부여
- id_18099: 병가 불승인 → 무단결근 → 해고 패턴은 사용자 귀책 무단결근의 대표 사례
