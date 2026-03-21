# misconduct_remaining_batch_072_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_072_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_402493` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 절차는 정당하나, 징계양정이 과하여 정직이 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_402495` [misconduct]
  - 변경: notes
  - notes: 병가 및 근무협조 부당사용으로 인한 직위해제의 업무상 필요성이 인정되고, 생활상 불이익이 근로자들이 감내하기 어려울 정도라고 보기 어려워, 직위
- `id_40253` [misconduct]
  - 변경: notes
  - notes: 사용자 주장하는 7가지 징계사유 중 근로자가 신탁투자를 의뢰한 회사의 사이외사로 선임됨에 있어 이사장 결재 없이 선임되는 등 6가지는 인정되나,
- `id_402535` [disciplinary_severity]
  - 변경: notes
  - notes: 각 인사명령(소환명령, 면보직, 대기명령)에 대한 부당해고 등 구제신청기간(통지일부터 3개월)이 지나 구제신청을 제기하여 각하 사유에 해당하며,
- `id_402545` [disciplinary_severity]
  - 변경: notes
  - notes: 부적절한 내용의 이메일을 다수 직원들에게 보낸 행위 등이 징계사유로 인정되나 정직 2월의 징계는 양정이 과하여 부당하다고 판정한 사례 — 징계양

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
