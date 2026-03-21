# misconduct_remaining_batch_120_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_120_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_5103` [procedure]
  - 변경: notes
  - notes: 징계사유의 일부만 인정되고, 징계양정이 과도하여 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_51045` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정이 과하지 않으며 징계절차상 하자가 존재한다고 보기 어려워 취업정지 1개월 징계처분이 정당하다고 판정한 사례 — 비위
- `id_5105` [disciplinary_severity]
  - 변경: notes
  - notes: 계사유가 인정되고, 징계양정도 적정하며, 징계절차에도 하자가 없어 징계가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_51051` [disciplinary_severity]
  - 변경: notes
  - notes: 사무실 밖에서 자신의 핸드폰을 던져 파손한 행위를 제외한 나머지는 징계사유로 인정되나 비교적 경미한 잘못으로 징계양정이 과하다고 판정한 사례 —
- `id_51055` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 징계사유가 모두 인정되고 징계양정도 적정하며 징계절차에 하자가 없어 정당한 해고라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
