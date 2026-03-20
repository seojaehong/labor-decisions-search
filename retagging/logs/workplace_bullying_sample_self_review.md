# workplace_bullying_sample_output.jsonl 1차 self-review 메모

## 1. primary/secondary가 가장 흔들린 사례

- **id_10075**: 괴롭힘이 반복 비위의 일부이지만 판정 중심은 누적 징계 후 해고 양정의 정당성이라 `workplace_harassment`보다 `disciplinary_severity`가 더 적합했음.
- **id_10281**: 표면상 신고 후 보복 사건이라 `retaliation`을 쓰고 싶지만 v1 primary enum에는 없어 `unfair_treatment`로 흡수해야 했음.
- **id_10345**: 괴롭힘 성립은 인정되지만 결론 중심은 해임의 과다 여부여서 `workplace_harassment`와 `disciplinary_severity` 경계가 흔들렸음.
- **id_10647**: 괴롭힘 조사 후 행위자 분리 전보 사건인데 `transfer_validity`를 primary로 두고 싶어도 v1 primary enum에는 없어 `unfair_treatment`로 처리함.

## 2. 괴롭힘 성립 vs 조사/보복/징계 경계 사례

- **id_10111**: 괴롭힘 신고는 배경이고 실제 핵심은 쌍방폭행 감봉의 형평성·양정 문제라 `disciplinary_severity` 유지, 신고 관련은 secondary의 `harassment_report`로 낮춤.
- **id_10281**: 괴롭힘 성립 자체보다 신고 4일 후 전보라는 불이익 조치가 핵심이라 `unfair_treatment` 중심으로 처리.
- **id_10485**: 괴롭힘이 직위해제 사유로 주장됐지만 실질은 사유 입증·통지 구조 문제라 `procedure`로 보정.
- **id_10721**: 괴롭힘 신고 후 전보·사직권유가 배경이지만 결론은 사직의 진정성/해고 부존재라 `dismissal_validity` 유지.
- **id_10295**: 괴롭힘 행위자에 대한 분리 전보+징계해고 사건으로, 보복이 아니라 보호조치/행위자 조치의 정당성 사례였음.

## 3. enum 밖 값 유입 사례

- `issue_type_primary`: `retaliation`, `transfer_validity`
- `issue_type_secondary`: `retaliation`
- `fact_markers`: `investigation_conducted`, `public_institution`
- `legal_focus`: `duty_of_investigation`
- `exclusion_flags`: `unrelated_to_harassment`
- `industry_context`: `education`

## 4. v1 유지 가능 규칙 / v1.1 후보 규칙

### v1 유지 가능 규칙
- 괴롭힘이 언급되어도 결론 중심이 징계양정이면 `disciplinary_severity`를 primary로 두는 방식은 유지 가능.
- 신고 후 불이익 주장이 있어도 실제로 배척되거나 배경사실이면 `harassment_report` secondary만으로도 상당 부분 대응 가능.
- 해고 부존재/사직 효력 사건은 괴롭힘 배경이 있어도 `dismissal_validity` + `no_formal_disposition`으로 정리 가능.
- 순수 행위자 징계 사건은 `workplace_harassment` primary를 유지해도 무리 없음.

### v1.1 후보 규칙
- `retaliation`을 primary enum으로 별도 추가할지 검토 필요. 현재는 `unfair_treatment`로 우회해야 해상도가 떨어짐.
- `transfer_validity`를 primary enum으로 허용할지 검토 필요. 괴롭힘 조사 후 분리전보/보복전보 사건에서 유용함.
- `duty_of_investigation` 또는 조사·보호조치 관련 legal_focus 보강 필요.
- `investigation_conducted`는 사실관계상 자주 중요하므로 fact_marker로 승격할지 검토 가치가 있음.

## 5. 개별 수정 내역

