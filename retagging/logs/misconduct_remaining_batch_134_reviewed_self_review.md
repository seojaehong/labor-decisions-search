# misconduct_remaining_batch_134_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_134_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_56983` [workplace_harassment]
  - 변경: notes
  - notes: 징계사유와 징계절차에 하자는 없으나 인정되는 징계사유에 비해 징계양정이 과도하여 부당하다고 판정한 사례 — 직장 내 괴롭힘 성립 여부가 핵심
- `id_56987` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 직무태만 및 팀장 지시를 불이행한 노조 간부에 대하여 직위해제 및 정직 3개월의 징계처분을 한 것은 정당하고, 부당노동행위는 존재하지 않는다고 
- `id_5699` [misconduct]
  - 변경: notes
  - notes: 징계사유를 인정할 수 없으므로 감봉처분은 부당하다고 판정한 사례 — 비위사실 자체의 입증 여부가 결론을 좌우
- `id_56997` [unfair_treatment]
  - 변경: notes
  - notes: 해고사유가 모두 인정되고 절차도 적법하고 임직원 대상 고소·고발 등을 고려할 때 양정이 과도하다고 보기 어렵고, 해고가 사용자의 부당노동행위 의
- `id_57017` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정이 적정하며 징계절차상 하자도 없어 징계해고 처분이 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
