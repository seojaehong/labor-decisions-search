# contract_expiry_batch_035_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_035_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_30309` [discrimination]
  - 변경: notes, secondary:['dismissal_validity', 'renewal_expectation']→['renewal_expectation', 'dismissal_validity']
  - notes: 근로자는 기간제근로자로서 근로계약의 갱신기대권이 인정되고, 갱신거절에 합리적 이유가 없어 근로관계 종료가 부당하다고 판정한 사례 — discri
- `id_30313` [renewal_expectation]
  - 변경: notes
  - notes: 근로자가 담당한 청년내일채움공제사업의 배정인원이 크게 축소되는 등 근로자에게 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없어 근로관계는 계
- `id_30321` [renewal_expectation]
  - 변경: notes
  - notes: 근로자가 근로계약 만료로 퇴사한다는 내용의 사직서를 제출하여 근로관계는 계약기간 만료로 정당하게 종료된 것으로 해고가 존재하지 않는다고 판정 —
- `id_30323` [dismissal_validity]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로계약을 체결한 근로자가 산업재해로 요양 중이라도 근로계약기간이 만료되면 당연히 근로관계는 종료되므로 구제신청의 이익이 없
- `id_30327` [worker_status]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로자에게 계약기간 만료를 이유로 계약종료를 통보한 것은 부당하다고 판정한 사례 — worker_status 판단이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
