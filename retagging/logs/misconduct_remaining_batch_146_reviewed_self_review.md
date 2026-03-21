# misconduct_remaining_batch_146_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_146_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_6435` [procedure]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정직 14일의 처분은 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론
- `id_6473` [unfair_treatment]
  - 변경: notes
  - notes: 사고 다발 근로자에 대하여는 징계의 사유, 양정, 절차가 모두 정당하고, 운행 중 흡연, 노동조합 홍보물 게시 등과 관련한 근로자들의 징계에 대
- `id_6477` [unfair_treatment]
  - 변경: notes
  - notes: 업무지시 거부 및 감사 거부의 징계사유가 일부 인정되나 징계양정이 과하므로 감봉처분은 부당징계에 해당하나, 이러한 감봉처분이 불이익 취급 및 지
- `id_6479` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계양정도 적정하며 징계절차에 하자도 없어 징계가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 
- `id_649` [unfair_treatment]
  - 변경: notes
  - notes: 견책은 징계사유가 인정되고, 양정도 적정하며 절차에도 하자가 없어 정당하며, 불이익 취급의 부당노동행위에 해당하지 않는다고 판정한 사례 — 부당

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
