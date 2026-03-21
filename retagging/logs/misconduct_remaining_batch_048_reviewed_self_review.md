# misconduct_remaining_batch_048_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_048_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_346983` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에 대한 해고는 징계사유가 존재하고, 양정도 적정하며, 절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과
- `id_347003` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 위탁판매 관련 문서 허위발급 및 허위작성, 판매대금의 임의 처분 등 사용자의 업무를 방해하고, 복무규정을 위반한 징계사유가 존재하고, 징계양정이
- `id_347013` [disciplinary_severity]
  - 변경: notes
  - notes: 중요사항을 기만하여 임용된 근로자에 대한 징계해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_347017` [disciplinary_severity]
  - 변경: notes
  - notes: 직위해제는 규정에 위배되거나 권리남용에 해당된다고 볼 수 없으므로 정당하고, 해고는 근로자의 비위행위가 대부분 징계사유에 해당하고, 그 비위행위
- `id_347025` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하지 않으므로 해고가 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
