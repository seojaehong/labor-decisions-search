# misconduct_remaining_batch_074_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_074_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_403345` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 업무총괄자로서 관리책임 부실 등의 징계사유가 존재하고 징계양정이 재량권을 일탈ㆍ남용하였다고 볼 만한 사정이 없으며, 징계절차를 준수하여 정당하다
- `id_403355` [disciplinary_severity]
  - 변경: notes
  - notes: 허위보고 등으로 거액의 미수금을 발생시킨 비위행위에 대한 징계해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_403369` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정이 과도하다고 볼 수 없으며, 징계절차상 하자도 없으므로 정직 처분은 정당하다고 판정한 사례 — 비위 인정이나 해고
- `id_403377` [disciplinary_severity]
  - 변경: notes
  - notes: 횡령의 징계사유가 존재하고, 근로자의 비위행위가 중하므로 양정이 과도하지 않으며, 징계절차에도 하자가 없어 해고가 정당하다고 판정한 사례 — 비
- `id_40339` [disciplinary_severity]
  - 변경: notes
  - notes: 인정 - 근로자가 출무점검표 등에 서명거부, 관리자에게 반말·폭언, 소속 조합원들의 서명거부 및 농성 선동을 한 것은 징계사유로 인정되나, 징계

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
