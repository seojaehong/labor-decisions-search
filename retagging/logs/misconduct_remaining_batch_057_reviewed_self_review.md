# misconduct_remaining_batch_057_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_057_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_35369` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유는 인정되나 징계양정이 과중하고 징계절차에 하자가 있어 부당해고라고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_35381` [disciplinary_severity]
  - 변경: notes
  - notes: 기각근로자가 회사의 거래회사 주식을 매매하여 부당한 이득을 취득한 행위에 대하여 정직 6월은 정당하다고 판정한 사례 — 징계양정(제재 수위)의 
- `id_35403` [misconduct]
  - 변경: notes
  - notes: 징계사유에 비해 해고는 징계양정이 과하여 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_35417` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 업무지시를 거부한 것은 징계사유에 해당하고, 징계양정 또한 적정하며, 징계절차상 하자가 발견되지 않는다고 판정한 사례 — 징계·해고 절차 하자가
- `id_35423` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 사용자의 당사자 적격, 구제신청의 대상 적격 및 징계사유가 인정되고, 징계사유에 비해 징계양정이 과하다고 볼 수 없으며 징계절차상 하자도 없어 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
