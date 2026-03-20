# probation_batch_009_reviewed.jsonl 1차 self-review 메모

## 배치 요약
- 총 30건 처리
- **rejection_of_regular_employment** (본채용 거부): 18건
- **probation_termination** (수습기간 중 해고): 4건
- **unrelated_to_probation** (수습 무관): 6건
- 기타 (해고 부존재/합의해지 등): 2건

## disposition_type 분류 기준

### rejection_of_regular_employment (18건)
수습/시용기간 만료 시점에 본채용을 거부하거나, 수습평가를 근거로 유보된 해약권을 행사한 경우.
- 정당 판정: id_22263, id_22483, id_2267, id_22759, id_22983, id_23111, id_23271, id_23305, id_23379, id_23555, id_23703
- 부당 판정: id_22195, id_2289, id_22709, id_22799, id_23343, id_23521
- 구제이익 없음: id_23445

### probation_termination (4건)
수습/시용기간 도중(만료 전) 해고된 경우.
- id_22869: 시용 택시기사 과속운행 등 — 기간 중 계약해지
- id_23179: 시용기간 중 폭행·무단결근
- id_23447: 수습기간 중 사용자 지시 거부·재산 침해
- id_23631 (근로자1): 시용기간 중 관리소장 해고

### unrelated_to_probation (6건)
수습 태그가 있으나 실질 쟁점이 수습/시용과 무관한 경우.
- id_22267: 시용 후 기간제 계약 → 갱신기대권 쟁점
- id_22879: 채용내정 정규직 → 인턴 일방변경 → 해고사유·절차 부당
- id_22933: 비수습자를 수습 취급하여 징계절차 생략
- id_22981: 수습 중이었으나 구두해고 존부만 다툼
- id_23257: 촉탁직 기간제 계약만료 (수습 운용 사례 없음)
- id_2345: 수습 완료 후 정규직 직권면직

## 주요 판단 메모

### id_22195
- primary: dismissal_validity, disposition: rejection_of_regular_employment
- 수습평가 객관성 부족(작성주체·시기 문제), 코칭 부재, 사후 확인서 → 부당
- id_2289와 유사 패턴 (평가기준 미교육·비계량화)

### id_22267
- employment_stage를 fixed_term으로 변경
- 시용기간은 이미 종료, 그 후 기간제 계약을 별도 체결. 쟁점은 갱신기대권
- exclusion_flags: unrelated_to_probation, renewal_expectation_dominant

### id_22799
- 핵심: 1차 경고 후 성적 향상에도 2차 경고 발부, 동일 경고받은 타 근로자는 근무 중
- comparative_fairness가 판단에 결정적
- sanction_type이 원본에서 warning으로 되어 있으나, 실질은 채용취소(=본채용 거부)

### id_22869
- 복합 판정 사건: 견책 정당 + 배차정지 부당 + 시용해고 정당 + 부당노동행위 불인정
- disposition에 probation_termination + suspension 병기

### id_22879
- 마이스터고 채용내정 → 정규직 근로계약 성립 인정
- 군 복무 후 인턴으로 일방 변경은 무효
- 수습/인턴 형태였지만 실질은 정규직. unrelated_to_probation

### id_22933
- "수습기간이 적용되는 신규입사자로 볼 수 없음"이 핵심 판단
- 비수습자에게 수습 적용하여 징계절차 생략 → 절차 하자
- employment_stage: regular, unrelated_to_probation

### id_22981
- 수습기간 중이었으나 해고 자체의 존부만 다툼
- 구두해고 입증자료 전무 → 해고 부존재
- 수습 관련 실체적 판단 없음. unrelated_to_probation

### id_23257
- 수습 실제 운용 사례 없음, 수습면제 규정 존재, 정년초과자
- 촉탁직 기간제 계약으로 판단 → 계약만료 종료
- unrelated_to_probation

### id_23343
- 성희롱 피해 신고 후 수습기간 종료 2일 전 해고
- retaliation이 primary — 성희롱 가해자(부원장)가 피해자에게 퇴직 통보
- 수습평가 미실시 절차 하자도 존재

### id_2345
- 수습기간 마침 + 계약 갱신 완료 → 정규직 상태
- 직권면직 사유(업무능력 부족) 미입증으로 부당
- unrelated_to_probation (수습은 이미 완료)

### id_23445
- 구제이익 소멸 사안. 복직명령 진정성 인정
- 수습 본채용 거부의 실체적 판단까지 가지 않음
- confidence: medium (구제이익 쟁점으로 수습 태깅 재활용성 낮음)

## confidence 분포
- high: 29건
- medium: 1건 (id_23445 — 구제이익 쟁점, 수습 태깅 재활용성 낮음)
