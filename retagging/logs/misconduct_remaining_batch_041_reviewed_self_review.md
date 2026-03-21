# misconduct_remaining_batch_041_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_041_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_33573` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 해임처분이 징계사유에 비하여 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_33607` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 정당하고, 양정이 적정하는 등 징계는 정당하고, 보조기사 배치는 이중징계로 보기 어렵다고 판정한 사례 — 징계양정(제재 수위)의 적정
- `id_33621` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정 또한 징계권자에게 맡겨진 징계재량권을 남용하였다고 볼 수 없으며, 징계절차상 하자도 없으므로 정당하다고 판정한 사
- `id_33637` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 징계사유가 일부 인정되고, 징계의 절차적 정당성은 인정되나 징계양정에 있어서 그 정당성을 인정하기 어려워 부당해고로 판정한 사례 
- `id_33639` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 서손(무효)수표 분실, 온누리상품권 착오 발급, 파출수납 후 당일 미입금, 파출수납 중 근무지 이탈 등의 징계사유는 징계면직(해고)에 이를 정도

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
