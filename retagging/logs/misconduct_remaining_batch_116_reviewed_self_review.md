# misconduct_remaining_batch_116_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_116_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_49559` [disciplinary_severity]
  - 변경: notes
  - notes: 조합원에 대한 제명의 징계가 정당하다고 보아 행정관청의 결의·처분에 대한 시정명령 의결 요청을 기각한 사례 — 징계양정(제재 수위)의 적정성이 
- `id_49585` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되며 그 양정이 과하다고 볼 수 없고 징계절차에 중대한 하자도 발견할 수 없으므로 정직 2주의 징계는 정당하다고 판정한 사례 — 
- `id_49591` [workplace_harassment]
  - 변경: notes
  - notes: 근로자의 직장 내 괴롭힘 행위가 인정되어 징계 사유가 존재하며 감봉처분은 경징계로 양정이 적정하므로 이 사건 징계처분이 정당하다고 판정한 사례 
- `id_49595` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 비위행위 9개 중 8개가 징계사유로 인정되고, 그 비위행위 정도에 비하여 양정이 과하지 않으며, 징계 절차의 하자가 있다고 볼 수 없으므로 해고
- `id_49603` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 대기발령은 구제이익이 존재하지 않고, 해고는 징계사유가 일부 인정되나 그 정도에 비해 양정이 과하여 부당하다고 판정한 사례 — 징계·해고 절차 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
