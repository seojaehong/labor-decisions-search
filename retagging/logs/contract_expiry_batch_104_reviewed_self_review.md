# contract_expiry_batch_104_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_104_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_52327` [worker_status]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로자1, 2는 근로기준법상 근로자로 볼 수 없고, 근로자3, 4는 사용자와 사용·종속 관계에서 근로를 제공한 근로자로 볼 수 있으며, 근로자3
- `id_5233` [dismissal_validity]
  - 변경: notes
  - notes: 근무기간이 2년을 초과하여 기간의 정함이 없는 근로계약을 체결한 근로자에 해당함에도 사용자가 정당한 이유 없이 계약기간 만료를 이유로 근로관계를
- `id_52339` [dismissal_validity]
  - 변경: notes
  - notes: 사용자의 일방적인 의사에 의해 근로관계가 종료되었다고 볼 수 없어 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유
- `id_52353` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 구제신청이 제척기간 도과 후에 제기되어 각하 사유에 해당한다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_52385` [discrimination]
  - 변경: notes
  - notes: 동일한 구청사 미화 업무를 수행하는 공무직에 비교하여 정규직 전환 당시 연령 등을 이유로 기간제근로자로 채용하였다는 사정만으로 정액급식비, 명절

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
