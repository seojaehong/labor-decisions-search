# misconduct_remaining_batch_148_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_148_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_7261` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 향된 인사명령인 강임은 구제신청 대상이고, 업무상 필요성이 인정되지 않아 부당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_7263` [disciplinary_severity]
  - 변경: notes
  - notes: 검찰의 통보로 인해 추가 확인된 부하직원의 업무상 횡령과 관련하여 실무책임자인 근로자에 대한 징계사유가 모두 인정되고, 직전 징계와 구체적인 징
- `id_7279` [misconduct]
  - 변경: notes
  - notes: 징계사유가 모두 인정되지 않아 해고가 부당하다고 판정한 사례 — 비위사실이 명확히 인정되어 해고 정당성 직접 좌우
- `id_7305` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정과 절차에 하자가 있다고 볼 수 없어 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_7309` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 일부가 인정되나 징계양정이 과도하고 취업규칙의 징계절차를 준수하지 않아 징계가 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
