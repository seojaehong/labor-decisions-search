# contract_expiry_batch_090_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_090_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_45311` [discrimination]
  - 변경: notes
  - notes: 근로자들이 기간제 또는 단시간 근로자에 해당하고 비교대상근로자가 존재하며 차별적 처우 금지영역에도 해당하나 차별적 처우가 없다고 판정한 사례 —
- `id_45325` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 만료에 따라 당사자 간 근로관계가 종료되었으므로 해고가 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이
- `id_45327` [renewal_expectation]
  - 변경: notes
  - notes: 갱신기대권이 인정되지 않아 근로계약기간 만료로 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_45333` [dismissal_validity]
  - 변경: notes, conf:high→medium
  - notes: 근로계약 관계는 일용 근로계약 관계에 해당하는 것으로 2021. 10. 21. 당일 근로를 종료함으로써 이 사건 근로자와의 근로계약은 종료되었음
- `id_45341` [discrimination]
  - 변경: notes
  - notes: 전임연구원은 동종 또는 유사한 업무에 종사하는 근로자로 볼 수 없으므로 비교대상근로자가 존재하지 않는다고 판정한 사례 — discriminati

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
