# misconduct_remaining_batch_099_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_099_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_42629` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 타워크레인 기사로서 과도한 월례비 요구를 관철하기 위해 비정상 작업으로 공사 지연시켰으므로 해고가 정당하다고 판정한 사례 — 징계·해고 절차 하
- `id_4263` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유는 인정되나 해고는 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_42637` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 무례한 태도, 근무시간 미준수, 서류 미제출은 징계사유로 인정되고, 근로관계 유지를 위한 최소한의 신뢰 관계가 훼손되어 해고는 적정하며, 징계효
- `id_4267` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유가 일부 인정되고 절차가 정당하나 양정이 과하여 징계가 부당하고, 부당노동행위에는 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취
- `id_42689` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유 일부가 인정되고 징계양정이 과도하여 부당하나, 사용자의 부당노동행위 의사를 입증할 만한 객관적이고 명백한 증거가 없이 부당노동행위에는 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
