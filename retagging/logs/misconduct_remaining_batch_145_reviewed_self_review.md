# misconduct_remaining_batch_145_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_145_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_61425` [misconduct]
  - 변경: notes, secondary:[]→['disciplinary_severity']
  - notes: 징계사유가 일부 인정되나, 인정되는 징계사유에 비해 파면의 징계는 양정이 과도하여 부당해고라고 판정한 사례 — 비위행위 존재 및 중대성이 해고 
- `id_61429` [misconduct]
  - 변경: notes
  - notes: 징계사유가 명백하고 인정되는 징계사유가 취업규칙상 감봉에 해당하여 징계가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직
- `id_61441` [unfair_treatment]
  - 변경: notes, secondary:['misconduct', 'disciplinary_severity']→['misconduct', 'procedure', 'disciplinary_severity'], conf:medium→high
  - notes: 징계사유가 인정되고 징계절차에 하자는 없으나, 해고는 징계사유에 비해 징계양정이 과하여 부당하고, 특별격려금 지급은 부당노동행위에 해당하나, 해
- `id_61459` [misconduct]
  - 변경: notes, secondary:[]→['disciplinary_severity', 'unfair_treatment']
  - notes: 노동조합이 조합원 2명에게 제명과 유기정권 3년을 각각 결의·처분한 것은 징계사유가 없고, 징계양정도 과하다고 판단하여 시정명령 의결요청을 인정
- `id_61463` [workplace_harassment]
  - 변경: notes
  - notes: 동료 근로자를 폭행한 행위와 이와 관련한 직장 내 괴롭힘, 퇴직한 동료 근로자에게 문자를 보낸 행위는 징계사유로 인정될 수 있으나 임신한 동료 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
