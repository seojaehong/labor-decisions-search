# contract_expiry_batch_125_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_125_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_8991` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자에게 촉탁직 재고용의 기대권이 인정되지 않고, 촉탁직 재고용 거절이 불이익 취급 및 지배·개입의 부당노동행위에 해당하지 않는다고 판정한 사
- `id_8997` [discrimination]
  - 변경: notes, conf:high→medium
  - notes: 정규직 전환기대권이 인정되고, 정규직 전환거절의 합리적 이유가 없어 부당하나, 정규직 전환거절은 부당노동행위로 인정하기 어렵다고 판정한 사례 —
- `id_905` [dismissal_validity]
  - 변경: notes
  - notes: 사용자의 퇴직 권고를 근로자가 수용하여 근로관계가 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효
- `id_9055` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'worker_status', 'dismissal_validity']→['procedure', 'training_opportunity', 'worker_status', 'dismissal_validity']
  - notes: 근로자가 무기계약 근로자에 해당하지는 않으나, 근로자에게 무기계약 전환기대권이 인정됨에도 불구하고 사용자가 무기계약 전환 심사절차를 거치지 않는
- `id_9057` [discrimination]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로계약을 체결하였고, 이후 근로자의 연령이 취업규칙상 정년에 도달하여 퇴직한 것으로 해고가 존재하지 않는다고 판정한 사례 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
