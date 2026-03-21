# contract_expiry_batch_117_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_117_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_59669` [dismissal_validity]
  - 변경: notes
  - notes: 근로자들은 기간의 정함이 있는 근로계약을 체결한 기간제근로자로서 근로계약기간 만료로 근로관계가 종료되었으므로 해고는 존재하지 않는다고 판정한 사
- `id_5967` [dismissal_validity]
  - 변경: notes
  - notes: 무기계약직의 인사 등에 대하여 정한 ‘무기계약직 및 기간제근로자 등 운용규정’이 별도로 있으므로 무기계약직에게는 이 규정을 우선 적용하여야 하고
- `id_59673` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약 갱신에 대한 기대권은 인정되나 갱신 거절의 합리적인 이유가 있어 근로관계가 정당하게 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 
- `id_59681` [unfair_treatment]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['misconduct', 'procedure', 'disciplinary_severity', 'dismissal_validity']
  - notes: 업무상 배임을 징계사유로 근로자에게 행한 ‘정직 1월’의 징계처분은 정당하고, 부당노동행위로 볼 수 없다고 판정한 사례 — 부당노동행위(불이익취
- `id_59699` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 사용자1과 근로계약관계에 있으며, 정년으로 근로계약이 종료되었고, 갱신기대권은 존재하지 않는다고 판단한 사례 — 갱신기대권 성립 여부 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