### id_10015
- 변경 전 primary/disposition: misconduct / ['disciplinary_dismissal']
- 변경 후 primary/disposition: misconduct / ['disciplinary_dismissal']
- 변경 전 secondary: ['workplace_harassment', 'disciplinary_severity']
- 변경 후 secondary: ['disciplinary_severity']
- 변경 전 fact_markers: ['investigation_conducted', 'witness_statement', 'prior_sanction_history', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['witness_statement', 'prior_sanction_history', 'disciplinary_committee', 'evidence_sufficient']
- 변경 이유: 성희롱 성격이 강해도 사용자-부하 관계에서 반복된 괴롭힘 징계사건으로 검색 가치가 있어 not_really_harassment_case는 제거. investigation_conducted는 v1 fact_marker 밖이라 제거.

### id_10075
- 변경 전 primary/disposition: misconduct / ['disciplinary_dismissal']
- 변경 후 primary/disposition: disciplinary_severity / ['disciplinary_dismissal']
- 변경 전 secondary: ['workplace_harassment', 'disciplinary_severity']
- 변경 후 secondary: ['disciplinary_severity']
- 변경 전 fact_markers: ['prior_sanction_history', 'investigation_conducted', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['prior_sanction_history', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 이유: 괴롭힘이 반복 비위의 일부이지만 판정 중심은 누적 징계 후 해고 양정의 정당성이므로 disciplinary_severity로 보정. investigation_conducted 제거.

### id_10111
- 변경 전 primary/disposition: disciplinary_severity / ['pay_cut']
- 변경 후 primary/disposition: disciplinary_severity / ['pay_cut']
- 변경 전 secondary: ['retaliation', 'workplace_harassment']
- 변경 후 secondary: ['harassment_report']
- 변경 전 fact_markers: ['harassment_report_filed', 'investigation_conducted', 'comparative_employee_case', 'disciplinary_committee']
- 변경 후 fact_markers: ['harassment_report_filed', 'comparative_employee_case', 'disciplinary_committee']
- 변경 이유: retaliation은 v1 secondary enum 밖이므로 harassment_report로 보정. 신고 후 불이익 주장은 배척되어 primary는 disciplinary_severity 유지.

### id_10281
- 변경 전 primary/disposition: retaliation / ['transfer']
- 변경 후 primary/disposition: unfair_treatment / ['transfer']
- 변경 전 secondary: ['transfer_validity', 'workplace_harassment']
- 변경 후 secondary: ['transfer_validity', 'harassment_report']
- 변경 전 fact_markers: ['harassment_report_filed', 'evidence_insufficient']
- 변경 후 fact_markers: ['harassment_report_filed', 'evidence_insufficient']
- 변경 이유: retaliation은 v1 primary enum 밖이라 unfair_treatment로 흡수. 괴롭힘 신고 후 보복성 전보 사건의 실질을 반영.

### id_10295
- 변경 전 primary/disposition: workplace_harassment / ['disciplinary_dismissal', 'transfer']
- 변경 후 primary/disposition: workplace_harassment / ['disciplinary_dismissal', 'transfer']
- 변경 전 secondary: ['transfer_validity', 'disciplinary_severity']
- 변경 후 secondary: ['transfer_validity', 'disciplinary_severity']
- 변경 전 fact_markers: ['investigation_conducted', 'harassment_report_filed', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['harassment_report_filed', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 이유: duty_of_investigation과 investigation_conducted는 v1 enum 밖이라 제거. 분리조치 정당성은 notes와 transfer_validity secondary로 유지.

### id_10325
- 변경 전 primary/disposition: disciplinary_severity / ['suspension']
- 변경 후 primary/disposition: disciplinary_severity / ['suspension']
- 변경 전 secondary: ['misconduct']
- 변경 후 secondary: ['misconduct']
- 변경 전 fact_markers: ['disciplinary_committee', 'comparative_employee_case', 'prior_sanction_history']
- 변경 후 fact_markers: ['disciplinary_committee', 'comparative_employee_case', 'prior_sanction_history']
- 변경 이유: unrelated_to_harassment는 v1 exclusion enum 밖이라 제거. not_really_harassment_case만으로 충분.

### id_10345
- 변경 전 primary/disposition: workplace_harassment / ['disciplinary_dismissal']
- 변경 후 primary/disposition: disciplinary_severity / ['disciplinary_dismissal']
- 변경 전 secondary: ['disciplinary_severity']
- 변경 후 secondary: ['disciplinary_severity']
- 변경 전 fact_markers: ['investigation_conducted', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient', 'public_institution']
- 변경 후 fact_markers: ['witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 이유: 괴롭힘은 인정되지만 결론 중심은 해임 양정 과다이므로 disciplinary_severity로 보정. enum 밖 fact_marker 제거.

### id_1035
- 변경 전 primary/disposition: workplace_harassment / ['disciplinary_dismissal']
- 변경 후 primary/disposition: workplace_harassment / ['disciplinary_dismissal']
- 변경 전 secondary: ['misconduct', 'disciplinary_severity']
- 변경 후 secondary: ['misconduct', 'disciplinary_severity']
- 변경 전 fact_markers: ['investigation_conducted', 'evidence_sufficient', 'prior_sanction_history']
- 변경 후 fact_markers: ['evidence_sufficient', 'prior_sanction_history']
- 변경 이유: investigation_conducted는 v1 fact_marker 밖이라 제거.

### id_10437
- 변경 전 primary/disposition: workplace_harassment / ['suspension']
- 변경 후 primary/disposition: workplace_harassment / ['suspension']
- 변경 전 secondary: ['disciplinary_severity']
- 변경 후 secondary: ['disciplinary_severity']
- 변경 전 fact_markers: ['investigation_conducted', 'disciplinary_committee', 'evidence_sufficient', 'public_institution']
- 변경 후 fact_markers: ['disciplinary_committee', 'evidence_sufficient']
- 변경 이유: investigation_conducted/public_institution는 v1 fact_marker 밖이라 제거.

### id_10467
- 변경 전 primary/disposition: misconduct / ['suspension']
- 변경 후 primary/disposition: misconduct / ['suspension']
- 변경 전 secondary: ['workplace_harassment', 'disciplinary_severity']
- 변경 후 secondary: ['disciplinary_severity']
- 변경 전 fact_markers: ['investigation_conducted', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['disciplinary_committee', 'evidence_sufficient']
- 변경 이유: 괴롭힘은 복수 비위 중 하나이므로 misconduct primary 유지. investigation_conducted 제거.

### id_10485
- 변경 전 primary/disposition: unfair_treatment / ['suspension']
- 변경 후 primary/disposition: procedure / ['suspension']
- 변경 전 secondary: ['workplace_harassment']
- 변경 후 secondary: []
- 변경 전 fact_markers: ['evidence_insufficient', 'harassment_report_filed']
- 변경 후 fact_markers: ['evidence_insufficient', 'harassment_report_filed', 'procedural_defect']
- 변경 이유: 괴롭힘 언급보다 직위해제 사유 통지·입증 구조의 하자가 실질 중심이므로 procedure로 보정.

### id_10555
- 변경 전 primary/disposition: misconduct / ['disciplinary_dismissal']
- 변경 후 primary/disposition: misconduct / ['disciplinary_dismissal']
- 변경 전 secondary: ['workplace_harassment', 'absence_without_leave', 'disciplinary_severity']
- 변경 후 secondary: ['absence_without_leave', 'disciplinary_severity']
- 변경 전 fact_markers: ['unauthorized_absence', 'investigation_conducted', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['unauthorized_absence', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 이유: industry_context=education은 v1 enum 밖이라 service로 보정. investigation_conducted 제거.

### id_10647
- 변경 전 primary/disposition: transfer_validity / ['transfer']
- 변경 후 primary/disposition: unfair_treatment / ['transfer']
- 변경 전 secondary: ['workplace_harassment']
- 변경 후 secondary: ['transfer_validity', 'harassment_report']
- 변경 전 fact_markers: ['investigation_conducted', 'harassment_report_filed', 'evidence_sufficient']
- 변경 후 fact_markers: ['harassment_report_filed', 'evidence_sufficient']
- 변경 이유: transfer_validity는 v1 primary enum 밖이므로 unfair_treatment primary로 흡수. 이 사건은 행위자 분리조치의 정당성 판단으로, 보복이 아니라 보호조치/인사조치 정당성 사건임.

### id_10717
- 변경 전 primary/disposition: workplace_harassment / ['pay_cut']
- 변경 후 primary/disposition: workplace_harassment / ['pay_cut']
- 변경 전 secondary: ['disciplinary_severity', 'procedure']
- 변경 후 secondary: ['disciplinary_severity', 'procedure']
- 변경 전 fact_markers: ['investigation_conducted', 'witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 후 fact_markers: ['witness_statement', 'disciplinary_committee', 'evidence_sufficient']
- 변경 이유: 괴롭힘 감봉 징계와 절차 논점 사건으로 v1 내 분류 가능. investigation_conducted 제거.

### id_10721
- 변경 전 primary/disposition: dismissal_validity / ['dismissal']
- 변경 후 primary/disposition: dismissal_validity / ['no_formal_disposition']
- 변경 전 secondary: ['retaliation', 'transfer_validity']
- 변경 후 secondary: ['transfer_validity', 'harassment_report', 'unfair_treatment']
- 변경 전 fact_markers: ['harassment_report_filed', 'resignation_dispute']
- 변경 후 fact_markers: ['harassment_report_filed', 'resignation_dispute']
- 변경 이유: retaliation은 v1 secondary enum 밖이라 harassment_report/unfair_treatment로 분해. 해고 부존재 사건이므로 disposition_type을 no_formal_disposition으로 보정.

