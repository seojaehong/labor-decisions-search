# misconduct_remaining_batch_087_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_087_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_409655` [misconduct]
  - 변경: notes
  - notes: 정직은 중대한 절차하자가 있어 부당하고, 직위해제는 업무상 필요성이 인정되고 생활상 불이익이 있다고 보기 어려워 정당하다고 판정한 사례 — 비위
- `id_409667` [unfair_treatment]
  - 변경: notes
  - notes: 사용자에게 고용관계를 원상회복하겠다는 진정성이 있다고 볼 수 없으므로 구제신청의 이익이 존재하며, 정당한 징계사유가 확인되지 않아 부당해고이나,
- `id_40967` [unfair_treatment]
  - 변경: notes
  - notes: 해고의 징계사유가 일부 인정되나 양정이 과하여 부당하며, 보직해임은 인사명령으로 근무장소 변경 외에 별도의 불이익을 수반하지 않아 구제이익이 없
- `id_409673` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 기관사의 승무 출무 관리 및 적합성 검사를 소홀히 한 징계 사유가 존재하고, 징계양정 및 절차의 정당성이 인정된다고 판정한 사례 — 징계·해고 
- `id_409685` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 양정과 절차 모두 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
