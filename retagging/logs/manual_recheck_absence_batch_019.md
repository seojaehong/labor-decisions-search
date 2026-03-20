# absence_batch_019 manual recheck

- 작성시각: 2026-03-20 22:21
- 목적: 자동 생성 draft를 최종본으로 쓰지 않고, 사용자 프롬프트 기준으로 케이스별 수동 판정을 먼저 고정
- 원칙: `issue_type_primary`는 실제 위원회 판단구조 기준, absence는 핵심일 때만 primary

| case_id | primary | secondary | disposition | exclusion_flags | confidence | 메모 |
|---|---|---|---|---|---|---|
| id_26243 | transfer_validity | dismissal_validity | transfer, dismissal | not_really_absence_case | high | 결근은 부당전보와 해고의 파생 결과일 뿐, 중심은 전보 정당성 |
| id_26253 | procedure | worker_status, dismissal_validity | dismissal | not_really_absence_case, procedure_dominant | high | 근로자성 판단이 선결되지만 결론은 서면통지 흠결에 의한 부당해고 |
| id_26323 | procedure | dismissal_validity | disciplinary_dismissal | not_really_absence_case, procedure_dominant | high | 해고 존재와 제척기간 문제를 거친 뒤 결론은 절차 위반으로 종결 |
| id_2637 | transfer_validity | attendance | transfer | not_really_absence_case, unrelated_to_dismissal | high | 근태불량은 전보 대상자 선정 사유일 뿐, 핵심은 부당전보 |
| id_26461 | disciplinary_severity | misconduct, retaliation | suspension | not_really_absence_case, unrelated_to_dismissal | high | 일부 비위는 인정되나 정직이 과중한지가 핵심 |
| id_26547 | procedure | dismissal_validity | no_formal_disposition | not_really_absence_case, resignation_dispute, procedure_dominant | high | 결근 자체보다 해고 존재와 서면통지 위반이 중심 |
| id_26615 | disciplinary_severity | misconduct | suspension | not_really_absence_case, unrelated_to_dismissal | high | 복합 비위에 대한 정직 2월의 양정 적정성이 핵심 |
| id_26673 | absence_without_leave | disciplinary_severity, procedure | dismissal |  | high | 장기 무단결근이 직접 해고사유이고 절차도 적법하다고 본 전형 사례 |
| id_26681 | disciplinary_severity | misconduct, attendance | suspension, reprimand | not_really_absence_case, unrelated_to_dismissal | high | 업무태만과 지시불이행 중심의 정직 1월 적정성 사건 |
| id_26711 | disciplinary_severity | misconduct | dismissal | not_really_absence_case | high | 징계사유 일부 인정 전제로 해고 양정 과다 여부가 핵심 |
| id_26729 | dismissal_validity |  | no_formal_disposition | not_really_absence_case, unrelated_to_dismissal | high | 해고 존재 또는 구제이익 존부가 핵심이며 결근은 사용자의 반박 사유 |
| id_26751 | dismissal_validity | procedure | dismissal | not_really_absence_case | high | 복직명령의 진정성으로 구제이익이 소멸했는지가 중심 |
| id_26781 | unfair_treatment | disciplinary_severity, retaliation, transfer_validity | rejection_of_regular_employment, suspension, pay_cut | not_really_absence_case, unrelated_to_dismissal | medium | 여러 근로자와 여러 처분이 결합된 복합 사건으로 absence는 부수적 |
| id_26787 | disciplinary_severity | absence_without_leave, misconduct, procedure | dismissal | not_really_absence_case | high | 무단결근과 폭행이 인정되나 핵심 판단은 해고 양정과 절차 적법성 |
| id_26825 | dismissal_validity | absence_without_leave | no_formal_disposition | not_really_absence_case, unrelated_to_dismissal | high | 해고가 있었는지 여부가 중심이고 결근은 오인에 따른 후속 사정 |
| id_26863 | disciplinary_severity | misconduct | pay_cut | not_really_absence_case, unrelated_to_dismissal | high | 연차 불승인 후 귀가와 협박 언행에 대한 감급 양정의 적정성 사건 |
| id_26879 | dismissal_validity |  | no_formal_disposition | not_really_absence_case, resignation_dispute, unrelated_to_dismissal | high | 퇴직원이 비진의인지 여부가 핵심인 사직 분쟁 |
| id_26885 | disciplinary_severity | attendance | dismissal | not_really_absence_case | high | 지속적 근태불량과 민원 등 복합 사유에 대한 해고 양정이 중심 |
| id_26911 | dismissal_validity |  | no_formal_disposition | not_really_absence_case, unrelated_to_dismissal | high | 해고 존재 및 복직명령 철회 효력으로 구제이익이 소멸했는지 판단 |
| id_26947 | disciplinary_severity | misconduct, procedure | disciplinary_dismissal | not_really_absence_case | high | 일부 사유만 인정되는 상황에서 징계해고 양정 과다 여부가 중심 |
| id_26985 | dismissal_validity |  | no_formal_disposition | not_really_absence_case, unrelated_to_dismissal | high | 복귀명령과 출근 사실로 해고가 부정되는 구제이익 사건 |
| id_27041 | procedure | dismissal_validity | dismissal | not_really_absence_case, procedure_dominant | high | 5인 이상 사업장 판단 후 결론은 해고 서면통지 위반 |
| id_2707 | dismissal_validity |  | no_formal_disposition | not_really_absence_case, unrelated_to_dismissal | high | 원직복직 명령으로 구제이익이 소멸했는지가 핵심 |
| id_27139 | absence_without_leave | dismissal_validity | dismissal |  | high | 병가 가능성과 보고 경위 때문에 무단결근으로 볼 수 있는지가 핵심 |
| id_27165 | procedure | dismissal_validity | dismissal | not_really_absence_case, procedure_dominant | high | 결근 언급은 있으나 실제 결론은 해고 존재와 서면통지 위반 |
| id_2717 | absence_without_leave | procedure | dismissal |  | high | 1개월 이상 무단결근이 직접 핵심 징계사유이고 절차 하자도 부정 |
| id_27177 | disciplinary_severity | misconduct, attendance | disciplinary_dismissal | not_really_absence_case | high | 비위는 인정되나 징계해고가 과중하다는 양정 사건 |
| id_27239 | procedure | dismissal_validity | suspension | not_really_absence_case, procedure_dominant, unrelated_to_dismissal | high | 승무정지 처분 존재와 징계절차 위반이 핵심 |
| id_27267 | absence_without_leave | disciplinary_severity, procedure | dismissal |  | high | 2개월간 반복 무단결근이 직접 해고사유인 전형 사례 |
| id_27275 | misconduct | dismissal_validity | disciplinary_dismissal | not_really_absence_case | high | 조직갈등·차별대우 주장에 대한 비위 입증 부족이 핵심 |

## 메모

- 기존 draft에서 특히 잘못 잡힌 케이스:
  - `id_26243`: absence -> transfer_validity
  - `id_26323`: misconduct -> procedure
  - `id_26673`: not_really_absence_case 제거 필요
  - `id_26751`: absence -> reinstatement/구제이익 구조
  - `id_27267`: procedure -> absence_without_leave
- 다음 단계:
  - 위 판정을 기준으로 `output/reviewed/absence_batch_019_reviewed.jsonl` 수동 재작성
  - 이어서 `absence_batch_019_self_review.md`를 이 분포 기준으로 갱신
