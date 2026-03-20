# Retrieval Failure Analysis

## Q8 징계사유는 인정되지만 해고까지는 과하다고 본 사건

- query id: `Q12`
- 현재 실패 원인: disciplinary_severity 모집단 안에서 proportionality/appropriateness_of_discipline보다 단순 primary match와 text overlap이 먼저 작동해 각하·구제이익·비본질 사건이 섞였다.
- 현재 상위 결과 why surfaced:
  - `id_24205` `disciplinary_severity` | issue_type_primary, legal_focus x2, text overlap x4
  - `id_1989` `disciplinary_severity` | issue_type_primary, legal_focus x2, text overlap x3
  - `id_11561` `disciplinary_severity` | issue_type_primary, legal_focus x2, text overlap x2
  - `id_11595` `disciplinary_severity` | issue_type_primary, legal_focus x2, text overlap x2
  - `id_11735` `disciplinary_severity` | issue_type_primary, legal_focus x2, text overlap x2

## Q7 정규직 저성과/업무능력 부족 해고

- query id: `Q10`
- 현재 실패 원인: work_ability 자체는 잡지만 employment_stage=regular 우선이 없어 probation/본채용거부 구조가 섞일 수 있었다.
- 현재 상위 결과 why surfaced:
  - `id_17059` `work_ability` | employment_stage, issue_type_primary, fact_markers x1, text overlap x1
  - `id_22323` `work_ability` | employment_stage, issue_type_primary, fact_markers x1, text overlap x1
  - `id_43869` `work_ability` | employment_stage, issue_type_primary, fact_markers x1, text overlap x1
  - `id_46597` `work_ability` | employment_stage, issue_type_primary, fact_markers x1, text overlap x1
  - `id_347233` `work_ability` | issue_type_primary, fact_markers x2, text overlap x2

## Q2 무단결근 + 절차위반

- query id: `Q02`
- 현재 실패 원인: absence와 procedure가 동시에 필요한 질의인데, 현행 후보 랭킹은 issue_type_primary match 위주라 교차 구조를 강하게 보상하지 못했다.
- 현재 상위 결과 why surfaced:
  - `id_33381` `dismissal_validity` | issue_type_primary, fact_markers x1, text overlap x3
  - `id_33463` `procedure` | issue_type_primary, fact_markers x1, text overlap x3
  - `id_33393` `dismissal_validity` | issue_type_primary, fact_markers x1, text overlap x2
  - `id_18093` `procedure` | issue_type_primary, fact_markers x1, text overlap x2
  - `id_24749` `procedure` | issue_type_primary, fact_markers x1, text overlap x2

## Q4 괴롭힘 신고 후 보복성 인사조치

- query id: `Q05`
- 현재 실패 원인: retaliation/unfair_treatment 직접 회수보다 workplace_harassment나 일반 징계 사건이 같이 올라오고, 신고 이후 보복 구조를 랭킹이 충분히 반영하지 못했다.
- 현재 상위 결과 why surfaced:
  - `id_23343` `retaliation` | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2
  - `id_43973` `retaliation` | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2
  - `id_10995` `unfair_treatment` | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2
  - `id_11565` `unfair_treatment` | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2
  - `id_11929` `unfair_treatment` | issue_type_primary, fact_markers x1, legal_focus x1, text overlap x2

