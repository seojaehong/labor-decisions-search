# misconduct_remaining_batch_105_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_105_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_45109` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자는 주취 상태였음을 사유로 상사에 대해 모욕적인 언행을 하였다는 징계사유를 부인하나, 피해자 및 목격자의 일관되고 구체적인 진술을 고려하여
- `id_4511` [unfair_treatment]
  - 변경: notes, secondary:['misconduct']→['misconduct', 'procedure', 'disciplinary_severity']
  - notes: 기각- 폭언 등 징계사유가 인정되고, 양정이 과하지 않으며, 절차에 위법이 없어 징계가 정당하며, 불이익 취급의 부당노동행위에 해당하지 않는다고
- `id_45111` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고 징계절차도 하자가 없으며 징계양정도 과하지 않다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_45113` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계양정이 과도하지 않으며 징계절차에 하자가 없어 정직 3개월의 징계처분은 정당하다고 판정한 사례 — 비위행위 존재 및 중대
- `id_45127` [misconduct]
  - 변경: notes
  - notes: 근로자와 사용자는 당사자 적격이 있고, 정당한 징계사유가 존재한다고 보기 어렵고 징계절차에 하자가 있으므로 징계해고는 부당하다고 판정한 사례 —

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
