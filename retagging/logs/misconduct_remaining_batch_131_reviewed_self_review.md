# misconduct_remaining_batch_131_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_131_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_55659` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 아파트 관리사무소 직원으로서 입주민 요청 등에 대한 부적절한 대응, 상사의 직무상 명령 지속적 불이행, 사용자에 대한 폭력적 언동 등을 한 징계
- `id_55671` [disciplinary_severity]
  - 변경: notes
  - notes: 해고는 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 
- `id_55697` [misconduct]
  - 변경: notes
  - notes: 업무상 필요성이 존재하지 않으므로 직위해제 및 대기발령이 부당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_55721` [workplace_harassment]
  - 변경: notes
  - notes: 근로자의 직장 내 괴롭힘 행위 등은 징계사유로 인정되고 징계양정이 적정하며 징계절차도 적법하여 정직 1개월 처분은 정당하다고 판정한 사례 — 직
- `id_55729` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 모두 인정되고, 그 비위행위 정도에 비해 징계양정이 과하다고 보기 어려우며, 징계절차도 정당하므로 징계가 정당하다고 판정한 사례 — 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
